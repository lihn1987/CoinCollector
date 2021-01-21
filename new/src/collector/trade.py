from huobi.client.account import AccountClient
from huobi.client.trade import TradeClient
from huobi.constant import *
from huobi.utils import *
import redis
from config import config
import time
import key
account_client = AccountClient(api_key=key.ak,
                              secret_key=key.sk)

if __name__ == "__main__":
    """
    #首先获取要监控的账户
    redis_db = redis.Redis(host=config["redis_config"]["host"], port=config["redis_config"]["port"])
    # 若没设置，初始化只看BTC和ETH
    if redis_db.get("HUOBI-CONFIG") == None or redis_db.get("OK-CONFIG") == None:
        redis_db.set("HUOBI-CONFIG", '[["BTC", "USDT"], ["ETH", "USDT"]]')
        redis_db.set("OK-CONFIG", '["BTC-USDT", "ETH-USDT"]')
    while True:
        coin_list = json.loads(redis_db.get("HUOBI-CONFIG"))
        balance_list = []
        for item in coin_list:
            balance_list.append(item[0].lower())
        balance_list.append("usdt")
        #首先刷新账户
        while True:
            try:
                list_obj = account_client.get_balance(213490)
                for item in list_obj:
                    if (item.currency in balance_list) and item.type=="trade":
                        redis_db.set(item.currency.upper()+"-HUOBI-BALANCE", str(item.balance))
                break
            except:
                print("error")

        time.sleep(1)
    """
    trade_client = TradeClient(api_key=key.ak,
                              secret_key=key.sk)
    order_id = trade_client.create_order(
        symbol="btc3lusdt", #btc+3
        account_id=213490, 
        client_order_id=1234567,
        amount=100, 
        order_type=OrderType.BUY_MARKET,
        price=0,
        source="spot-api")
    print(order_id)