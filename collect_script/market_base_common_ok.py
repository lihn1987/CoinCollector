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
    response = url_open('https://www.okex.com/api/spot/v3/instruments')
    json_data = json.loads(response)
    for item in json_data:
        db_base.insert_market_base_common(
            item['base_currency'].upper(),
            item['quote_currency'].upper(),
            item['tick_size'].find('.'),
            item['size_increment'].find('.'),
            0,
            0 ,
            float(item['min_size']),
            float(10^20),
            float(0),
            2
        )

#run()
