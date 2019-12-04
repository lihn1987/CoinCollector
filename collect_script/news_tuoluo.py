import urllib.request
import json
import _thread
import threading
import time
import mysql.connector
from pyquery import PyQuery as pq
import news_base

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

def get_news(page_count,cb):
    error_count = 0
    latest_id = ''
    #for i in range(1,page_count+1):
    for i in range(page_count):
        response = url_open("https://www.tuoluocaijing.cn/api/kuaixun/v2/get_list?limit=20&markedred=0&class_id=&last_kxid=%s"%(latest_id))
        #print(response)
        json_data = json.loads(response)
        for item in json_data["data"]["list"]:
            print(item["title"])
            #author, time_utc, title, desc, content, source_addr, source_media
            article_item = news_base.article_info("陀螺快讯", int(item["timeStamp"]), item['title'], item['content'], item['content'], 'https://www.tuoluocaijing.cn/kuaixun/detail-%s.html'%str(item['s_id']), "陀螺财经")
            latest_id = str(item['s_id'])
            if not cb(article_item):
                error_count+=1
            else:
                error_count = 0
            if error_count >= 5:
                break
        if error_count >= 5:
            print("err break")
            break

#get_news(10,None)

#print(response)