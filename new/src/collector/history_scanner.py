
import json
import threading
import time

from config import config
import sys
import redis
import urllib.request

import key_main
import key_sub1
import hashlib
import hmac
import base64
import datetime

import io
import mysql_tools

def Post(key, path, args, show_log = False):
    while True:
        host = "api.hbdm.com"
        method =  "POST"
        time_str = datetime.datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%M:%S')
        
        sign_args = [
            "AccessKeyId=%s"%urllib.parse.quote(key.ak),
            "SignatureMethod=HmacSHA256",
            "SignatureVersion=2",
            "Timestamp="+urllib.parse.quote(time_str)
        ]
        
        sign_args_str = ""
        for item in sign_args:
            sign_args_str += item+"&"
        sign_args_str = sign_args_str[:-1]

        payload0 = '%s\n%s\n%s\n%s' % (method, host, path, sign_args_str)
        dig = hmac.new(key.sk.encode('utf-8'), msg=payload0.encode('utf-8'), digestmod=hashlib.sha256).digest()
        # 进行base64编码
        signature = base64.b64encode(dig).decode()
    
        try:
            headers = {'Content-Type':'application/json'}
            url = ("https://%s%s?"%(host, path))+\
                  ("AccessKeyId=%s"%key.ak)+\
                  ("&Signature=%s"%urllib.parse.quote(signature))+\
                  "&SignatureMethod=HmacSHA256"+\
                  "&SignatureVersion=2"+\
                  ("&Timestamp=%s"%time_str)
                  
            request = urllib.request.Request(
                url = url, 
                headers = headers, 
                data = json.dumps(args).encode("utf-8"), 
                method = 'POST'
            )
            response = urllib.request.urlopen(request, timeout=5)
            json_obj = json.loads(response.read().decode('utf-8'))
            #print(json_obj)
            if "status" in json_obj and json_obj["status"] == "error" and json_obj["err_code"]!= 1051:
                print(json_obj)
                print("Post error, continue")
                continue
            if "data" in json_obj and "errors" in json_obj["data"] and len(json_obj["data"]["errors"]) != 0:
                print(json_obj)
                print("Post error, continue")
                continue
            if show_log:
                print(json_obj)
            return json_obj
        except Exception as e:
            print("huobi symbol error:", e)
            pass


"""
trade_type: 3 buy, 4 sell
"""
def UpdateHistory(key, tag, coin_name, trade_type):
    print("start update %s"%(coin_name))
    count = 0
    try:
        page_size = 0
        args = {
            "contract_code":"%s-USDT"%(coin_name,),
            "trade_type": trade_type,
            "create_date":7,
            "page_index":1,
            "page_size":50
        }
        res = Post(key, "/linear-swap-api/v1/swap_cross_matchresults", args, False)
        if res["status"] == "ok":
            db = mysql_tools.GetDB()
            db_cursor = db.cursor()
            for trade_item in res["data"]["trades"]:
                db_cursor.execute("insert into trade_history values('%s','%s','%s','%s', %d, %0.4f,%0.4f,%0.4f,%d)"%\
                    (trade_item["id"], tag, coin_item, "USDT", trade_type, trade_item["real_profit"],trade_item["trade_turnover"], trade_item["trade_fee"], trade_item["create_date"]))
                count += 1
                db.commit()
            db_cursor.close()
            db.close()
    except Exception as e:
        print(e)

    print("end update %s:%d"%(coin_name, count))

def UpdateNow(key, tag, coin_name,):
    print("start update %s"%(coin_name))
    count = 0
    try:
        page_size = 0
        args = {
            "contract_code":"%s-USDT"%(coin_name,)
        }
        res = Post(key, "/linear-swap-api/v1/swap_cross_position_info", args, False)
        db = mysql_tools.GetDB()
        db_cursor = db.cursor()
        db_cursor.execute("delete from trade_now where tag='%s' and coin_order='%s'"%(tag, coin_name))
        if res["status"] == "ok" and len(res["data"]) != 0:
            print("===================insert")
            db_cursor.execute("insert into trade_now values('%s','%s','%s', '%s', %0.4f,%0.4f,%0.4f)"%\
                (tag, coin_item, "USDT", res["data"][0]["direction"], res["data"][0]["profit"],res["data"][0]["profit_rate"],res["data"][0]["position_margin"]))
        else:
            print("===================delete")
        db.commit()
        db_cursor.close()
        db.close()
        
            
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main_coin = ["ETH", "DOGE", "XRP", "ZEC", "ALGO", "LINK","DOT","SNX","NEO"]
    sub1_coin = ["ETH", "DOGE", "XRP", "ZEC", "ALGO", "LINK","DOT","SNX","NEO"]
    while True:
        for coin_item in main_coin:
            #买入平空
            UpdateHistory(key_main.key, "huobi_1", coin_item, 3)
            UpdateHistory(key_main.key, "huobi_1", coin_item, 4)
            UpdateNow(key_main.key, "huobi_1", coin_item)
            #time.sleep(1)

        for coin_item in sub1_coin:
            #买入平空
            UpdateHistory(key_sub1.key, "huobi_2", coin_item, 3)
            UpdateHistory(key_sub1.key, "huobi_2", coin_item, 4)
            UpdateNow(key_sub1.key, "huobi_2", coin_item)
            #time.sleep(1)
