import urllib.request
import json
import _thread
import threading
import time
import mysql.connector
from pyquery import PyQuery as pq

class article_info:
    def __init__(self, author, time_utc, title, content, source_addr, source_media):
        self.author = author
        self.time_utc = time_utc
        self.title = title
        self.content = content
        self.source_addr = source_addr
        self.source_media = source_media
    def __str__(self):
        return("""\
author:%s
time_utc:%d
title:%s
content:%s
source_addr:%s
source_media:%s"""%(self.author, self.time_utc, self.title, "111", self.source_addr, self.source_media))

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
        response = url_open("https://www.chainnews.com/api/articles/feeds/?page=%d&ts=%d"%(i, time_utc))
        #print(response)
        json_data = json.loads(response)
        for item in json_data['results']:
            article_item = article_info(item['author_name'], item["pb_timestamp"], item['title'],item['content'],item['refer_link'],"链闻chainnews")
            print(article_item)

get_news(10)
#def get_news(10)

#print(response)