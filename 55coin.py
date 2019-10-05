import urllib.request
import json
import _thread
import threading
import time
import mysql.connector
from pyquery import PyQuery as pq

class article_info:
    def __init__(self, author, time_utc, title, desc, content, source_addr, source_media):
        self.author = author
        self.time_utc = time_utc
        self.title = title
        self.desc = desc
        self.content = content
        self.source_addr = source_addr
        self.source_media = source_media
    def __str__(self):
        return("""==========================
author:%s
time_utc:%d
title:%s
desc:%s
content:%s
source_addr:%s
source_media:%s"""%(self.author, self.time_utc, self.title, self.desc, 'self.content', self.source_addr, self.source_media))

def url_open(url):
    print(url)
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}  
    req = urllib.request.Request(url=url, headers=headers)
    for i in range(10):
        try:
            response = urllib.request.urlopen(url=req, timeout=5).read().decode('utf-8')
            return response
        except Exception as e:
            print("chainnewscrawl except:".str(e))

def get_news(page_count):
    time_utc = int(time.time())
    for i in range(1,page_count+1):
        response = url_open("https://www.55coin.com/index/article/search.html?cat_id=4&page=%d&is_index=1"%(i))
        #print(response)
        json_data = json.loads(response)
        for item in json_data['list']:
            article_item = article_info(
                item['nickname'], 
                int(item["add_time"]), 
                item['title'], 
                item['brief'],
                'content', 
                'https://www.55coin.com/article/%d.html'%item['article_id'], 
                "区势传媒")
            source_responce = url_open(article_item.source_addr)
            source_doc = pq(source_responce)
            article_item.content = source_doc(".article-content").html()
            print(article_item)
        #print(json_data['results'][0])

get_news(1)
#def get_news(10)

#print(response)