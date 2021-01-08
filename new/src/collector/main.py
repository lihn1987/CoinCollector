import huobi_info
import ok_info
import redis
import json

from multiprocessing import Process
from config import config
def process_huobi(coin_list):
    print("process_huobi", coin_list)
    huobi_info.StartCrwal(coin_list)

def process_ok(coin_list):
    ok_info.StartCrwal(coin_list)

if __name__ == "__main__":
    redis_db = redis.Redis(host=config["redis_config"]["host"], port=config["redis_config"]["port"])
    #若没设置，初始化只看BTC和ETH
    if redis_db.get("HUOBI-CONFIG") == None or redis_db.get("OK-CONFIG") == None:
        redis_db.set("HUOBI-CONFIG", '[["BTC", "USDT"], ["ETH", "USDT"]]')
        redis_db.set("OK-CONFIG", '["BTC-USDT", "ETH-USDT"]')
    
    huobi_coin_list = json.loads(redis_db.get("HUOBI-CONFIG"))
    ok_coin_list = json.loads(redis_db.get("OK-CONFIG"))

    print(huobi_coin_list)
    print(ok_coin_list)
    for i in range(0, len(huobi_coin_list), 8):
        p = Process(target=process_huobi, args=(huobi_coin_list[i: i+8 if i+8 < len(huobi_coin_list) else len(huobi_coin_list)],))
        p.start() 

    # for i in range(0, len(ok_coin_list), 8):
    #     p = Process(target=process_ok, args=(ok_coin_list[i: i+8 if i+8 < len(ok_coin_list) else len(ok_coin_list) - 1],))
    #     p.start() 
