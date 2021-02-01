
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
                request = urllib.request.Request(url = 'https://api.hbdm.com/linear-swap-api/v1/swap_contract_info', headers = headers)
                response = urllib.request.urlopen(request)
                json_obj = json.loads(response.read().decode('utf-8'))
                for item in json_obj["data"]:
                    for_save = {
                        "base-coin": "USDT",
                        "order-coin": item["symbol"].upper(),
                        "contract_code": item["contract_code"],
                        "contract_size": item["contract_size"],
                        "price_tick":item["price_tick"],
                    }
                    #print(config["redis_config"]["host"], config["redis_config"]["port"])
                    redis_db = redis.Redis(host=config["redis_config"]["host"], port=config["redis_config"]["port"])
                    for k, v in for_save.items():
                        db_key = for_save["order-coin"].upper()+"_"+for_save["base-coin"]+"-"+"HUOBI_CONTRACT-"+k
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
