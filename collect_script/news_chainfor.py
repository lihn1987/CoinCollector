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
    error_count = 0
    time_utc = int(time.time())*1000
    for i in range(1,page_count+1):
        #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        response = url_open("https://www.chainfor.com/home/list/news/data.do?categoryId=&lastItemTimeStamp=%d&device_type=0"%(time_utc))
        #print(response)
        json_data = json.loads(response)
        for item in json_data['list']:
            article_item = news_base.article_info(
                item['nickName'],# 
                int(item["releaseDate"]['time'])/1000,# 
                item['title'], #
                item["introduction"],#
                'content', 
                "https://www.chainfor.com/news/show/%d.html"%item["id"],
                "链向财经")
            source_responce = url_open(article_item.source_addr)
            source_doc = pq(source_responce)
            article_item.content = source_doc(".m-i-bd").html()
            time_utc = item["releaseDate"]['time']
            if not cb(article_item):
                error_count+=1
            else:
                error_count = 0
            if error_count >= 5:
                break
        if error_count >= 5:
            break
            #print(article_item)
        #print(json_data['results'][0])

#get_news(2)
#def get_news(10)

#print(response)