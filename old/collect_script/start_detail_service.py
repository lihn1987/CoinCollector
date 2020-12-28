
import json
import threading
import time
import gzip
import websocket
import redis
import pickle
from depth_info import DepthInfo
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

import trade_detail_huobi
import trade_detail_ok
import trade_detail_binance
import db_base
allow_channel = [(0, "BTC", "USDT"),(0, "ETH", "USDT"),(0, "XRP", "USDT"),(0, "BCH", "USDT"),(0, "LTC", "USDT"),(0, "EOS", "USDT"),(0, "BSV", "USDT"),(0, "XLM", "USDT"),(0, "TRX", "USDT"),(0, "ADA", "USDT"),
                 (1, "BTC", "USDT"),(1, "ETH", "USDT"),(1, "XRP", "USDT"),(1, "BCH", "USDT"),(1, "LTC", "USDT"),(1, "EOS", "USDT"),(1, "BSV", "USDT"),(1, "XLM", "USDT"),(1, "TRX", "USDT"),(1, "ADA", "USDT"),
                 (2, "BTC", "USDT"),(2, "ETH", "USDT"),(2, "XRP", "USDT"),(2, "BCH", "USDT"),(2, "LTC", "USDT"),(2, "EOS", "USDT"),(2, "BSV", "USDT"),(2, "XLM", "USDT"),(2, "TRX", "USDT"),(2, "ADA", "USDT")]
clients = []
detail_client = {}

for item in allow_channel:
    detail_client[item] = []
redis_db = redis.Redis(host='localhost', port=6379)
threadLock = threading.Lock()
detail_lock = threading.Lock()
trade_detail = {}
def detail_callback(key, info_list):
    #插入数据库
    if len(info_list):
        db_base.insert_into_trade_detail(key, info_list)
    #处理要展示的数据
    detail_lock.acquire()
    if key not in trade_detail:
        trade_detail[key] = []
    trade_detail[key] += info_list
    #太多了就需要删除
    if len(trade_detail[key]) > 10000:
        print("??????????????")
        trade_detail[key] = []
    detail_lock.release()
    #处理分钟，小时天的统计
    detail_analyse(key, info_list)
def detail_analyse(key, info_list):
    min_detail_analyse(key, info_list)
    hour_line_analyse(key, info_list)
    day_line_analyse(key, info_list)
def min_detail_analyse(key, info_list):
    #进行归类
    time_key = {}
    for info_item in info_list:
        print(type(info_item["trade_time"]))
        time_key_item = int(info_item["trade_time"]/1000/60)*1000*60
        if time_key_item not in time_key:
            time_key[time_key_item] = {}
            time_key[time_key_item]["buy"] = 0.0
            time_key[time_key_item]["sell"] = 0.0
        if info_item["dir"] == 0:
            time_key[time_key_item]["buy"]+= float(info_item["amount"])
        else:
            time_key[time_key_item]["sell"]+= float(info_item["amount"])
    #准备写入数据库
    key = "trade_detail_min_"+str(key[0])+"_"+key[1]+"_"+key[2]
    #读
    data_db = redis_db.get(key)
    if data_db is None:
        data_db = []
    else:
        data_db = json.loads(data_db)
    for time_key_item in time_key:
        if len(data_db)==0:
            data_db.append({"time":time_key_item, "buy":time_key[time_key_item]["buy"], "sell":time_key[time_key_item]["sell"]})
            break
        for i in range(len(data_db)):
            if time_key_item > data_db[i]["time"]:
                data_db.insert(i, {"time":time_key_item, "buy":time_key[time_key_item]["buy"], "sell":time_key[time_key_item]["sell"]})
                break
            elif time_key_item == data_db[i]["time"]:
                data_db[i]["buy"] += time_key[time_key_item]["buy"]
                data_db[i]["sell"] += time_key[time_key_item]["sell"]
                break
    #删除多余数据
    print(key)
    if len(data_db) > 60:
        del data_db[60:]
    redis_db.set(key, json.dumps(data_db))

def hour_line_analyse(key, info_list):
    #进行归类
    time_key = {}
    for info_item in info_list:
        print(type(info_item["trade_time"]))
        time_key_item = int(info_item["trade_time"]/1000/60/60)*1000*60*60
        if time_key_item not in time_key:
            time_key[time_key_item] = {}
            time_key[time_key_item]["buy"] = 0.0
            time_key[time_key_item]["sell"] = 0.0
        if info_item["dir"] == 0:
            time_key[time_key_item]["buy"]+= float(info_item["amount"])
        else:
            time_key[time_key_item]["sell"]+= float(info_item["amount"])
    #准备写入数据库
    key = "trade_detail_hour_"+str(key[0])+"_"+key[1]+"_"+key[2]
    #读
    data_db = redis_db.get(key)
    if data_db is None:
        data_db = []
    else:
        data_db = json.loads(data_db)
    for time_key_item in time_key:
        if len(data_db)==0:
            data_db.append({"time":time_key_item, "buy":time_key[time_key_item]["buy"], "sell":time_key[time_key_item]["sell"]})
            break
        for i in range(len(data_db)):
            if time_key_item > data_db[i]["time"]:
                data_db.insert(i, {"time":time_key_item, "buy":time_key[time_key_item]["buy"], "sell":time_key[time_key_item]["sell"]})
                break
            elif time_key_item == data_db[i]["time"]:
                data_db[i]["buy"] += time_key[time_key_item]["buy"]
                data_db[i]["sell"] += time_key[time_key_item]["sell"]
                break
    #删除多余数据
    print(key)
    if len(data_db) > 60:
        del data_db[60:]
    redis_db.set(key, json.dumps(data_db))
def day_line_analyse(key, info_list):
    #进行归类
    time_key = {}
    for info_item in info_list:
        print(type(info_item["trade_time"]))
        time_key_item = int(info_item["trade_time"]/1000/60/60/24)*1000*60*60*24
        if time_key_item not in time_key:
            time_key[time_key_item] = {}
            time_key[time_key_item]["buy"] = 0.0
            time_key[time_key_item]["sell"] = 0.0
        if info_item["dir"] == 0:
            time_key[time_key_item]["buy"]+= float(info_item["amount"])
        else:
            time_key[time_key_item]["sell"]+= float(info_item["amount"])
    #准备写入数据库
    key = "trade_detail_day_"+str(key[0])+"_"+key[1]+"_"+key[2]
    #读
    data_db = redis_db.get(key)
    if data_db is None:
        data_db = []
    else:
        data_db = json.loads(data_db)
    for time_key_item in time_key:
        if len(data_db)==0:
            data_db.append({"time":time_key_item, "buy":time_key[time_key_item]["buy"], "sell":time_key[time_key_item]["sell"]})
            break
        for i in range(len(data_db)):
            if time_key_item > data_db[i]["time"]:
                data_db.insert(i, {"time":time_key_item, "buy":time_key[time_key_item]["buy"], "sell":time_key[time_key_item]["sell"]})
                break
            elif time_key_item == data_db[i]["time"]:
                data_db[i]["buy"] += time_key[time_key_item]["buy"]
                data_db[i]["sell"] += time_key[time_key_item]["sell"]
                break
    #删除多余数据
    print(key)
    if len(data_db) > 60:
        del data_db[60:]
    redis_db.set(key, json.dumps(data_db))
trade_detail_huobi.run(detail_callback)
trade_detail_ok.run(detail_callback)
trade_detail_binance.run(detail_callback)


class SimpleChat(WebSocket):
    def __init__(self, server, sock, address):
        WebSocket.__init__(self, server, sock, address)

    def handleMessage(self):
        json_obj = None
        try:
            json_obj = json.loads(self.data)
        except:
            self.close()
            print("json解析失败")
            return
        if 'method' not in json_obj:
            self.close()
            print("参数不全")
            return
        print(json_obj)
        if json_obj['method'] == 'sub_depth':
            if 'param' in json_obj and \
            'order_coin' in json_obj['param'] and \
            'base_coin' in json_obj['param'] and \
            'depth' in json_obj['param'] and \
            'market' in json_obj['param']:
                
                key = (json_obj['param']['market'],json_obj['param']['order_coin'],json_obj['param']['base_coin'])
                if key not in allow_channel:
                    return
                threadLock.acquire()
                if key not in detail_client:
                    detail_client[key] = []
                detail_client[(json_obj['param']['market'],json_obj['param']['order_coin'],json_obj['param']['base_coin'])].append((self, json_obj['param']['depth']))
                print("收到新的订阅")
                print(detail_client)
                threadLock.release()
        else:
            self.close()

    def handleConnected(self):
       print(self.address, 'connected')
       clients.append(self)

    def handleClose(self):
        clients.remove(self)
        print(self.closed)

class myThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self) 
    def run(self):
        while True:
            threadLock.acquire()
            for key in detail_client:
                #遍历订阅频道
                if len(detail_client[key]) == 0 or (key[0], key[1].upper(), key[2].upper()) not in trade_detail:
                    #订阅者为0的直接滚
                    trade_detail[(key[0], key[1].upper(), key[2].upper())] = []
                    continue
                #获取订阅信息
                detail_lock.acquire()
                str_for_send = json.dumps({
                    'market':key[0],
                    'order_coin':key[1].upper(),
                    'base_coin':key[2].upper(),
                    'data':trade_detail[(key[0], key[1].upper(), key[2].upper())]})
                tmp = trade_detail[(key[0], key[1].upper(), key[2].upper())]
                trade_detail[(key[0], key[1].upper(), key[2].upper())] = []
                detail_lock.release()
                for i in range(len(detail_client[key])-1, -1, -1):
                    #将订阅信息发送给每个没断开的订阅者
                    if detail_client[key][i][0].closed == True:
                        detail_client[key].pop(i)
                        #print(detail_client)
                        continue
                    #print(str_for_send)
                    if len(tmp):
                        #print(str_for_send)
                        detail_client[key][i][0].sendMessage(str_for_send)
            threadLock.release()
            #print("发送订阅")
            time.sleep(0.1)
db_base.init_db()
thread = myThread()
thread.start()
server = SimpleWebSocketServer('', 8001, SimpleChat)
server.serveforever()