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
        except Exception as e:
            print("chainnewscrawl except:".str(e))

def get_news(page_count, cb):
    time_utc = int(time.time())
    error_count = 0
    for i in range(1,page_count+1):
        response = url_open("https://www.55coin.com/index/article/search.html?cat_id=4&page=%d&is_index=1"%(i))
        #print(response)
        json_data = json.loads(response)
        for item in json_data['list']:
            article_item = news_base.article_info(
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
            if not cb(article_item):
                error_count+=1
            else:
                error_count = 0
            if error_count >= 5:
                break
        if error_count >= 5:
            break
        #print(json_data['results'][0])

#def get_news(10)

#print(response)