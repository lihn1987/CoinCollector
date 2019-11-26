
import json
import threading
import time
import mysql.connector
import gzip
import websocket
import redis
import pickle
import zlib
class myThread (threading.Thread):
    def __init__(self, coin_list):
        threading.Thread.__init__(self)
        self.coin_list = coin_list
        self.coin_dict = {}
        self.ws = websocket.WebSocket()
        self.timer = None
        self.redis_db = redis.Redis(host='localhost', port=6379)

    def connect(self):
        self.ws.connect("wss://real.okex.com:8443/ws/v3", http_proxy_host="127.0.0.1", http_proxy_port=50617)
    def on_recv(self, str):
        print("recive:"+str)
        '''
        self.reset_timer()
        json_data = json.loads(str)
        #对ping pong 的处理
        if 'ping' in json_data:
            send_data = {'pong':json_data['ping']}
            self.send_data(send_data)
        elif 'ch' in json_data:
            print(json_data['ch'].split(".")[1])
            print(self.coin_dict[json_data['ch'].split(".")[1].upper()])
            key = "0_"+self.coin_dict[json_data['ch'].split(".")[1].upper()][0]+"_"+self.coin_dict[json_data['ch'].split(".")[1].upper()][1]
            self.redis_db.set(key, pickle.dumps(json_data))
        '''
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
            print(item)
            symbel = item[0].upper()+item[1].upper()
            self.coin_dict[symbel] = (item[0].upper(), item[1].upper())
            self.send_data({"op": "subscribe", "args": ["spot/depth:%s-%s"%(item[0].upper(),item[1].upper())]})
    #重置超时时间
    def reset_timer(self):
        if self.timer and self.timer.isAlive():
            self.timer.cancel()
        self.timer = threading.Timer(6, self.shutdown)
        self.timer.start()
    def run(self):
        while True:
            #try:
                print('-------0.1')
                self.connect()
                print('-------0.2')
                #启动定时器
                if self.ws.connected:
                    self.reset_timer()
                #设置要监听的币种
                print('-------1')
                self.sub_depth()
                print('-------2')
                while True:
                    print('-------3')
                    recv_data = self.ws.recv()
                    print('-------4')
                    if recv_data == '':
                        print("huobi recive 空")
                        break
                    decompress = zlib.decompressobj(
                            -zlib.MAX_WBITS  # see above
                    )
                    inflated = decompress.decompress(recv_data)
                    inflated += decompress.flush()
                    self.on_recv(inflated.decode())
            #except:
                print("huobi socket error")
                pass

coin_list=[("BTC","USDT")]
thread_ = myThread(coin_list)
thread_.start()
thread_.join()
print("exit")
