
import urllib.request
import json
import numpy as np
import redis
from config import config
from multiprocessing import Process

def GetKline(symbol,period, size):

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    request = urllib.request.Request(url = 'https://api.huobi.pro/market/history/kline?symbol=%s&period=%s&size=%d'%(symbol, period, size), headers = headers)
    response = urllib.request.urlopen(request, timeout=15)
    kline_str = response.read().decode('utf-8')
    json_obj = json.loads(kline_str)
        
    rtn_obj = []
    try:
        for item in json_obj["data"]:
            rtn_obj.append([item["high"], item["low"]])
    except:
        print((symbol, period, size))
        print(kline_str)
        exit(0)
    
    return rtn_obj

def IsBuyTime(kline_list, price_margin):
    max=min=None
    for item in kline_list:
        if max == None or item[0] > max:
            max = item[0]
        if min == None or item[1] < min:
            min = item[1]
    if (max-min)*100.0/max > price_margin and max == kline_list[-1][0]:
        return (True,max)
    else:
        return (False, None)


def IsUnBuyTime(kline_list, low_price_margin, high_price_margin):
    max=min=None
    for item in kline_list:
        if max == None or item[0] > max:
            max = item[0]
        if min == None or item[1] < min:
            min = item[1]

    if (max-min)*100.0/max > high_price_margin and max == kline_list[-1][0]:
        return (True,max)
    elif (max-min)*100.0/max > low_price_margin and min == kline_list[-1][1]:
        return (True,min)
    else:
        return (False, None)

"""
    kline_list kline的相关数据[[high,low],[high,low]...]
    buy_width 窗口宽度
    fee 手续费
    buy_point 买点涨幅
    sell_point [止损卖点,止盈卖点]
"""
def GetProfit(kline_list, buy_width, fee, buy_point, sell_point):
    tran_list = []
    is_buy = False
    org_money = 100
    for idx in range(0, len(kline_list) - buy_width):
        if is_buy == False:
            (judge, price) = IsBuyTime(kline_list[idx:idx+buy_width], buy_point)
        else:
            (judge, price) = IsUnBuyTime(kline_list[idx:idx+buy_width], sell_point[0], sell_point[1])
        # 计算价格
        if judge and is_buy == False:
            # 买
            org_money = org_money/price*(1-fee)
            tran_list.append({
                "is_buy":True,
                "price":price,
                "account":org_money
            })
            #print("买", price,org_money)
        elif judge and is_buy == True:
            #卖
            org_money = org_money*price*(1-fee)
            tran_list.append({
                "is_buy":False,
                "price":price,
                "account":org_money
            })
            #print("卖", price,org_money)
        # 翻转买卖
        if judge:
            is_buy = not is_buy
    # 处理交易记录
    if len(tran_list) and tran_list[-1]["is_buy"] != False:
        tran_list = tran_list[:-1]
    return tran_list

# 一直进行分析
def Analyse(redis_db, symbol_pair, buy_width_range, buy_point_range, sell_point_range):
    while True:
        print("Analyse:",symbol_pair)
        symbol=symbol_pair[0].lower()+symbol_pair[1].lower()
        kline_type_list = ["1min", "5min", "15min", "30min", "60min", "4hour",]
        for kline_type in kline_type_list:
            try:
                kline_list = GetKline(symbol, kline_type, 2000)
                max_profit = 0
                best_buy_point = buy_point_range[0]
                best_sell_point_range = [sell_point_range[0][0], sell_point_range[1][0]]
                best_buy_width_range = buy_width_range[0]
                last_max_profit = 0
                for i in range(10):
                    # 寻找最优窗口宽度
                    for buy_width in range(buy_width_range[0], buy_width_range[1], 1):
                        tran_list = GetProfit(kline_list, buy_width, 0.002, best_buy_point, best_sell_point_range)
                        if len(tran_list):
                            if tran_list[-1]["account"] > max_profit:
                                max_profit = tran_list[-1]["account"]
                                best_buy_width_range = buy_width

                    # 寻找最优买点
                    for buy_point in np.arange(float(buy_point_range[0]), float(buy_point_range[1]), 0.1):
                        tran_list = GetProfit(kline_list, best_buy_width_range, 0.002, buy_point, best_sell_point_range)
                        if len(tran_list):
                            if tran_list[-1]["account"] > max_profit:
                                max_profit = tran_list[-1]["account"]
                                best_buy_point = buy_point

                    # 寻找最优止损点
                    for sell_point_1 in np.arange(float(sell_point_range[0][0]), float(sell_point_range[0][1]), 0.1):
                        tran_list = GetProfit(kline_list, best_buy_width_range, 0.002, best_buy_point, [sell_point_1, best_sell_point_range[1]])
                        if len(tran_list):
                            if tran_list[-1]["account"] > max_profit:
                                max_profit = tran_list[-1]["account"]
                                best_sell_point_range[0] = sell_point_1

                    #寻找最优获利点
                    for sell_point_2 in np.arange(float(sell_point_range[1][0]), float(sell_point_range[1][1]), 0.1):
                        tran_list = GetProfit(kline_list, best_buy_width_range, 0.002, best_buy_point, [best_sell_point_range[0], sell_point_2])
                        if len(tran_list):
                            if tran_list[-1]["account"] > max_profit:
                                max_profit = tran_list[-1]["account"]
                                best_sell_point_range[1] = sell_point_2

                    if last_max_profit == max_profit:
                        break
                    last_max_profit = max_profit
                    #print("max_profit:", max_profit)

                print("==============")
                print("symbol_pair:", symbol_pair)
                print("kline_type", kline_type)
                print("max_profit:", max_profit)
                print("best_buy_point:", best_buy_point)
                print("best_sell_point_range:", best_sell_point_range)
                print("best_buy_width_range:", best_buy_width_range)
                print("normal_profit", str((kline_list[-1][1] - kline_list[0][0])/kline_list[0][0]))


                redis_db.set("HAIGUI-"+symbol_pair[0]+"-"+symbol_pair[1]+"-HUOBI-"+kline_type+"-"+"max_profit", str(max_profit))
                redis_db.set("HAIGUI-"+symbol_pair[0]+"-"+symbol_pair[1]+"-HUOBI-"+kline_type+"-"+"best_buy_width_range", str(best_buy_width_range))
                redis_db.set("HAIGUI-"+symbol_pair[0]+"-"+symbol_pair[1]+"-HUOBI-"+kline_type+"-"+"best_buy_point", str(best_buy_point))
                redis_db.set("HAIGUI-"+symbol_pair[0]+"-"+symbol_pair[1]+"-HUOBI-"+kline_type+"-"+"best_sell_point_low", str(best_sell_point_range[0]))
                redis_db.set("HAIGUI-"+symbol_pair[0]+"-"+symbol_pair[1]+"-HUOBI-"+kline_type+"-"+"best_sell_point_hight", str(best_sell_point_range[1]))
                redis_db.set("HAIGUI-"+symbol_pair[0]+"-"+symbol_pair[1]+"-HUOBI-"+kline_type+"-"+"normal_profit", str((kline_list[-1][1] - kline_list[0][0])/kline_list[0][0]))
            except:
                # 超时
                pass






def restart_processes(process_list, coin_list, redis_db):
    print("restart process:", coin_list)
    for item in process_list:
        item.kill()
    # for i in range(0, len(coin_list), 8):
    #     p = Process(target=process_func, args=(coin_list[i: i+8 if i+8 < len(coin_list) else len(coin_list)],))
    #     p.start() 
    #     process_list.append(p)
    for item in coin_list:
        p = Process(target=Analyse, args=(redis_db, item, [5, 50], [0.1, 10], [[1,10], [1, 20]]))
        p.start() 
        process_list.append(p)

if __name__ == "__main__":
    redis_db = redis.Redis(host=config["redis_config"]["host"], port=config["redis_config"]["port"])
    # 若没设置，初始化只看BTC和ETH
    if redis_db.get("HUOBI-CONFIG") == None or redis_db.get("OK-CONFIG") == None:
        redis_db.set("HUOBI-CONFIG", '[["BTC", "USDT"], ["ETH", "USDT"]]')
        redis_db.set("OK-CONFIG", '["BTC-USDT", "ETH-USDT"]')

    process_list = []
    coin_list = json.loads(redis_db.get("HUOBI-CONFIG"))
    print(coin_list)
    restart_processes(process_list, coin_list, redis_db)
    #Analyse("btcusdt", [5, 50], [0.1, 10], [[1,10], [1, 20]])
    print("开始订阅监听币种的信息")
    ps = redis_db.pubsub()
    ps.subscribe('HUOBI-CONFIG') 
    next(ps.listen())
    for item in ps.listen():		#监听状态：有消息发布了就拿过来
        print("收到监听信息，重置采集")
        print(item)
        coin_list = json.loads(redis_db.get("HUOBI-CONFIG"))
        restart_processes(process_list, coin_list, redis_db)

#ps -ef | grep -v grep | grep quantitative_haigui.py  | awk '{print $2}' | xargs kill -9

    