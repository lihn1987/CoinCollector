
import json
import threading
import time
import mysql.connector
import gzip
import websocket
import redis
import pickle
from depth_info import DepthInfo
from config import config

class myThread (threading.Thread):
    def __init__(self, coin_list):
        threading.Thread.__init__(self)
        self.coin_list = coin_list
        self.coin_dict = {}
        self.ws = websocket.WebSocket()
        self.timer = None
        self.redis_db = redis.Redis(host='localhost', port=6379)

    def connect(self):
        if config["proxy_config"]["proxy_use"]:
            self.ws.connect("wss://api.huobi.pro/ws", http_proxy_host=config["proxy_config"]["proxy_ip"], http_proxy_port=config["proxy_config"]["proxy_port"])
        else:
            self.ws.connect("wss://api.huobi.pro/ws")
    def on_recv(self, str):
        self.reset_timer()
        json_data = json.loads(str)
        
        #对ping pong 的处理
        if 'ping' in json_data:
            send_data = {'pong':json_data['ping']}
            self.send_data(send_data)
        elif 'ch' in json_data:
            deep_info = DepthInfo()
            deep_info.up_time = json_data['ts']
            deep_info.order_coin = self.coin_dict[json_data['ch'].split(".")[1].upper()][0]
            deep_info.base_coin = self.coin_dict[json_data['ch'].split(".")[1].upper()][1]
            deep_info.forbuy = json_data['tick']['bids']
            deep_info.forsell = json_data['tick']['asks']
            deep_info.market = 0
            key = "0_"+self.coin_dict[json_data['ch'].split(".")[1].upper()][0]+"_"+self.coin_dict[json_data['ch'].split(".")[1].upper()][1]
            self.redis_db.set(key, pickle.dumps(deep_info))
    def shutdown(self):
        print("shutdown")
        self.ws.shutdown()
        self.ws.close()
    def send_data(self, obj):
        str = json.dumps(obj)
        print('send:'+str)
        self.ws.send(str.encode())
    def sub_depth(self):
        for item in self.coin_list:
            symbel = item[0].upper()+item[1].upper()
            self.coin_dict[symbel] = (item[0].upper(), item[1].upper())
            self.send_data({
            "sub": "market.%s.depth.step0"%symbel.lower(),
            "id": "asefddfeasdfefgh"
            })
    #重置超时时间
    def reset_timer(self):
        if self.timer and self.timer.isAlive():
            self.timer.cancel()
        self.timer = threading.Timer(6, self.shutdown)
        self.timer.start()
    def run(self):
        while True:
            try:
                self.connect()
                #启动定时器
                if self.ws.connected:
                    self.reset_timer()
                #设置要监听的币种
                self.sub_depth()
                while True:
                    recv_data = self.ws.recv()
                    if recv_data == '':
                        print("huobi recive 空")
                        break
                    self.on_recv(gzip.decompress(recv_data).decode())
            except:
                print("huobi socket error")
                pass

coin_list=[("BTC", "USDT"),("ETH", "USDT"),("XRP", "USDT"),("BCH", "USDT"),("LTC", "USDT"),("EOS", "USDT"),("BSV", "USDT"),("XLM", "USDT"),("TRX", "USDT"),("ADA", "USDT")]

def StartCrwal():
    thread_ = myThread(coin_list)
    thread_.start()
'''
StartCrwal()
while True:
    time.sleep(1)
'''