import urllib.request
import json
import _thread
import threading
import time
import mysql.connector
from pyquery import PyQuery as pq
import news_base
def url_open(url):
    print(url)
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}  
    req = urllib.request.Request(url=url, headers=headers)
    for i in range(10):
        try:
            response = urllib.request.urlopen(url=req, timeout=5).read().decode('utf-8')
            return response
        except Exception as e:
            print("chainnewscrawl except:"+str(e))

def get_news(page_count, cb):
    page_count*=10
    error_count = 0
    time_utc = int(time.time())
    for i in range(1,page_count+1):
        response = url_open("https://www.chainnews.com/api/articles/feeds/?page=%d&ts=%d"%(i, time_utc))
        #print(response)
        json_data = json.loads(response)
        for item in json_data['results']:
            article_item = news_base.article_info(
                item['author_name'],# 
                item["pb_timestamp"],# 
                item['title'], #
                item['digest'],
                item['content'], 
                item['refer_link'],
                "链闻chainnews")
            if not cb(article_item):
                    error_count+=1
            else:
                error_count = 0
            if error_count >= 5:
                break
        if error_count >= 5:
            break
        
#def get_news(10)

#print(response)