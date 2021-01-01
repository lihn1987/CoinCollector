
import json
import threading
import time
import gzip
import websocket
from config import config
import sys
import redis

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
            deep_info["order_coin"] = self.coin_dict[json_data['ch'].split(".")[1].upper()][0]
            deep_info["base_coin"] = self.coin_dict[json_data['ch'].split(".")[1].upper()][1]
            deep_info["forbuy"] = json_data['tick']['bids']
            deep_info["forsell"] = json_data['tick']['asks']
            deep_info["market"] = 0
            deep_info["delay"] = (time_now-deep_info["up_time"])
            #保存到redis
            k = deep_info["order_coin"]+"-"+deep_info["base_coin"]+"-HUOBI"
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

#python3 depth_huobi.py BTC-USDT,ETH-USDT
#python3 depth_huobi.py SKM-USDT,SUN-USDT,CKB-USDT,CNNS-USDT,OGO-USDT,ETH-USDT,FTT-USDT,DHT-USDT,VEN-USDT,XMX-USDT,BAL-USDT,ALGO-USDT,LRC-USDT,TNB-USDT,HB10-USDT,LOOM-USDT,BCHA-USDT,GRT-USDT,ELF-USDT,SOL-USDT,NEW-USDT,UTK-USDT,SNX-USDT,LBA-USDT,ACT-USDT,HPT-USDT,CTXC-USDT,OXT-USDT,AVAX-USDT,HC-USDT,VSYS-USDT,DOT-USDT,MXC-USDT,FSN-USDT,YAMV2-USDT,NAS-USDT,XMR-USDT,FIL3S-USDT,BTM-USDT,WXT-USDT,FIL-USDT,FOR-USDT,GLM-USDT,XTZ-USDT,WTC-USDT,LTC3S-USDT,CRE-USDT,HT-USDT,ZRX-USDT,KCASH-USDT,YEE-USDT,SUSHI-USDT,LAMB-USDT,VET-USDT,HOT-USDT,UNI2L-USDT,DAI-USDT,REN-USDT,DOGE-USDT,ANKR-USDT,BCH3L-USDT,NBS-USDT,EKT-USDT,SKL-USDT,SMT-USDT,ELA-USDT,KSM-USDT,ABT-USDT,HIVE-USDT,TITAN-USDT,NEST-USDT,KAVA-USDT,DF-USDT,ETH3L-USDT,BTC3L-USDT,PHA-USDT,EM-USDT,LTC3L-USDT,SWFTC-USDT,PAI-USDT,WICC-USDT,CMT-USDT,VIDY-USDT,ZEC3L-USDT,DCR-USDT,IRIS-USDT,NHBTC-USDT,NKN-USDT,PEARL-USDT,CRV-USDT,OGN-USDT,ADA-USDT,BSV3S-USDT,ATP-USDT,FRONT-USDT,MTA-USDT,STEEM-USDT,HIT-USDT,WAXP-USDT,CVP-USDT,UNI2S-USDT,VALUE-USDT,LOL-USDT,AE-USDT,UNI-USDT,YFII-USDT,JST-USDT,ACH-USDT,OMG-USDT,ICX-USDT,MX-USDT,MKR-USDT,NANO-USDT,UMA-USDT,BNT-USDT,HBC-USDT,RSR-USDT,BCH3S-USDT,CVC-USDT,BSV3L-USDT,DAC-USDT,BTC3S-USDT,WOO-USDT,CHR-USDT,FTI-USDT,XRP3L-USDT,STORJ-USDT,DOT2L-USDT,ITC-USDT,LINK-USDT,EGT-USDT,ZIL-USDT,KNC-USDT,AKRO-USDT,LINK3L-USDT,ETH3S-USDT,GT-USDT,TT-USDT,BAND-USDT,XRP3S-USDT,NEXO-USDT,MCO-USDT,ETH1S-USDT,EOS3S-USDT,EOS-USDT,GNX-USDT,ETC-USDT,POND-USDT,XRT-USDT,WAVES-USDT,SOC-USDT,SNT-USDT,IOST-USDT,API3-USDT,BTC-USDT,ANT-USDT,DOT2S-USDT,EOS3L-USDT,TRB-USDT,SWRV-USDT,FIS-USDT,BTC1S-USDT,GXC-USDT,CHZ-USDT,OCN-USDT,TRX-USDT,AAC-USDT,YFI-USDT,THETA-USDT,CRO-USDT,BLZ-USDT,WNXM-USDT,XLM-USDT,IOTA-USDT,RUFF-USDT,FIL3L-USDT,1INCH-USDT,BETH-USDT,COMP-USDT,BOT-USDT,BHD-USDT,TOP-USDT,PVT-USDT,LUNA-USDT,RING-USDT,SEELE-USDT,ZEC-USDT,NULS-USDT,AST-USDT,ONT-USDT,QTUM-USDT,DTA-USDT,LXT-USDT,DOCK-USDT,UUU-USDT,XEM-USDT,HBAR-USDT,STPT-USDT,FIRO-USDT,BAT-USDT,NEAR-USDT,GOF-USDT,RVN-USDT,SAND-USDT,UIP-USDT,DASH-USDT,BTT-USDT,NSURE-USDT,KAN-USDT,AR-USDT,BIX-USDT,BSV-USDT,ZEC3S-USDT,ONE-USDT,ARPA-USDT,LET-USDT,LEND-USDT,NEO-USDT,AAVE-USDT,ATOM-USDT,XRP-USDT,MDS-USDT,NODE-USDT,MANA-USDT,LINK3S-USDT,LTC-USDT,BCH-USDT,CRU-USDT,DKA-USDT,MLN-USDT,BTS-USDT
if __name__ == "__main__":
    arg1 = sys.argv[1]
    coin_list = []
    coin_pair_list = arg1.split(",")
    for item in coin_pair_list:
        coin_list.append(item.split("-"))
    print(coin_list)
    StartCrwal(coin_list)
    while True:
        time.sleep(1)
