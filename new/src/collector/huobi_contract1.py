
import json
import threading
import time
import gzip
import websocket
from config import config
import sys
import redis
import urllib.request
import eth_usdt_kline
from enum import Enum
import key_main
import key_sub1
import hashlib
import hmac
import base64
import datetime
import logging
import os.path
import io
redis_db = redis.Redis(host=config["redis_config"]["host"], port=config["redis_config"]["port"])
#plan_index = 1 #高风险
#plan_index = 2 #低风险
plan_index = None

key = None
#1 1.5 2.5 5
#0  2   4  8
#amount = 0
#simulate
simu = False
sim_kline = None

DIR_NONE = 0
DIR_BUY = 1
DIR_SELL = 2

STEP_NONE = None
STEP_START_MAKER = 0
STEP_WAIT_MAKE = 1
STEP_DO_MAKER = 2
STEP_DO_PROFIT = 3

#系统参数
order_coin = "DOGE"
base_coin = "USDT"
persent_list = [1, 1.5, 2.5, 5]
step_list = None#[0, 0.03, 0.1, 0.2]


org_price = 0
trade_dir = DIR_NONE
maker_list = []

usdt_account = None
amount_usdt_all = None
amount_base = None
amount_order = None
amount_base_frezen = None
amount_order_frezen = None
trade_list = []

def GetPrefixLog():
    return "%s-%s %s"%(order_coin, base_coin, datetime.datetime.now())

def WatchDog():
    redis_db.set("%s-%s-%d-latest_time"%(order_coin, base_coin, plan_index), time.time())

def GetKline(period, size):
    global sim_kline
    if simu and size==1:
        return sim_kline
    else:
        while True:
            try:
                headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
                request = urllib.request.Request(url = 'https://api.hbdm.com/linear-swap-ex/market/history/kline?contract_code=%s-%s&period=%s&size=%d'%(order_coin, base_coin, period, size), headers = headers)
                response = urllib.request.urlopen(request, timeout=5)
                json_obj = json.loads(response.read().decode('utf-8'))
                if len(json_obj["data"]) == 0:
                    continue
                return json_obj["data"]
            except Exception as e:
                print("huobi symbol error:", e)
                pass
        
def GetPriceNow():
    item = GetKline("1min", 1)[0]
    price = (item["open"]+item["close"])/2
    print("获取得到当前中位价格为", price)
    return price

def CheckTime():
    now = datetime.datetime.now()
    while (now.hour == 23 and now.minute == 59 and now.second > 10) or\
        (now.hour == 7 and now.minute == 59 and now.second > 10) or\
        (now.hour == 15 and now.minute == 59 and now.second > 10) or\
        (now.hour == 0 and now.minute < 4) or\
        (now.hour == 8 and now.minute < 4) or\
        (now.hour == 16 and now.minute < 4):
        time.sleep(1)
        now = datetime.datetime.now()

def Post(path, args, show_log = False):
    WatchDog()
    CheckTime()
    while True:
        host = "api.hbdm.com"
        method =  "POST"
        time_str = datetime.datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%M:%S')
        
        sign_args = [
            "AccessKeyId=%s"%urllib.parse.quote(key.ak),
            "SignatureMethod=HmacSHA256",
            "SignatureVersion=2",
            "Timestamp="+urllib.parse.quote(time_str)
        ]
        
        sign_args_str = ""
        for item in sign_args:
            sign_args_str += item+"&"
        sign_args_str = sign_args_str[:-1]

        payload0 = '%s\n%s\n%s\n%s' % (method, host, path, sign_args_str)
        dig = hmac.new(key.sk.encode('utf-8'), msg=payload0.encode('utf-8'), digestmod=hashlib.sha256).digest()
        # 进行base64编码
        signature = base64.b64encode(dig).decode()
    
        try:
            headers = {'Content-Type':'application/json'}
            url = ("https://%s%s?"%(host, path))+\
                  ("AccessKeyId=%s"%key.ak)+\
                  ("&Signature=%s"%urllib.parse.quote(signature))+\
                  "&SignatureMethod=HmacSHA256"+\
                  "&SignatureVersion=2"+\
                  ("&Timestamp=%s"%time_str)
                  
            request = urllib.request.Request(
                url = url, 
                headers = headers, 
                data = json.dumps(args).encode("utf-8"), 
                method = 'POST'
            )
            response = urllib.request.urlopen(request, timeout=15)
            json_obj = json.loads(response.read().decode('utf-8'))
            #print(json_obj)
            if "status" in json_obj and json_obj["status"] == "error" and json_obj["err_code"]!= 1051:
                print(json_obj)
                print("Post error, continue")
                continue
            if "data" in json_obj and "errors" in json_obj["data"] and len(json_obj["data"]["errors"]) != 0:
                print(json_obj)
                print("Post error, continue")
                exit(0)
            if show_log:
                print(json_obj)

            #if path == "/linear-swap-api/v1/swap_cross_batchorder":
            #    raise "err"

            return json_obj
        except Exception as e:
            print("huobi symbol error:", e)
            if path == "/linear-swap-api/v1/swap_cross_batchorder":
                print("挂单超时，检测挂单是否成功")
                result, result_data = IsMaker()
                if result == True:
                    print("已经挂单成功,模拟成功返回")
                    sim_result = {
                        'status': 'ok', 
                        'data': {
                            'errors': [], 
                            'success': [
                                #{'order_id': 812240758404116480, 'index': 1, 'order_id_str': '812240758404116480'}, 
                                #{'order_id': 812240758420893696, 'index': 2, 'order_id_str': '812240758420893696'}, 
                                #{'order_id': 812240758437670912, 'index': 3, 'order_id_str': '812240758437670912'}
                            ]
                        }
                    }
                    for item in result_data["data"]["orders"]:
                        sim_result["data"]["success"].insert(0, {
                            'order_id':item['order_id'],
                            'order_id_str':str(item["order_id"])
                        })
                    return sim_result
                else:
                     pass
            pass

def ClearMaker():
    print("开始清空所有订单")
    Post("/linear-swap-api/v1/swap_cross_cancelall", args = {
        "contract_code":"%s-%s"%(order_coin, base_coin)
    })

def Maker():
    global maker_list
    args = {
        "orders_data":[]
    }
    print("开始挂单>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    for item in maker_list:
        if trade_dir == DIR_NONE:
            offset = "open"
        elif trade_dir == DIR_BUY:
            if item[0] == DIR_BUY:
                offset = "open"
            elif item[0] == DIR_SELL:
                offset = "close"
        elif trade_dir == DIR_SELL:
            if item[0] == DIR_BUY:
                offset = "close"
            elif item[0] == DIR_SELL:
                offset = "open"
                
        args["orders_data"].append({
            "contract_code":"%s-%s"%(order_coin,base_coin),
            "price": ("{0:.%df}"%price_point).format(item[1]),
            "volume":item[2],
            "direction":"buy" if item[0] == DIR_BUY else "sell",
            "offset":offset,
            "lever_rate":10,
            "order_price_type":"limit"
            
        })
        print("订单类型:", offset)
        print("方向:", "买" if item[0] == DIR_BUY else "卖")
        print("价格:", item[1])
        print("数量:", item[2])
        print("======================================")
    post_rtn = Post("/linear-swap-api/v1/swap_cross_batchorder", args)
    print(post_rtn)
    #配置maker_list的orderid
    print(maker_list)
    for i in range(len(maker_list)):
        maker_list[i][3] = post_rtn["data"]["success"][i]["order_id"]
    print("挂单详情为",maker_list)

def IsMaker():
    result = Post("/linear-swap-api/v1/swap_cross_openorders", {
        "contract_code":"%s-%s"%(order_coin,base_coin),
    }, True)
    if len(result["data"]["orders"]) > 0:
        return (True, result)
    else:
        return (False, result)

def SyncMaker():
    if not simu:
        ClearMaker()
        Maker()
        redis_db.set("%s-%s-maker_list"%(order_coin,base_coin), json.dumps(maker_list))
    else:
        print("开始挂单>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        for item in maker_list:
            if trade_dir == DIR_NONE:
                offset = "open"
            elif trade_dir == DIR_BUY:
                if item[0] == DIR_BUY:
                    offset = "open"
                elif item[0] == DIR_SELL:
                    offset = "close"
            elif trade_dir == DIR_SELL:
                if item[0] == DIR_BUY:
                    offset = "close"
                elif item[0] == DIR_SELL:
                    offset = "open"
                    

            print("订单类型:", offset)
            print("方向:", "买" if item[0] == DIR_BUY else "卖")
            print("价格:", item[1])
            print("数量:", item[2])
            print("======================================")

def StartMaker(price):
    global maker_list
    if plan_index == 1:#较低风险
        maker_list = [[DIR_BUY, price*0.97, GetCountPersent(price, DIR_BUY)[0], 0], [DIR_SELL, price*1.03, GetCountPersent(price, DIR_SELL)[0],0]]
    elif plan_index == 2:#高风险
        maker_list = [[DIR_BUY, price*0.97, GetCountPersent(price, DIR_BUY)[0], 0], [DIR_SELL, price*1.03, GetCountPersent(price, DIR_SELL)[0],0]]
    SyncAmount(maker_list, [],[])
    SyncMaker()

def GetSellPriceAndCount():
    sum_count = 0
    sum_money = 0
    for item in trade_list:
        sum_count += item[2]
        sum_money += item[1]*item[2]
    print(trade_list)
    print("GetSellPriceAndCount", (DIR_BUY if trade_dir == DIR_SELL else DIR_SELL, sum_money/sum_count*(0.9846 if trade_dir == DIR_SELL else 1.0154), sum_count))
    price = None
    """
    if trade_dir == DIR_SELL:
        price = sum_money/sum_count*(0.986)-200
    elif trade_dir == DIR_BUY:
        price = sum_money/sum_count*(1.014)+200
    """
    if trade_dir == DIR_SELL:
        price = sum_money/sum_count*(0.9896)
    elif trade_dir == DIR_BUY:
        price = sum_money/sum_count*(1.0104)
    return (DIR_BUY if trade_dir == DIR_SELL else DIR_SELL, price, sum_count, 0)
        
def SyncAmount(maker_list_add, maker_list_rm, maker_list_complate):
    global amount_base, amount_order, amount_base_frezen, amount_order_frezen
    for item in maker_list_add:
        print("item",item)
        if item[0] == DIR_BUY:
            amount_base -= item[1]*item[2]
            amount_base_frezen += item[1]*item[2]
        elif item[0] == DIR_SELL:
            amount_order -= item[2]
            amount_order_frezen += item[2]

    for item in maker_list_rm:
        if item[0] == DIR_BUY:
            amount_base += item[1]*item[2]
            amount_base_frezen -= item[1]*item[2]
        elif item[0] == DIR_SELL:
            amount_order += item[2]
            amount_order_frezen -= item[2]
            

    for item in maker_list_complate:
        #print("complate item:", item)
        if item[0] == DIR_BUY:
            amount_base_frezen -= item[1]*item[2]
            amount_order += item[2]
        elif item[0] == DIR_SELL:
            amount_order_frezen -= item[2]
            amount_base += item[1]*item[2]
    #print("amount_base:%f ,amount_order:%f , amount_base_frezen:%f ,amount_order_frezen:%f"%(amount_base,amount_order, amount_base_frezen,amount_order_frezen))

def PrintAmount():
    print("amount_base:%f ,amount_order:%f , amount_base_frezen:%f ,amount_order_frezen:%f"%(amount_base,amount_order, amount_base_frezen,amount_order_frezen))

def GetCountPersent(price, dir):
    rtn = []
    if dir == DIR_BUY:
        sum = 0
        for i in range(len(persent_list)):
            sum += persent_list[i]*(1-step_list[i])
        rtn = [
            int(amount_usdt_all*persent_list[0]*(1-step_list[0])/sum/((1-step_list[0])*price)),
            int(amount_usdt_all*persent_list[1]*(1-step_list[1])/sum/((1-step_list[1])*price)),
            int(amount_usdt_all*persent_list[2]*(1-step_list[2])/sum/((1-step_list[2])*price)),
            int(amount_usdt_all*persent_list[3]*(1-step_list[3])/sum/((1-step_list[3])*price)),
            ]
    elif dir == DIR_SELL:
        sum = 0
        for i in range(len(persent_list)):
            sum += persent_list[i]*(1+step_list[i])
        rtn = [
            int(amount_usdt_all*persent_list[0]*(1+step_list[0])/sum/((1+step_list[0])*price)),
            int(amount_usdt_all*persent_list[1]*(1+step_list[1])/sum/((1+step_list[1])*price)),
            int(amount_usdt_all*persent_list[2]*(1+step_list[2])/sum/((1+step_list[2])*price)),
            int(amount_usdt_all*persent_list[3]*(1+step_list[3])/sum/((1+step_list[3])*price)),
            ]
    return rtn

def GetPersentMaker(price, dir):
    rtn = []
    if dir == DIR_BUY:
        sum = 0
        for i in range(len(persent_list)):
            sum += persent_list[i]*(1-step_list[i])
        rtn = [
            [dir, (1-step_list[0])*price, int(amount_usdt_all*persent_list[0]*(1-step_list[0])/sum/((1-step_list[0])*price)), 0],
            [dir, (1-step_list[1])*price, int(amount_usdt_all*persent_list[1]*(1-step_list[1])/sum/((1-step_list[1])*price)), 0],
            [dir, (1-step_list[2])*price, int(amount_usdt_all*persent_list[2]*(1-step_list[2])/sum/((1-step_list[2])*price)), 0],
            [dir, (1-step_list[3])*price, int(amount_usdt_all*persent_list[3]*(1-step_list[3])/sum/((1-step_list[3])*price)), 0],
            ]
    elif dir == DIR_SELL:
        sum = 0
        for i in range(len(persent_list)):
            sum += persent_list[i]*(1+step_list[i])
        rtn = [
            [dir, (1+step_list[0])*price, int(amount_usdt_all*persent_list[0]*(1+step_list[0])/sum/((1+step_list[0])*price)), 0],
            [dir, (1+step_list[1])*price, int(amount_usdt_all*persent_list[1]*(1+step_list[1])/sum/((1+step_list[1])*price)), 0],
            [dir, (1+step_list[2])*price, int(amount_usdt_all*persent_list[2]*(1+step_list[2])/sum/((1+step_list[2])*price)), 0],
            [dir, (1+step_list[3])*price, int(amount_usdt_all*persent_list[3]*(1+step_list[3])/sum/((1+step_list[3])*price)), 0],
            ]
    print("GetCountPersent", rtn)
    return rtn

#获取未成交委托

def WaitMaker():
    print("开始等待方向")
    global org_price,trade_dir, open_count
    event_flag = False
    event_idx = 0
    while True:
        post_rtn = Post("/linear-swap-api/v1/swap_cross_openorders", {"contract_code":"%s-%s"%(order_coin, base_coin)})
        #查找完成的订单
        for idx, item in enumerate(maker_list):
            finded = False
            for maker_item in post_rtn["data"]["orders"]:
                if item[3] == maker_item["order_id"]:
                    finded = True
                    break
            if finded == False:
                #有订单完成了！
                event_flag = True
                event_idx = idx
                org_price = item[1]
                trade_dir = item[0]
                trade_list.append(list([item[0], item[1], item[2]]))
                break
        if event_flag:
            print("有订单完成了:", maker_list[event_idx])
            SyncAmount([], [] ,[maker_list[event_idx]])
            del maker_list[event_idx]
            SyncAmount([],maker_list ,[])
            del maker_list[0]
            PrintAmount()
            SaveEnv()
            return
        else:
            time.sleep(1)

def DoMaker():
    print("DoMaker")
    global maker_list
    if len(maker_list) == 0:
        maker_list = GetPersentMaker(org_price, trade_dir)[1:]
        print("开始挂梯度", maker_list)
        SyncAmount(maker_list, [],[])
        print("开始挂平单", maker_list)
        maker_list.append(list(GetSellPriceAndCount()))
        print("完成挂平单", maker_list)
        SyncAmount([list(GetSellPriceAndCount())], [], [])
        SyncMaker()

def DoProfit():
    print("开始等待盈利")
    while True:
        event_flag = False
        post_rtn = Post("/linear-swap-api/v1/swap_cross_openorders", {"contract_code":"%s-%s"%(order_coin, base_coin)})
        #查找完成的订单
        for idx, item in enumerate(maker_list):
            finded = False
            for maker_item in post_rtn["data"]["orders"]:
                if item[3] == maker_item["order_id"]:
                    finded = True
                    break
            if finded == False:
                #有订单完成了！
                event_flag = True
                event_idx = idx
                trade_list.append(list([item[0], item[1], item[2]]))
                break
        if event_flag:
            dir_tmp = maker_list[event_idx][0]
            print("有订单完成了", maker_list[event_idx])
            SyncAmount([], [] ,[maker_list[event_idx]])
            del maker_list[event_idx]

            if trade_dir != dir_tmp:
                print("盈利！！！！！！！！！！！！！！")
                SyncAmount([], maker_list, [])
                maker_list.clear()
                #SyncMaker()
                break
            else:
                print("加仓！！！！！！！！！！！！！！")
                #获取平仓单
                idx_tmp = 0
                for i in range(len(maker_list)):
                    if maker_list[i][0] != trade_dir:
                        idx_tmp = i
                        break
                #重新配置平仓单
                
                SyncAmount([], [maker_list[idx_tmp]] ,[])
                del maker_list[idx_tmp]
                maker_list.append(list(GetSellPriceAndCount()))
                SyncAmount([list(GetSellPriceAndCount())], [] ,[])
                print(maker_list)
                SyncMaker()
            SaveEnv()
        else:
            time.sleep(1)


def SaveEnv():
    print("SaveEnv")
    print("org_price", org_price)
    redis_db.set("%s-%s-org_price"%(order_coin, base_coin),org_price)
    redis_db.set("%s-%s-trade_dir"%(order_coin, base_coin),trade_dir)
    redis_db.set("%s-%s-maker_list"%(order_coin, base_coin),json.dumps(maker_list))
    redis_db.set("%s-%s-amount_usdt_all"%(order_coin, base_coin),amount_usdt_all)
    redis_db.set("%s-%s-amount_base"%(order_coin, base_coin),amount_base)
    redis_db.set("%s-%s-amount_order"%(order_coin, base_coin),amount_order)
    redis_db.set("%s-%s-amount_base_frezen"%(order_coin, base_coin),amount_base_frezen)
    redis_db.set("%s-%s-amount_order_frezen"%(order_coin, base_coin),amount_order_frezen)
    redis_db.set("%s-%s-trade_list"%(order_coin, base_coin),json.dumps(trade_list))

def LoadEnv():
    global org_price, trade_dir, maker_list, amount_usdt_all, amount_base, amount_order, amount_base_frezen, amount_order_frezen, trade_list
    try:
        org_price = float(redis_db.get("%s-%s-org_price"%(order_coin, base_coin)))
        trade_dir = int(redis_db.get("%s-%s-trade_dir"%(order_coin, base_coin)))
        maker_list = json.loads(redis_db.get("%s-%s-maker_list"%(order_coin, base_coin)))
        amount_usdt_all = float(redis_db.get("%s-%s-amount_usdt_all"%(order_coin, base_coin)))
        amount_base = float(redis_db.get("%s-%s-amount_base"%(order_coin, base_coin)))
        amount_order = float(redis_db.get("%s-%s-amount_order"%(order_coin, base_coin)))
        amount_base_frezen = float(redis_db.get("%s-%s-amount_base_frezen"%(order_coin, base_coin)))
        amount_order_frezen = float(redis_db.get("%s-%s-amount_order_frezen"%(order_coin, base_coin)))
        trade_list = json.loads(redis_db.get("%s-%s-trade_list"%(order_coin, base_coin)))
    except:
        ResetEnv()

def ResetEnv():
    global org_price, trade_dir, maker_list, amount_usdt_all, amount_base, amount_order, amount_base_frezen, amount_order_frezen, trade_list
    org_price = 0
    trade_dir = DIR_NONE
    maker_list = []
    amount_usdt_all = usdt_account/contract_size*10
    amount_base = amount_usdt_all
    amount_order = 0
    amount_base_frezen = 0
    amount_order_frezen = 0
    trade_list = []



def create_detail_day():
    # 年-月-日
    # daytime = datetime.datetime.now().strftime('day'+'%Y-%m-%d')
    # 年_月_日
    daytime = datetime.datetime.now().strftime('day'+'%Y_%m_%d')
    # 时：分：秒
    # hourtime = datetime.datetime.now().strftime("%H:%M:%S")
    # hourtime = datetime.datetime.now().strftime('time' + "%H_%M_%S")
    detail_time = daytime
    # print(daytime + "-" + hourtime)
    # detail_time = daytime + "__" + hourtime
    return detail_time


class Logger(object):
    def __init__(self, filename="Default.log", path="./"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        self.terminal = sys.stdout
        self.log = open(os.path.join(path, filename), "a", encoding='utf8')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.terminal.flush()
        self.log.flush()

    def flush(self):
        pass

import getopt
def ProcessArg():
    global order_coin, base_coin, persent_list, step_list, usdt_account,contract_size, price_point, key, plan_index
    cmd = None
    coin_name = None
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "d:c:k",  
                                   ["cmd=",
                                    "coin=",
                                    "key="])  # 长选项模式
     
    except:
        print("参数格式不正确")
 
    for opt, arg in opts:
        if opt in ['-d', '--cmd']:
            cmd = arg
        elif opt in ['-c', '--coin']:
            coin_name = arg
        elif opt in ['-k', '--key']:
            key = arg
    if key == "main":
        key = key_main.key
        plan_index = 1
    elif key == "sub":
        key = key_sub1.key
        plan_index = 2
    else:
        print("unknown key")
    if cmd == "start":
        persent_list = [1, 1.5, 2.5, 5]
        step_list = [0, 0.045, 0.108, 0.157]
        base_coin = "USDT"
        coin_list = {
            "DOGE":{
                "usdt_account": 350,
                "contract_size": 100,
                "price_point": 5
            },
            "XRP":{
                "usdt_account": 350,
                "contract_size": 10,
                "price_point": 4
            },
            "ZEC":{
                "usdt_account": 350,
                "contract_size": 0.1,
                "price_point": 2
            },
            "ALGO":{
                "usdt_account": 350,
                "contract_size": 10,
                "price_point": 4
            },
            "LINK":{
                "usdt_account": 350,
                "contract_size": 0.1,
                "price_point": 4
            },
            "DOT":{
                "usdt_account": 350,
                "contract_size": 1,
                "price_point": 4
            },
        }

        if coin_name in coin_list:
            order_coin = coin_name
            base_coin = "USDT"
            usdt_account = coin_list[coin_name]["usdt_account"]
            contract_size = coin_list[coin_name]["contract_size"]
            price_point = coin_list[coin_name]["price_point"]
        else:
            print("无法识别的币种")
            exit(1)
    elif cmd == "clear":
        if coin_name in ["ETH", "DOGE", "XRP", "ZEC", "ALGO", "LINK","DOT","SNX","NEO"]:
            keys = redis_db.keys("%s-USDT-*"%coin_name)
            print(keys)
            for item in keys:
                redis_db.delete(item)
            print("环境变量已清空")
            exit(1)
        else:
            print("无法识别的币种")
            exit(1)
    else:
        print("无法识别的命令")
        exit(1)

if __name__ == "__main__":
    
    ProcessArg()
    if simu:
        print("开始获取模拟k线")
        sim_kline = GetKline("1min", 20)
        print(sim_kline)
        

    #初始化日志
    sys.stdout = Logger("%s-%s"%(order_coin, base_coin) + '.log', path='')
    print(create_detail_day().center(60, '*'))
    print('explanation'.center(80, '*'))

    print("程序启动")
    step = redis_db.get("%s-%s-step"%(order_coin, base_coin))
    if step == None:
        step = 0
    else:
        step = int(step)
    LoadEnv()
    print("step",step)
    while True:
        if step == 0:
            print("开始获取当前市场价格,并部署买挂单")
            StartMaker(GetPriceNow())
            step += 1
            redis_db.set("%s-%s-step"%(order_coin, base_coin), step)
            SaveEnv()
#            exit(1)
        if step == 1:
            WaitMaker()
            step += 1
            redis_db.set("%s-%s-step"%(order_coin, base_coin), step)
            SaveEnv()
        if step == 2:
            DoMaker()
            step += 1
            redis_db.set("%s-%s-step"%(order_coin, base_coin), step)
            SaveEnv()
        if step == 3:
            DoProfit()
            ResetEnv()
            step = 0
            redis_db.set("%s-%s-step"%(order_coin, base_coin), step)
            SaveEnv()
            ClearMaker()
            SaveEnv()
            for i in range(5):
                time.sleep(1*60)
                WatchDog()

