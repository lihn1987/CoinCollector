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

def get_news(page_count, cb):
    time_utc = int(time.time())
    error_count = 0
    index = 0
    for i in range(1,page_count+1):
        #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        response = url_open("https://api.jinse.com/v6/information/list?catelogue_key=www&limit=23&information_id=%d&flag=down&version=9.9.9&_source=www"%(index))
        #print(response)
        json_data = json.loads(response)
        for item in json_data['list']:
            if item["type"] != 1 and item["type"] != 2:
                continue
            article_item = news_base.article_info(
                item["extra"]['author'],# 
                int(item["extra"]["published_at"]),# 
                item['title'], #
                item["extra"]['summary'],#
                'content', 
                item["extra"]['topic_url'],
                "金色财金")
            source_responce = url_open(article_item.source_addr)
            try:
                source_doc = pq(source_responce)
                article_item.content = source_doc(".js-article-detail").html() if source_doc(".js-article-detail").html() else source_doc(".js-article").html()
                index = item['id']
                if not cb(article_item):
                    error_count+=1
                else:
                    error_count = 0
            except:
                error_count += 1
            if error_count >= 5:
                break
        if error_count >= 5:
            break
        #print(json_data['results'][0])

#def get_news(10)

#print(response)