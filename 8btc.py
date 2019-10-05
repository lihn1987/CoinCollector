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
source_media:%s"""%(self.author, self.time_utc, self.title, self.desc, self.content, self.source_addr, self.source_media))

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
        response = url_open("https://webapi.8btc.com/bbt_api/news/list?num=20&page=%d"%(i))
        #print(response)
        json_data = json.loads(response)
        for item in json_data['data']['list']:
            
            article_item = article_info(item['author_info']['display_name'], int(item["post_date"]), item['title'], item['desc'],'content', 'https://www.8btc.com/article/'+str(item['id']), "8比特")
            source_responce = url_open(article_item.source_addr)
            source_doc = pq(source_responce)
            article_item.content = source_doc(".bbt-html").html()
            print(article_item)
        #print(json_data['results'][0])

get_news(1)
#def get_news(10)

#print(response)