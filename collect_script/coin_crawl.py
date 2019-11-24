import urllib.request
import json
import _thread
import threading
import time
import mysql.connector
from pyquery import PyQuery as pq
import sys
import db_base  

def append_coin_info_2_db(coin_info):
    db_base.insert_coin_info(
        coin_info.index, 
        coin_info.name, 
        coin_info.name_en, 
        coin_info.name_cn, 
        coin_info.official_website, 
        coin_info.description)

class coin_info:
    index = 0
    name = ''
    name_en = ''
    name_cn = ''
    price_now = 0.0
    description = ''

    def __init__(self, index = 0, name = '', name_en = '', name_cn = '', price_now = 0.0, count = 0.0):
        self.index = int(index)
        self.name = name
        self.name_en = name_en
        self.name_cn = name_cn
        self.price_now = 0.0 if (price_now=='') else float(price_now)
        self.count = 0.0 if (count=='') else float(count)
        self.official_website = ''
        self.description = ''
    def print(self):
        print("index:%05d  full name:%28s  english name:%8s  chinese name:%8s  price now:%f\ndiscription:%s" %(self.index , self.name ,self.name_en ,self.name_cn ,self.price_now, self.description))
        print("website:%40s"%(self.official_website))

def url_open(url):
    while True:
        try:
            response = urllib.request.urlopen(url, timeout=3)
            return response
        except:
            print("url:%s open errer retry"%(url))

def get_basic_info(page_size = 100, page_start = 0, page_count = 1):
    for page_idx in range(page_start, page_start+page_count):
        url = "https://h5-market.niuyan.com/web/v3/coin/list?pagesize="+str(page_size)+"&offset="+str(page_size*page_idx)+"&lan=zh-cn"
        response = url_open(url)
        print(url)
        if response.status ==200:
            print('get_basic_info success!')
        else:
            print('get_basic_info faild!')
            return
        #print(response.read().decode('utf-8'))
        json_data = json.loads(response.read().decode('utf-8'))
        #print(json_data)
        info = json_data['data']['data']
        #print(info)
        for i in range(0, len(json_data['data']['data'])):
            coin = coin_info(info[i][2], info[i][0], info[i][1], info[i][4], info[i][5], info[i][7])
            coin.official_website,coin.description = get_official_website_and_description(coin.name)
            append_coin_info_2_db(coin)
            

#通过coin_name拼接网址，获取官方网站
def get_official_website_and_description(coin_name):
    url ="https://h5-market.niuyan.com/web/v3/coin/intro?coin_id="+coin_name+"&lan=zh-cn"
    response = url_open(url)
    json_data = json.loads(response.read().decode('utf-8'))
    web=""
    des=""
    if json_data["code"] == 0:
        des = json_data["data"]["intro"]
        if json_data["data"]["official_website"]:
            web = json_data["data"]["official_website"][0]
    return web,des


#get_basic_info(page_size = 100, page_start = 0, page_count = 1):
class myThread (threading.Thread):
    page_size = 0
    page_start = 0
    page_end = 0
    def __init__(self, page_size, page_start, page_count):
        threading.Thread.__init__(self)
        self.page_size = page_size
        self.page_count = page_count
        self.page_start = page_start
    def run(self):
        print("thread start",self.page_start)
        get_basic_info(self.page_size, self.page_start, self.page_count)
        print("thread end",self.page_start)

def StartCrawl(thread_count,page_count):
    start_time = time.time()
    will_crawl = list(range( page_count))
    #print(will_crawl);return
    thread_list = []
    for i in range(thread_count):
        if i >= page_count:
            break
        thread_list.append(myThread(50, i, 1))
        thread_list[i].start()
        will_crawl.pop(0)

    while True:
        #print(will_crawl,thread_list[0].is_alive())
        if not len(will_crawl):
            for thread_item in thread_list:
                thread_item.join()
            break
        for i in range(len(thread_list)):
            if thread_list[i].is_alive() == False:
                thread_list[i] = myThread(50, will_crawl.pop(0), 1)
                thread_list[i].start()
        time.sleep(1)
    print("over")
    print("time:", time.time()-start_time)

#print(get_description("bitcoin"))
db_base.init_db()
StartCrawl(8, 72)
#get_official_website("bitcoin")

