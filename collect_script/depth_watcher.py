
import json
import threading
import time
import mysql.connector
import gzip
import websocket
import redis
import pickle

redis_db = redis.Redis(host='localhost', port=6379)
while True:
    str_out=''
    obj = pickle.loads(redis_db.get('0_BTC_USDT'))
    str_out += "ch:"+obj['ch'].split(".")[1]+"\r\n"
    str_out+="time:"+str(obj['ts'])+"\r\n"
    str_out+='卖:'+"\r\n"
    for item in reversed(obj['tick']['asks'][0:10]):
        str_out+=str(item)+"\r\n"
    str_out+='买:'+"\r\n"
    for item in obj['tick']['bids'][0:10]:
        str_out+=str(item)+"\r\n"
    print(str_out)