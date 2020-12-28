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
    for i in range(1,page_count+1):
        response = url_open("https://webapi.8btc.com/bbt_api/news/list?num=20&page=%d"%(i))
        #print(response)
        json_data = json.loads(response)
        for item in json_data['data']['list']:
            article_item = news_base.article_info(item['author_info']['display_name'], int(item["post_date"]), item['title'], item['desc'],'content', 'https://www.8btc.com/article/'+str(item['id']), "8比特")
            source_responce = url_open(article_item.source_addr)
            source_doc = pq(source_responce)
            article_item.content = source_doc(".bbt-html").html()
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