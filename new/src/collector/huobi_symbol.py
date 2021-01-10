
import json
import threading
import time
import urllib.request
import redis
from config import config

class myThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        pass
    def run(self):
        while True:
            try:
                headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
                request = urllib.request.Request(url = 'https://api.huobi.pro/v1/common/symbols', headers = headers)
                response = urllib.request.urlopen(request)
                json_obj = json.loads(response.read().decode('utf-8'))
                for item in json_obj["data"]:
                    for_save = {
                        "base-coin": item["quote-currency"].upper(),
                        "order-coin": item["base-currency"].upper(),
                        "price-precision": item["price-precision"],
                        "amount-precision": item["amount-precision"],
                        "symbol-partition": 1 if item["symbol-partition"] == "main" else 2,
                        "symbol": item["symbol"],
                        "state": 1 if item["state"] == "online" else 0,
                        "value-precision": item["value-precision"],
                        "limit-order-min-order-amt": item["limit-order-min-order-amt"],
                        "limit-order-max-order-amt": item["limit-order-max-order-amt"],
                        "sell-market-min-order-amt": item["sell-market-min-order-amt"],
                        "sell-market-max-order-amt": item["sell-market-max-order-amt"],
                        "buy-market-max-order-value": item["buy-market-max-order-value"],
                        "min-order-value": item["min-order-value"],
                    }
                    #print(config["redis_config"]["host"], config["redis_config"]["port"])
                    redis_db = redis.Redis(host=config["redis_config"]["host"], port=config["redis_config"]["port"])
                    for k, v in for_save.items():
                        db_key = for_save["order-coin"].upper()+"_"+for_save["base-coin"]+"-"+"HUOBI-"+k
                        redis_db.set(db_key, v)
                print("Flush complate")
                time.sleep(10)
            except Exception as e:
                print("huobi symbol error:", e)
                time.sleep(10)
                pass

#coin_list=[("BTC", "USDT"),("ETH", "USDT"),]

def StartCrwal():
    thread_ = myThread()
    thread_.start()

if __name__ == "__main__":
    StartCrwal()
    while True:
        time.sleep(1)
