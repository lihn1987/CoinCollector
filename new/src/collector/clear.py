from huobi.client.account import AccountClient
from huobi.client.trade import TradeClient
from huobi.constant import *
from huobi.utils import *
import redis
from config import config
import time
import key
import _thread

if __name__ == "__main__":

    redis_db = redis.Redis(host=config["redis_config"]["host"], port=config["redis_config"]["port"])
    redis_db.delete("HAIGUI-BTC3S-USDT-HUOBI-1min-is_buy")
    redis_db.delete("HAIGUI-BTC3S-USDT-HUOBI-1min-amount")
    redis_db.delete("HAIGUI-BTC3L-USDT-HUOBI-1min-is_buy")
    redis_db.delete("HAIGUI-BTC3L-USDT-HUOBI-1min-amount")
    redis_db.delete("HAIGUI-BTC3S-USDT-HUOBI-1min-price")
    redis_db.delete("HAIGUI-BTC3L-USDT-HUOBI-1min-price")
