
import json
import threading
import time
import gzip
import websocket
import redis
import pickle
from depth_info import DepthInfo
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
#==========================
##开始抓取部分
import time
import depth_huobi
import depth_ok
import depth_binance
depth_huobi.StartCrwal()
depth_ok.StartCrwal()
depth_binance.StartCrwal()
#==========================
allow_channel = [(0, "BTC", "USDT"),(0, "ETH", "USDT"),(0, "XRP", "USDT"),(0, "BCH", "USDT"),(0, "LTC", "USDT"),(0, "EOS", "USDT"),(0, "BSV", "USDT"),(0, "XLM", "USDT"),(0, "TRX", "USDT"),(0, "ADA", "USDT"),
                 (1, "BTC", "USDT"),(1, "ETH", "USDT"),(1, "XRP", "USDT"),(1, "BCH", "USDT"),(1, "LTC", "USDT"),(1, "EOS", "USDT"),(1, "BSV", "USDT"),(1, "XLM", "USDT"),(1, "TRX", "USDT"),(1, "ADA", "USDT"),
                 (2, "BTC", "USDT"),(2, "ETH", "USDT"),(2, "XRP", "USDT"),(2, "BCH", "USDT"),(2, "LTC", "USDT"),(2, "EOS", "USDT"),(2, "BSV", "USDT"),(2, "XLM", "USDT"),(2, "TRX", "USDT"),(2, "ADA", "USDT")]
clients = []
depth_client = {}
redis_db = redis.Redis(host='localhost', port=6379)


threadLock = threading.Lock()

class SimpleChat(WebSocket):
    def __init__(self, server, sock, address):
        WebSocket.__init__(self, server, sock, address)
        self.timer = None
    #处理超时
    def reset_timer(self):
        if self.timer and self.timer.isAlive():
            self.timer.cancel()
        self.timer = threading.Timer(10, self.shut_down)
        self.timer.start()
    def shut_down(self):
        print("shutdown")
        self.close()
    def handleMessage(self):
        json_obj = None
        try:
            json_obj = json.loads(self.data)
            if "ping" in json_obj:
                self.reset_timer()
                self.sendMessage(json.dumps({"pong":json_obj["ping"]}))
                return
        except:
            self.close()
            print("json解析失败")
            return
        if 'method' not in json_obj:
            self.close()
            print("参数不全")
            return
        #print(json_obj)
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
                if key not in depth_client:
                    depth_client[key] = []
                depth_client[(json_obj['param']['market'],json_obj['param']['order_coin'],json_obj['param']['base_coin'])].append((self, json_obj['param']['depth']))
                print("收到新的订阅")
                print(depth_client)
                threadLock.release()
        else:
            self.close()

    def handleConnected(self):
        self.reset_timer()
        print(self.address, 'connected')
        clients.append(self)

    def handleClose(self):
        clients.remove(self)
        print(self.closed)
import tracemalloc
tracemalloc.start()
_count = 0
class myThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self) 
    def run(self):
        global _count
        while True:
            _count = _count + 1
            if _count % 100 == 0:
                snapshot = tracemalloc.take_snapshot()
                top_stats = snapshot.statistics('lineno')

                print("[ Top 10 ]")
                for stat in top_stats[:10]:
                    print(stat)
                
            threadLock.acquire()
            for key in depth_client:
                #遍历订阅频道
                if len(depth_client[key]) == 0:
                    #订阅者为0的直接滚
                    continue
                #获取订阅信息
                data_db = redis_db.get(str(key[0])+'_'+key[1].upper()+'_'+key[2].upper())
                if data_db is None:
                    continue
                obj = pickle.loads(data_db)
                str_for_send = json.dumps(obj.dumps())
                for i in range(len(depth_client[key])-1, -1, -1):
                    #将订阅信息发送给每个没断开的订阅者
                    if depth_client[key][i][0].closed == True:
                        depth_client[key].pop(i)
                        #print(depth_client)
                        continue
                    depth_client[key][i][0].sendMessage(str_for_send)
            threadLock.release()
            #print("发送订阅")
            time.sleep(0.1)

thread = myThread()
thread.start()
server = SimpleWebSocketServer('', 8000, SimpleChat)
server.serveforever()