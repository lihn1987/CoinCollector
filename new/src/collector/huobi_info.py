
import json
import threading
import time
import gzip
import websocket
from config import config
import sys
import redis
from multiprocessing import Process

class myThread (threading.Thread):
    def __init__(self, coin_list):
        threading.Thread.__init__(self)
        #保存要监控的币种
        self.coin_list = coin_list

        #保存 BTCUSDT =》 BTC USDT
        self.coin_dict = {}


        self.huobi_ws = websocket.WebSocket()
        self.timer = None
        self.redis_db = redis.Redis(host=config["redis_config"]["host"], port=config["redis_config"]["port"])

    def connect(self):
        if config["proxy_config"]["proxy_use"]:
            self.huobi_ws.connect("wss://api.huobi.pro/ws", http_proxy_host=config["proxy_config"]["proxy_ip"], http_proxy_port=config["proxy_config"]["proxy_port"])
        else:
            self.huobi_ws.connect("wss://api.huobi.pro/ws")

    def on_huobi_recv(self, str):
        self.reset_timer()
        json_data = json.loads(str)

        #对ping pong 的处理
        if 'ping' in json_data:
            send_data = {'pong':json_data['ping']}
            self.send_data(send_data)
        elif 'ch' in json_data:
            time_now = time.time()*1000#毫秒
            deep_info = {}
            deep_info["up_time"] = json_data['ts']
            order_coin = self.coin_dict[json_data['ch'].split(".")[1].upper()][0]
            base_coin = self.coin_dict[json_data['ch'].split(".")[1].upper()][1]
            deep_info["forbuy"] = json_data['tick']['bids']
            deep_info["forsell"] = json_data['tick']['asks']
            deep_info["market"] = 0
            deep_info["delay"] = (time_now-deep_info["up_time"])
            #保存到redis
            k = order_coin+"-"+base_coin+"-HUOBI-DEPTH"
            v = json.dumps(deep_info)
            self.redis_db.set(k, v)
            #print("深度延时", time_now-deep_info.up_time)
            #print(self.info)
            #key = "0_"+self.coin_dict[json_data['ch'].split(".")[1].upper()][0]+"_"+self.coin_dict[json_data['ch'].split(".")[1].upper()][1]


    def shutdown(self):
        print("shutdown")
        self.huobi_ws.shutdown()
        self.huobi_ws.close()

    def send_data(self, obj):
        str = json.dumps(obj)
        print('send:'+str)
        self.huobi_ws.send(str.encode())

    def sub_depth(self):
        print("sub depth")
        for item in self.coin_list:
            symbel = item[0].upper()+item[1].upper()
            self.coin_dict[symbel] = (item[0].upper(), item[1].upper())
            self.send_data({
            "sub": "market.%s.depth.step0"%symbel.lower(),
            "id": "asefddfeasdfefgh"
            })

    #重置超时时间
    def reset_timer(self):
        if self.timer and self.timer.is_alive():
            self.timer.cancel()
        self.timer = threading.Timer(6, self.shutdown)
        self.timer.start()

    def run(self):
        while True:
            try:
                self.connect()
                #启动定时器
                if self.huobi_ws.connected:
                    self.reset_timer()
                #设置要监听的币种
                self.sub_depth()
                while True:
                    recv_data = self.huobi_ws.recv()
                    if recv_data == '':
                        print("huobi recive 空")
                        break
                    self.on_huobi_recv(gzip.decompress(recv_data).decode())
            except:
                print("huobi socket error")
                pass

#coin_list=[("BTC", "USDT"),("ETH", "USDT"),]

def StartCrwal(coin_list):
    thread_ = myThread(coin_list)
    thread_.start()

def process_func(coin_list):
    print("process:", coin_list)
    StartCrwal(coin_list)

def restart_processes(process_list, coin_list):
    print("restart process:", coin_list)
    for item in process_list:
        item.kill()
    for i in range(0, len(coin_list), 8):
        p = Process(target=process_func, args=(coin_list[i: i+8 if i+8 < len(coin_list) else len(coin_list)],))
        p.start() 
        process_list.append(p)


if __name__ == "__main__":
    redis_db = redis.Redis(host=config["redis_config"]["host"], port=config["redis_config"]["port"])
    # 若没设置，初始化只看BTC和ETH
    if redis_db.get("HUOBI-CONFIG") == None or redis_db.get("OK-CONFIG") == None:
        redis_db.set("HUOBI-CONFIG", '[["BTC", "USDT"], ["ETH", "USDT"]]')
        redis_db.set("OK-CONFIG", '["BTC-USDT", "ETH-USDT"]')

    process_list = []
    coin_list = json.loads(redis_db.get("HUOBI-CONFIG"))
    restart_processes(process_list, coin_list)
    
    print("开始订阅监听币种的信息")
    ps = redis_db.pubsub()
    ps.subscribe('HUOBI-CONFIG') 
    next(ps.listen())
    for item in ps.listen():		#监听状态：有消息发布了就拿过来
        print("收到监听信息，重置采集")
        print(item)
        coin_list = json.loads(redis_db.get("HUOBI-CONFIG"))
        restart_processes(process_list, coin_list)
