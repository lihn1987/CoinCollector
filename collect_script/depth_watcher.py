
import json
import threading
import time
import mysql.connector
import gzip
import websocket
import redis
import pickle
from depth_info import DepthInfo

def run(market, order_coin, base_coin):
    redis_db = redis.Redis(host='localhost', port=6379)
    while True:
        str_out=''
        obj = pickle.loads(redis_db.get(str(market)+'_'+order_coin.upper()+'_'+base_coin.upper()))
        str_out += obj.order_coin+"\r\n"
        str_out += obj.base_coin+"\r\n"
        str_out+="time:"+str(obj.up_time)+"\r\n"
        str_out+='卖:'+"\r\n"
        for item in reversed(obj.forsell[0:10]):
            str_out+=str(item)+"\r\n"
        str_out+='买:'+"\r\n"
        for item in obj.forbuy[0:10]:
            str_out+=str(item)+"\r\n"
        print(str_out)
        time.sleep(0.1)
import sys
run(int(sys.argv[1]), sys.argv[2], sys.argv[3])