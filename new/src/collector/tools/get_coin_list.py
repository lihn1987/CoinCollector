import urllib.request
import json

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
request = urllib.request.Request(url = 'https://api.huobi.pro/market/tickers', headers = headers)
response = urllib.request.urlopen(request)
json_obj = json.loads(response.read().decode('utf-8'))
print("普通交易")
# 筛选usdt，btc结尾的币种
all_items = []
eth_price = 0.0
btc_price = 0.0
for item in json_obj["data"]:
    """
    if item["symbol"].endswith("usdt"):
        usdt_items.append(item)
    elif item["symbol"].endswith("eth"):
        eth_items.append(item)
    elif item["symbol"].endswith("btc"):
        btc_items.append(item)
    """
    if item["symbol"].endswith("usdt") :
        all_items.append(item)
    if item["symbol"] == "btcusdt":
        btc_price = item["close"]
    elif item["symbol"] == "ethusdt":
        eth_price = item["close"]


def takeSatistic(item):
    return item["amount"]

all_items.sort(key=takeSatistic)   

# 计算最终币种
coin_list = []
#1000000000
for item in all_items:
    if item["amount"] > 100000  and (item["ask"] - item["bid"])/item["bid"] < 0.02:
        coin_list.append(item)

format_list = []
for item in coin_list:
    format_list.append([item["symbol"][:-4], item["symbol"][-4:]])

print(len(format_list))
print(format_list)

print("合约")
request = urllib.request.Request(url = 'https://api.hbdm.com/linear-swap-api/v1/swap_contract_info', headers = headers)
response = urllib.request.urlopen(request)
json_obj = json.loads(response.read().decode('utf-8'))
print(json_obj)