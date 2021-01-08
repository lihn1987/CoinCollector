
import json
import threading
import time
import gzip
import websocket
import zlib
import numpy
import sys
import time
from config import config
import redis
def OnChange(depth_info, change_info):
    #修改卖盘
    for_change = change_info['data'][0]['asks']
    for_change.reverse()
    for i in range(len(depth_info["forsell"])-1, -1, -1):
        while True:
            if len(for_change) == 0 :
                break
            if len(for_change) != 0 and depth_info["forsell"][i][0] == for_change[0][0] and for_change[0][1] == '0':
                #需要删除的
                depth_info["forsell"].pop(i)
                for_change.pop(0)
                break

            elif len(for_change) != 0 and depth_info["forsell"][i][0] == for_change[0][0] and for_change[0][1] != '0':
                #需要修改的
                depth_info["forsell"][i][1] = for_change[0][1]
                for_change.pop(0)
                continue
        
            elif len(for_change) != 0 and float(depth_info["forsell"][i][0]) < float(for_change[0][0]):
                depth_info["forsell"].insert(i+1, for_change[0][0:2])
                for_change.pop(0)
                continue

            break
        if len(for_change) == 0 :
            break
        if i == 0:
            for_change.reverse()
            if len(for_change):
                depth_info["forsell"] = numpy.array(for_change)[:,0:2].tolist()+depth_info["forsell"]

    #修改买盘
    for_change = change_info['data'][0]['bids']
    for_change.reverse()
    for i in range(len(depth_info["forbuy"])-1, -1, -1):
        while True:
            if len(for_change) == 0 :
                break
            if len(for_change) != 0 and depth_info["forbuy"][i][0] == for_change[0][0] and for_change[0][1] == '0':
                #需要删除的
                depth_info["forbuy"].pop(i)
                for_change.pop(0)
                break

            elif len(for_change) != 0 and depth_info["forbuy"][i][0] == for_change[0][0] and for_change[0][1] != '0':
                #需要修改的
                depth_info["forbuy"][i][1] = for_change[0][1]
                for_change.pop(0)
                continue
        
            elif len(for_change) != 0 and float(depth_info["forbuy"][i][0]) > float(for_change[0][0]):
                depth_info["forbuy"].insert(i+1, for_change[0][0:2])
                for_change.pop(0)
                continue

            break
            
        if len(for_change) == 0 :
            break
        if i == 0:
            for_change.reverse()
            if len(for_change):
                depth_info["forbuy"] = numpy.array(for_change)[:,0:2].tolist()+depth_info["forbuy"]
    #depth_info.dump()


    
class myThread (threading.Thread):
    def __init__(self, coin_list):
        threading.Thread.__init__(self)
        self.coin_list = coin_list
        self.coin_dict = {}
        self.ws = websocket.WebSocket()
        self.timer = None
        self.info = {}
        self.redis_db = redis.Redis(host=config["redis_config"]["host"], port=config["redis_config"]["port"])
        for coin in coin_list:
            self.info[tuple(coin)] = {}
    def connect(self):
        print("start connect")
        if config["proxy_config"]["proxy_use"]:
            self.ws.connect("wss://real.okex.com:8443/ws/v3", http_proxy_host=config["proxy_config"]["proxy_ip"], http_proxy_port=config["proxy_config"]["proxy_port"])
        else:
            self.ws.connect("wss://real.okex.com:8443/ws/v3")
        print("end connect")

    def on_recv(self, str):
        
        self.reset_timer()
        json_data = json.loads(str)
        if 'event' not in json_data and json_data['action'] == 'partial':
            order_coin = json_data['data'][0]['instrument_id'].split("-")[0]
            base_coin = json_data['data'][0]['instrument_id'].split("-")[1]

            info = self.info[(order_coin,base_coin)]
            info["forbuy"] = numpy.array(json_data['data'][0]['bids'])[:,0:2].tolist()
            info["forsell"] = numpy.array(json_data['data'][0]['asks'])[:,0:2].tolist()

            d = time.strptime(json_data['data'][0]['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ")
            timeStamp = (time.mktime(d))+8*60*60
            info["up_time"] = timeStamp*1000
            info["market"] = 1
            info["delay"] = time_now-timeStamp*1000
            k = order_coin+"-"+base_coin+"-OK-DEPTH"
            v = json.dumps(info)
            self.redis_db.set(k, v)

        elif 'event' not in json_data and json_data['action'] == 'update':
            order_coin = json_data['data'][0]['instrument_id'].split("-")[0]
            base_coin = json_data['data'][0]['instrument_id'].split("-")[1]

            info = self.info[(order_coin, base_coin)]
            OnChange(info, json_data)
            d = time.strptime(json_data['data'][0]['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ")
            timeStamp = (time.mktime(d))+8*60*60
            info["up_time"] = timeStamp*1000
            k = info["order_coin"]+"-"+info["base_coin"]+"-OK-DEPTH"
            v = json.dumps(info)
            self.redis_db.set(k, v)
            

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
        if self.timer and self.timer.is_alive():
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

def StartCrwal(coin_list):
    thread_ = myThread(coin_list)
    thread_.start()
'''
StartCrwal()
while True:
    time.sleep(1)
'''
#python3 depth_huobi.py BTC-USDT,ETH-USDT
#python3 depth_ok.py SKM-USDT,SUN-USDT,CKB-USDT,CNNS-USDT,OGO-USDT,ETH-USDT,FTT-USDT,DHT-USDT,VEN-USDT,XMX-USDT,BAL-USDT,ALGO-USDT,LRC-USDT,TNB-USDT,HB10-USDT,LOOM-USDT,BCHA-USDT,GRT-USDT,ELF-USDT,SOL-USDT,NEW-USDT,UTK-USDT,SNX-USDT,LBA-USDT,ACT-USDT,HPT-USDT,CTXC-USDT,OXT-USDT,AVAX-USDT,HC-USDT,VSYS-USDT,DOT-USDT,MXC-USDT,FSN-USDT,YAMV2-USDT,NAS-USDT,XMR-USDT,FIL3S-USDT,BTM-USDT,WXT-USDT,FIL-USDT,FOR-USDT,GLM-USDT,XTZ-USDT,WTC-USDT,LTC3S-USDT,CRE-USDT,HT-USDT,ZRX-USDT,KCASH-USDT,YEE-USDT,SUSHI-USDT,LAMB-USDT,VET-USDT,HOT-USDT,UNI2L-USDT,DAI-USDT,REN-USDT,DOGE-USDT,ANKR-USDT,BCH3L-USDT,NBS-USDT,EKT-USDT,SKL-USDT,SMT-USDT,ELA-USDT,KSM-USDT,ABT-USDT,HIVE-USDT,TITAN-USDT,NEST-USDT,KAVA-USDT,DF-USDT,ETH3L-USDT,BTC3L-USDT,PHA-USDT,EM-USDT,LTC3L-USDT,SWFTC-USDT,PAI-USDT,WICC-USDT,CMT-USDT,VIDY-USDT,ZEC3L-USDT,DCR-USDT,IRIS-USDT,NHBTC-USDT,NKN-USDT,PEARL-USDT,CRV-USDT,OGN-USDT,ADA-USDT,BSV3S-USDT,ATP-USDT,FRONT-USDT,MTA-USDT,STEEM-USDT,HIT-USDT,WAXP-USDT,CVP-USDT,UNI2S-USDT,VALUE-USDT,LOL-USDT,AE-USDT,UNI-USDT,YFII-USDT,JST-USDT,ACH-USDT,OMG-USDT,ICX-USDT,MX-USDT,MKR-USDT,NANO-USDT,UMA-USDT,BNT-USDT,HBC-USDT,RSR-USDT,BCH3S-USDT,CVC-USDT,BSV3L-USDT,DAC-USDT,BTC3S-USDT,WOO-USDT,CHR-USDT,FTI-USDT,XRP3L-USDT,STORJ-USDT,DOT2L-USDT,ITC-USDT,LINK-USDT,EGT-USDT,ZIL-USDT,KNC-USDT,AKRO-USDT,LINK3L-USDT,ETH3S-USDT,GT-USDT,TT-USDT,BAND-USDT,XRP3S-USDT,NEXO-USDT,MCO-USDT,ETH1S-USDT,EOS3S-USDT,EOS-USDT,GNX-USDT,ETC-USDT,POND-USDT,XRT-USDT,WAVES-USDT,SOC-USDT,SNT-USDT,IOST-USDT,API3-USDT,BTC-USDT,ANT-USDT,DOT2S-USDT,EOS3L-USDT,TRB-USDT,SWRV-USDT,FIS-USDT,BTC1S-USDT,GXC-USDT,CHZ-USDT,OCN-USDT,TRX-USDT,AAC-USDT,YFI-USDT,THETA-USDT,CRO-USDT,BLZ-USDT,WNXM-USDT,XLM-USDT,IOTA-USDT,RUFF-USDT,FIL3L-USDT,1INCH-USDT,BETH-USDT,COMP-USDT,BOT-USDT,BHD-USDT,TOP-USDT,PVT-USDT,LUNA-USDT,RING-USDT,SEELE-USDT,ZEC-USDT,NULS-USDT,AST-USDT,ONT-USDT,QTUM-USDT,DTA-USDT,LXT-USDT,DOCK-USDT,UUU-USDT,XEM-USDT,HBAR-USDT,STPT-USDT,FIRO-USDT,BAT-USDT,NEAR-USDT,GOF-USDT,RVN-USDT,SAND-USDT,UIP-USDT,DASH-USDT,BTT-USDT,NSURE-USDT,KAN-USDT,AR-USDT,BIX-USDT,BSV-USDT,ZEC3S-USDT,ONE-USDT,ARPA-USDT,LET-USDT,LEND-USDT,NEO-USDT,AAVE-USDT,ATOM-USDT,XRP-USDT,MDS-USDT,NODE-USDT,MANA-USDT,LINK3S-USDT,LTC-USDT,BCH-USDT,CRU-USDT,DKA-USDT,MLN-USDT,BTS-USDT
if __name__ == "__main__":
    arg1 = sys.argv[1]
    coin_list = []
    coin_pair_list = arg1.split(",")
    for item in coin_pair_list:
        coin_list.append(item.split("-"))
    StartCrwal(coin_list)
    while True:
        time.sleep(1)