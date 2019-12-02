
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
                 (1, "BTC", "USDT"),(1, "ETH", "USDT"),(1, "XRP", "USDT"),(1, "BCH", "USDT"),(1, "LTC", "USDT"),(1, "EOS", "USDT"),(1, "BSV", "USDT"),(1, "XLM", "USDT"),(1, "TRX", "USDT"),(1, "ADA", "USDT"),
                 (2, "BTC", "USDT"),(2, "ETH", "USDT"),(2, "XRP", "USDT"),(2, "BCH", "USDT"),(2, "LTC", "USDT"),(2, "EOS", "USDT"),(2, "BSV", "USDT"),(2, "XLM", "USDT"),(2, "TRX", "USDT"),(2, "ADA", "USDT")]
clients = []
depth_client = {}
redis_db = redis.Redis(host='localhost', port=6379)

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
        #print(json_obj)
        if json_obj['method'] == 'sub_analyse':
            if 'param' in json_obj and \
            'order_coin' in json_obj['param'] and \
            'base_coin' in json_obj['param'] and \
            'market' in json_obj['param'] and \
            'watch_type' in json_obj['param']:
                
                key = (json_obj['param']['market'],json_obj['param']['order_coin'],json_obj['param']['base_coin'])
                if key not in allow_channel:
                    return
                if key not in depth_client:
                    depth_client[key] = []
                depth_client[(json_obj['param']['market'],json_obj['param']['order_coin'],json_obj['param']['base_coin'])].append((self, json_obj['param']['watch_type']))
                print("收到新的订阅")
                print(depth_client)
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
            for key in depth_client:
                #遍历订阅频道
                if len(depth_client[key]) == 0:
                    #订阅者为0的直接滚
                    continue
                #获取订阅信息
                json_obj_min = {"type":"min_"+str(key[0])+"_"+key[1]+"_"+key[2],"data":[]}
                json_obj_hour = {"type":"hour_"+str(key[0])+"_"+key[1]+"_"+key[2],"data":[]}
                json_obj_day = {"type":"day_"+str(key[0])+"_"+key[1]+"_"+key[2],"data":[]}
                for i in range(len(depth_client[key])-1, -1, -1):
                    #清除已断开的客户端
                    if depth_client[key][i][0].closed == True:
                        depth_client[key].pop(i)
                        print(depth_client)
                        continue
                    #将订阅信息发送给每个没断开的订阅者
                    if "min" in depth_client[key][i][1]:
                        if len(json_obj_min["data"]) == 0:
                            redis_data = redis_db.get("trade_detail_min_"+str(key[0])+"_"+key[1]+"_"+key[2])
                            if redis_data is None:
                                json_obj_min["data"] = json.loads("[]")
                            else:
                                json_obj_min["data"] = json.loads(redis_data)
                        depth_client[key][i][0].sendMessage(json.dumps(json_obj_min))
                    if "hour" in depth_client[key][i][1]:
                        if len(json_obj_hour["data"]) == 0:
                            redis_data = redis_db.get("trade_detail_hour_"+str(key[0])+"_"+key[1]+"_"+key[2])
                            if redis_data is None:
                                json_obj_hour["data"] = json.loads("[]")
                            else:
                                json_obj_hour["data"] = json.loads(redis_data)
                        depth_client[key][i][0].sendMessage(json.dumps(json_obj_hour))
                    if "day" in depth_client[key][i][1]:
                        if len(json_obj_day["data"]) == 0:
                            redis_data = redis_db.get("trade_detail_day_"+str(key[0])+"_"+key[1]+"_"+key[2])
                            if redis_data is None:
                                json_obj_day["data"] = json.loads("[]")
                            else:
                                json_obj_day["data"] = json.loads(redis_data)
                        depth_client[key][i][0].sendMessage(json.dumps(json_obj_day))
            #print("发送订阅")
            time.sleep(0.5)

thread = myThread()
thread.start()
print("Start")
server = SimpleWebSocketServer('', 8002, SimpleChat)
print("Start Ok")
server.serveforever()