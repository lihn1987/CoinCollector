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
    response = url_open('https://api.huobi.pro/v1/common/symbols')
    json_data = json.loads(response)
    if json_data['status']== 'ok':
        for item in json_data['data']:
            db_base.insert_market_base_common(
                item['base-currency'].upper(),
                item['quote-currency'].upper(),
                item['price-precision'],
                item['amount-precision'],
                item['value-precision'],
                (0 if item['state']=='online'else 1),
                item['min-order-amt'],
                item['max-order-amt'],
                item['min-order-value'],
                0
            )
            print(item['min-order-value'])
    else:
        
        print("火币币种获取失败")
    #print(response)
#run()
