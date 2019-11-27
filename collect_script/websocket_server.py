
import json
import threading
import time
import gzip
import websocket
import redis
import pickle
from depth_info import DepthInfo
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

allow_channel = [(0, "BTC", "USDT"),(0, "ETH", "USDT"),(0, "XRP", "USDT"),(0, "BCH", "USDT"),(0, "LTC", "USDT"),(0, "EOS", "USDT"),(0, "BSV", "USDT"),(0, "XLM", "USDT"),(0, "TRX", "USDT"),(0, "ADA", "USDT"),
                 (1, "BTC", "USDT"),(1, "ETH", "USDT"),(1, "XRP", "USDT"),(1, "BCH", "USDT"),(1, "LTC", "USDT"),(1, "EOS", "USDT"),(1, "BSV", "USDT"),(1, "XLM", "USDT"),(1, "TRX", "USDT"),(1, "ADA", "USDT")]
clients = []
depth_client = {}
redis_db = redis.Redis(host='localhost', port=6379)


threadLock = threading.Lock()

class SimpleChat(WebSocket):
    def __init__(self, server, sock, address):
        WebSocket.__init__(self, server, sock, address)

    def handleMessage(self):
        print("收到消息:"+self.data)

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
                threadLock.acquire()
                key = (json_obj['param']['market'],json_obj['param']['order_coin'],json_obj['param']['base_coin'])
                if key not in depth_client:
                    depth_client[key] = []
                depth_client[(json_obj['param']['market'],json_obj['param']['order_coin'],json_obj['param']['base_coin'])].append((self, json_obj['param']['depth']))
                print("收到新的订阅")
                print(depth_client)
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
                        continue
                    depth_client[key][i][0].sendMessage(str_for_send)
            threadLock.release()
            #print("发送订阅")
            time.sleep(0.1)

thread = myThread()
thread.start()
server = SimpleWebSocketServer('', 8000, SimpleChat)
server.serveforever()