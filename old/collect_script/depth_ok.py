
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
from config import config

def OnChange(depth_info, change_info):
    #修改卖盘
    for_change = change_info['data'][0]['asks']
    for_change.reverse()
    for i in range(len(depth_info.forsell)-1, -1, -1):
        while True:
            if len(for_change) == 0 :
                break
            if len(for_change) != 0 and depth_info.forsell[i][0] == for_change[0][0] and for_change[0][1] == '0':
                #需要删除的
                depth_info.forsell.pop(i)
                for_change.pop(0)
                break

            elif len(for_change) != 0 and depth_info.forsell[i][0] == for_change[0][0] and for_change[0][1] != '0':
                #需要修改的
                depth_info.forsell[i][1] = for_change[0][1]
                for_change.pop(0)
                continue
        
            elif len(for_change) != 0 and float(depth_info.forsell[i][0]) < float(for_change[0][0]):
                depth_info.forsell.insert(i+1, for_change[0][0:2])
                for_change.pop(0)
                continue

            break
            
        if len(for_change) == 0 :
            break
        if i == 0:
            for_change.reverse()
            if len(for_change):
                depth_info.forsell = numpy.array(for_change)[:,0:2].tolist()+depth_info.forsell
    #修改买盘
    for_change = change_info['data'][0]['bids']
    for_change.reverse()
    for i in range(len(depth_info.forbuy)-1, -1, -1):
        while True:
            if len(for_change) == 0 :
                break
            if len(for_change) != 0 and depth_info.forbuy[i][0] == for_change[0][0] and for_change[0][1] == '0':
                #需要删除的
                depth_info.forbuy.pop(i)
                for_change.pop(0)
                break

            elif len(for_change) != 0 and depth_info.forbuy[i][0] == for_change[0][0] and for_change[0][1] != '0':
                #需要修改的
                depth_info.forbuy[i][1] = for_change[0][1]
                for_change.pop(0)
                continue
        
            elif len(for_change) != 0 and float(depth_info.forbuy[i][0]) > float(for_change[0][0]):
                depth_info.forbuy.insert(i+1, for_change[0][0:2])
                for_change.pop(0)
                continue

            break
            
        if len(for_change) == 0 :
            break
        if i == 0:
            for_change.reverse()
            if len(for_change):
                depth_info.forbuy = numpy.array(for_change)[:,0:2].tolist()+depth_info.forbuy

    #depth_info.dump()


    
class myThread (threading.Thread):
    def __init__(self, coin_list):
        threading.Thread.__init__(self)
        self.coin_list = coin_list
        self.coin_dict = {}
        self.ws = websocket.WebSocket()
        self.timer = None
        self.redis_db = redis.Redis(host='localhost', port=6379)
        self.info = {}
        for coin in coin_list:
            self.info[coin] = DepthInfo()

    def connect(self):
        if config["proxy_config"]["proxy_use"]:
            self.ws.connect("wss://real.okex.com:8443/ws/v3", http_proxy_host=config["proxy_config"]["proxy_ip"], http_proxy_port=config["proxy_config"]["proxy_port"])
        else:
            self.ws.connect("wss://real.okex.com:8443/ws/v3")
    def on_recv(self, str):
        self.reset_timer()
        json_data = json.loads(str)
        if 'event' not in json_data and json_data['action'] == 'partial':
            info = self.info[(json_data['data'][0]['instrument_id'].split("-")[0],json_data['data'][0]['instrument_id'].split("-")[1])]
            info.order_coin = json_data['data'][0]['instrument_id'].split("-")[0]
            info.base_coin = json_data['data'][0]['instrument_id'].split("-")[1]
            info.forbuy = numpy.array(json_data['data'][0]['bids'])[:,0:2].tolist()
            info.forsell = numpy.array(json_data['data'][0]['asks'])[:,0:2].tolist()
            info.up_time = json_data['data'][0]['timestamp']*1000
            info.market = 1
            key = "1_"+json_data['data'][0]['instrument_id'].split("-")[0]+"_"+json_data['data'][0]['instrument_id'].split("-")[1]
            self.redis_db.set(key, pickle.dumps(info))
        elif 'event' not in json_data and json_data['action'] == 'update':
            info = self.info[(json_data['data'][0]['instrument_id'].split("-")[0],json_data['data'][0]['instrument_id'].split("-")[1])]
            OnChange(info, json_data)
            key = "1_"+json_data['data'][0]['instrument_id'].split("-")[0]+"_"+json_data['data'][0]['instrument_id'].split("-")[1]
            self.redis_db.set(key, pickle.dumps(info))

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
            self.send_data({"op": "subscribe", "args": ["spot/depth:%s-%s"%(item[0].upper(),item[1].upper())]})
    #重置超时时间
    def reset_timer(self):
        if self.timer and self.timer.isAlive():
            self.timer.cancel()
        self.timer = threading.Timer(10, self.shutdown)
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
                    decompress = zlib.decompressobj(
                            -zlib.MAX_WBITS  # see above
                    )
                    inflated = decompress.decompress(recv_data)
                    inflated += decompress.flush()
                    self.on_recv(inflated.decode())
            except:
                print("ok socket error")
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

