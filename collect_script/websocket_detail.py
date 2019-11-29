
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
import db_base
allow_channel = [(0, "BTC", "USDT"),(0, "ETH", "USDT"),(0, "XRP", "USDT"),(0, "BCH", "USDT"),(0, "LTC", "USDT"),(0, "EOS", "USDT"),(0, "BSV", "USDT"),(0, "XLM", "USDT"),(0, "TRX", "USDT"),(0, "ADA", "USDT"),
                 (1, "BTC", "USDT"),(1, "ETH", "USDT"),(1, "XRP", "USDT"),(1, "BCH", "USDT"),(1, "LTC", "USDT"),(1, "EOS", "USDT"),(1, "BSV", "USDT"),(1, "XLM", "USDT"),(1, "TRX", "USDT"),(1, "ADA", "USDT")]
clients = []
detail_client = {}
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

trade_detail_huobi.run(detail_callback)
trade_detail_ok.run(detail_callback)



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
                        print(detail_client)
                        continue
                    #print(str_for_send)
                    if len(tmp):
                        print(str_for_send)
                        detail_client[key][i][0].sendMessage(str_for_send)
            threadLock.release()
            #print("发送订阅")
            time.sleep(0.1)
db_base.init_db()
thread = myThread()
thread.start()
server = SimpleWebSocketServer('', 8001, SimpleChat)
server.serveforever()