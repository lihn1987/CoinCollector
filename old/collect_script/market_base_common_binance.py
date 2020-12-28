import urllib.request
import json
import _thread
import threading
import time
import mysql.connector
from pyquery import PyQuery as pq
import db_base
db_base.init_db()
def url_open(url):
    #print(url)
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}  
    req = urllib.request.Request(url=url, headers=headers)
    for i in range(10):
        try:
            response = urllib.request.urlopen(url=req, timeout=5).read().decode('utf-8')
            return response
        except :
            print("chainnewscrawl except:")
def run():
    response = url_open('https://api.binance.com/api/v3/exchangeInfo')
    json_data = json.loads(response)
    for item in json_data['symbols']:
        for filter_item in item['filters']:
            if filter_item['filterType']=='PRICE_FILTER':
                db_base.insert_market_base_common(
                    item['baseAsset'].upper(),
                    item['quoteAsset'].upper(),
                    item['quotePrecision'],
                    item['baseCommissionPrecision'],
                    item['quoteCommissionPrecision'],
                    (0 if item['status']=='TRADING'else 1),
                    float(filter_item['minPrice']),
                    float(filter_item['maxPrice']),
                    float(filter_item['tickSize']),
                    1
                )
                break

    #print(response)
#run()
