
import json
import threading
import time
import mysql.connector
import gzip
import websocket
import redis
import pickle
import zlib
import numpy
from depth_info import DepthInfo

    
class myThread (threading.Thread):
    def __init__(self, coin_pair):
        threading.Thread.__init__(self)
        self.coin_pair = coin_pair
        self.coin_dict = {}
        self.ws = websocket.WebSocket()
        self.timer = None
        self.redis_db = redis.Redis(host='localhost', port=6379)
        self.info = {}

    def connect(self):   
        print("开始连接")
        tmp_str = ''
        tmp_str+="/%s%s@depth20@100ms"%(self.coin_pair[0].lower(), self.coin_pair[1].lower())
        self.ws.connect("wss://stream.binance.com:9443/ws"+tmp_str, http_proxy_host="127.0.0.1", http_proxy_port=1087)
        print("连接完成")
    def on_recv(self, str):
        self.reset_timer()
        json_data = json.loads(str)
        if 'ping' in json_data:
            send_data = {'pong':json_data['ping']}
            self.send_data(send_data)
            print("binance ping")
        elif 'bids' in json_data:
            info = DepthInfo()
            info.order_coin = self.coin_pair[0].upper()
            info.base_coin = self.coin_pair[1].upper()
            info.forbuy = json_data['bids']
            info.forsell = json_data['asks']
            info.up_time = 0
            info.market = 2
            key = "1_"+info.order_coin+"_"+info.base_coin
            self.redis_db.set(key, pickle.dumps(info))
        else:
            print("binance ping nimei")

    def shutdown(self):
        print("shutdown")
        self.ws.shutdown()
        self.ws.close()
    def send_data(self, obj):
        str = json.dumps(obj)
        print('send:'+str)
        self.ws.send(str.encode())
    #重置超时时间
    def reset_timer(self):
        if self.timer and self.timer.isAlive():
            self.timer.cancel()
        self.timer = threading.Timer(6*60, self.shutdown)
        self.timer.start()
    def run(self):
        while True:
            try:
                self.connect()
                print("连接成功！！！！！")
                #启动定时器
                if self.ws.connected:
                    self.reset_timer()
                #设置要监听的币种
                #self.sub_depth()
                while True:
                    recv_data = self.ws.recv()
                    if recv_data == '':
                        print("huobi recive 空")
                        break
                    #print(recv_data)
                    self.on_recv(recv_data)
            except:
                print(self.coin_pair)
                print("binance socket error")
                pass
coin_list=[("BTC", "USDT"),("ETH", "USDT"),("XRP", "USDT"),("BCH", "USDT"),("LTC", "USDT"),("EOS", "USDT"),("BSV", "USDT"),("XLM", "USDT"),("TRX", "USDT"),("ADA", "USDT")]
def StartCrwal():
    for item in coin_list:
        thread_ = myThread(item)
        thread_.start()
'''
StartCrwal()
while True:
    time.sleep(1)
'''





