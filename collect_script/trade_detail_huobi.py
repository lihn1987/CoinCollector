
import json
import threading
import time
import mysql.connector
import gzip
import websocket
import redis
import pickle
from trade_detail_info import TradeDetailInfo

class myThread (threading.Thread):
    def __init__(self, coin_list, detail_callback):
        threading.Thread.__init__(self)
        self.coin_list = coin_list
        self.coin_dict = {}
        self.ws = websocket.WebSocket()
        self.timer = None
        self.redis_db = redis.Redis(host='localhost', port=6379)
        self.callback = detail_callback
    def connect(self):
        self.ws.connect("wss://api.huobi.pro/ws", http_proxy_host="127.0.0.1", http_proxy_port=50617)
    def on_recv(self, str):
        self.reset_timer()
        json_data = json.loads(str)
        
        #对ping pong 的处理
        if 'ping' in json_data:
            send_data = {'pong':json_data['ping']}
            self.send_data(send_data)
        elif 'ch' in json_data:
            info_list = []
            key = (0, self.coin_dict[json_data['ch'].split(".")[1].upper()][0], self.coin_dict[json_data['ch'].split(".")[1].upper()][1])
            for item in json_data["tick"]["data"]:
                info = {}
                info["amount"] = item['amount']
                info["price"] = item['price']
                info["dir"] = 0 if item['direction'] == 'buy' else 1
                info["trade_time"] = item['ts']
                info_list.append(info)
            self.callback(key, info_list)

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
            "sub": "market.%s.trade.detail"%symbel.lower(),
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

coin_list=[("BTC", "USDT"),("ETH", "USDT"),("XRP", "USDT"),("BCH", "USDT"),("LTC", "USDT"),("EOS", "USDT"),("BSV", "USDT"),("XLM", "USDT"),("TRX", "USDT"),("ADA", "USDT"),
                 ("BTC", "USDT"),("ETH", "USDT"),("XRP", "USDT"),("BCH", "USDT"),("LTC", "USDT"),("EOS", "USDT"),("BSV", "USDT"),("XLM", "USDT"),("TRX", "USDT"),("ADA", "USDT")]

def run(detail_callback):
    thread_ = myThread(coin_list, detail_callback)
    thread_.start()


