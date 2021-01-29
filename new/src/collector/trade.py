from huobi.client.account import AccountClient
from huobi.client.trade import TradeClient
from huobi.constant import *
from huobi.utils import *
import redis
from config import config
import time
import key
import _thread
account_client = AccountClient(api_key=key.ak,
                              secret_key=key.sk)



def Buy(order_coin, base_coin, amount):
    print("buy", order_coin, base_coin, amount)
    trade_client = TradeClient(api_key=key.ak,
                                secret_key=key.sk)
    while True:
        try:
            order_id = trade_client.create_order(
                symbol="%s%s"%(order_coin.lower(), base_coin.lower()), #btc+3
                account_id=213490, 
                client_order_id=None,
                amount=amount, 
                order_type=OrderType.BUY_MARKET,
                price=0,
                source="spot-api")
            while True:
                try:
                    obj = trade_client.get_order(order_id)
                    print(float(obj.filled_amount), float(obj.filled_fees), float(float(amount)/float(obj.filled_amount)))
                    return float(obj.filled_amount), float(obj.filled_fees), float(float(amount)/float(obj.filled_amount))
                except:
                    print("get order error")
                    time.sleep(0.1)
                    pass
        except:
            print("buy error", order_coin, base_coin, amount)
            time.sleep(0.1)
            pass

def Sell(order_coin, base_coin, amount):
    print("Sell", order_coin, base_coin, amount)
    trade_client = TradeClient(api_key=key.ak,
                                secret_key=key.sk)
    while True:
        try:
            order_id = trade_client.create_order(
                symbol="%s%s"%(order_coin.lower(), base_coin.lower()), #btc+3
                account_id=213490, 
                client_order_id=None,
                amount=amount, 
                order_type=OrderType.SELL_MARKET,
                price=0,
                source="spot-api")
            while True:
                try:
                    obj = trade_client.get_order(order_id)
                    return float(obj.filled_cash_amount), float(obj.filled_fees)
                except:
                    print("get order error", order_coin, base_coin, amount)
                    time.sleep(0.1)
                    pass
        except:
            print("sell error")
            time.sleep(0.1)
            pass

def ThreadFunc(order_coin, base_coin, market, period):
    order_coin = order_coin.upper()
    base_coin = base_coin.upper()
    market = market.upper()
    redis_db = redis.Redis(host=config["redis_config"]["host"], port=config["redis_config"]["port"])

    # ==========获取上一次参数
    is_buy = None
    tmp = redis_db.get("HAIGUI-%s-%s-%s-%s-is_buy"%(order_coin, base_coin, market, period))
    if tmp == None:
        is_buy = False
    else:
        is_buy = True if int(tmp) else False

    amount = None
    tmp = redis_db.get("HAIGUI-%s-%s-%s-%s-amount"%(order_coin, base_coin, market, period))
    if tmp == None:
        amount = 100
    else:
        amount = float(tmp)
    
    tmp = redis_db.get("HAIGUI-%s-%s-%s-%s-price"%(order_coin, base_coin, market, period))
    price = float(tmp) if tmp else None
    print("HAIGUI-%s-%s-%s-%s-is_buy"%(order_coin, base_coin, market, period))
    print("当前买卖方向", "买" if not is_buy else "卖")
    print("当前价格", price)
    while True:
        range_width = int(redis_db.get("HAIGUI-%s-%s-%s-%s-best_buy_width_range"%(order_coin, base_coin, market, period)))
        best_buy_point = float(redis_db.get("HAIGUI-%s-%s-%s-%s-best_buy_point"%(order_coin, base_coin, market, period)))
        best_sell_point_high = float(redis_db.get("HAIGUI-%s-%s-%s-%s-best_sell_point_hight"%(order_coin, base_coin, market, period)))
        best_sell_point_low = float(redis_db.get("HAIGUI-%s-%s-%s-%s-best_sell_point_low"%(order_coin, base_coin, market, period)))

        kline_list = json.loads( redis_db.get("%s-%s-%s-%s"%(order_coin, base_coin, period, market)).decode("utf8"))["data"][:range_width]
        if is_buy == False:
            _max = _min = None
            for item in kline_list:
                if not _max or item["high"] > _max:
                    _max = item["high"]
                if not _min or item["low"] < _min:
                    _min = item["low"]
            
            if (_max - _min)*100/_min > best_buy_point and _max == kline_list[0]["high"]:
                is_buy = True
                result = Buy(order_coin, base_coin, amount)
                amount = int((result[0] - result[1])*10000)/10000
                price = result[2]
                redis_db.set("HAIGUI-%s-%s-%s-%s-is_buy"%(order_coin, base_coin, market, period), 1 if is_buy else 0)
                redis_db.set("HAIGUI-%s-%s-%s-%s-amount"%(order_coin, base_coin, market, period), amount)
                redis_db.set("HAIGUI-%s-%s-%s-%s-price"%(order_coin, base_coin, market, period), price)
                print("HAIGUI-%s-%s-%s-%s-is_buy"%(order_coin, base_coin, market, period))

        if is_buy == True:
            _max = _min = None
            for item in kline_list:
                if not _max or item["high"] > _max:
                    _max = item["high"]
                if not _min or item["low"] < _min:
                    _min = item["low"]
            if (_max - price)*100/price > best_sell_point_high and _max == kline_list[0]["high"] or (_max - price)*100/price > best_sell_point_low and _min == kline_list[0]["low"]:
                is_buy = False
                result = Sell(order_coin, base_coin, amount)
                amount = int((result[0] - result[1])*10000)/10000
                redis_db.set("HAIGUI-%s-%s-%s-%s-is_buy"%(order_coin, base_coin, market, period), 1 if is_buy else 0)
                redis_db.set("HAIGUI-%s-%s-%s-%s-amount"%(order_coin, base_coin, market, period), amount)
        #print(kline_list)
        time.sleep(1)

if __name__ == "__main__":
    _thread.start_new_thread ( ThreadFunc, ("btc3s", "usdt", "huobi", "1min"))
    _thread.start_new_thread ( ThreadFunc, ("btc3l", "usdt", "huobi", "1min"))
    while True:
        time.sleep(1)
