
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
import datetime,pytz 
from config import config
def iso2timestamp(datestring, format='%Y-%m-%dT%H:%M:%S.%fZ',timespec='seconds'):
    """
    ISO8601时间转换为时间戳

    :param datestring:iso时间字符串 2019-03-25T16:00:00.000Z，2019-03-25T16:00:00.000111Z
    :param format:%Y-%m-%dT%H:%M:%S.%fZ；其中%f 表示毫秒或者微秒
    :param timespec:返回时间戳最小单位 seconds 秒，milliseconds 毫秒,microseconds 微秒
    :return:时间戳 默认单位秒
    """
    tz = pytz.timezone('Asia/Shanghai')
    utc_time = datetime.datetime.strptime(datestring, format)  # 将字符串读取为 时间 class datetime.datetime

    time = utc_time.replace(tzinfo=pytz.utc).astimezone(tz)

    times = {
        'seconds': int(time.timestamp()),
        'milliseconds': round(time.timestamp() * 1000),
        'microseconds': round(time.timestamp() * 1000 * 1000),
    }
    return times[timespec]

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
    def __init__(self, coin_list,callback):
        threading.Thread.__init__(self)
        self.coin_list = coin_list
        self.coin_dict = {}
        self.ws = websocket.WebSocket()
        self.timer = None
        self.redis_db = redis.Redis(host='localhost', port=6379)
        self.callback = callback
        for item in coin_list:
            self.coin_dict[item[0]+item[1]] = (item[0],item[1])
    def connect(self):
        tmp_str = ''
        for coin_item in coin_list:
            tmp_str+="/%s%s@trade"%(coin_item[0].lower(), coin_item[1].lower())

        if config["proxy_config"]["proxy_use"]:
            self.ws.connect("wss://stream.binance.com:9443/ws"+tmp_str, http_proxy_host=config["proxy_config"]["proxy_ip"], http_proxy_port=config["proxy_config"]["proxy_port"])
        else:
            self.ws.connect("wss://stream.binance.com:9443/ws"+tmp_str)
    def on_recv(self, str):
        self.reset_timer()
        json_data = json.loads(str)
        info = {}
        #print(json_data)
        info["dir"] = 0 if json_data['m']==True else 1
        info["price"] = float(json_data['p'])
        info["amount"] = float(json_data['q'])
        info["trade_time"] = json_data['T']
        key = (2, self.coin_dict[json_data['s']][0], self.coin_dict[json_data['s']][1])
        self.callback(key, [info])

    def shutdown(self):
        print("shutdown")
        self.ws.shutdown()
        self.ws.close()
    def send_data(self, obj):
        str = json.dumps(obj)
        print('send:'+str)
        self.ws.send(str.encode())
    def sub_detail(self):
        for item in self.coin_list:
            symbel = item[0].upper()+item[1].upper()
            self.coin_dict[symbel] = (item[0].upper(), item[1].upper())
            self.send_data({"op": "subscribe", "args": ["spot/trade:%s-%s"%(item[0].upper(),item[1].upper())]})
    #重置超时时间
    def reset_timer(self):
        if self.timer and self.timer.isAlive():
            self.timer.cancel()
        self.timer = threading.Timer(5, self.shutdown)
        self.timer.start()
    def run(self):
        while True:
            try:
                self.connect()
                #启动定时器
                if self.ws.connected:
                    self.reset_timer()
                #设置要监听的币种
                #self.sub_detail()
                while True:
                    recv_data = self.ws.recv()
                    print(recv_data)
                    self.on_recv(recv_data)
            except:
                print("binance socket error")
                pass
coin_list=[("BTC", "USDT"),("ETH", "USDT"),("XRP", "USDT"),("BCH", "USDT"),("LTC", "USDT"),("EOS", "USDT"),("BSV", "USDT"),("XLM", "USDT"),("TRX", "USDT"),("ADA", "USDT")]
def run(detail_callback):
    thread_ = myThread(coin_list, detail_callback)
    thread_.start()

