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
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0',
    'accept-language': 'zh-CN,zh;q=0.9'}  
    req = urllib.request.Request(url=url, headers=headers)
    for i in range(10):
        try:
            response = urllib.request.urlopen(url=req, timeout=5).read().decode('utf-8')
            return response
        except :
            print("chainnewscrawl except:")

def get_news(page_count, cb):
    error_count = 0
    responce = url_open("https://www.bishijie.com/")
    source_doc = pq(responce)
    article_title = []
    article_author = []
    article_content = []
    url = []
    #开始抓取
    print(time.time())


    try:
        for item in source_doc(".newscontainer h3").items():
            article_title.append(item.text()[6:])

        for item in source_doc(".newscontainer .news-content").items():
            article_content.append(item.text())

        for item in source_doc(".newscontainer a").items():
            if item.attr("href").find("/kuaixun_") == 0:
                tmp = item.attr("href")
                if tmp not in url:
                    url.append(tmp)
    except:
        print("B世界深度异常1")
        return
    if len(article_title) != 30 or len(article_content) != 30 or len(url) != 30:
        print("B世界深度异常2")
        print(len(url))
        return
    for i in range(30):
        article_item = news_base.article_info(
                "币世界快讯",# 
                int(time.time()),# 
                article_title[i], #
                article_content[i],#
                article_content[i], 
                "https://www.bishijie.com"+url[i],
                "币世界深度")
        if not cb(article_item):
            error_count+=1
        else:
            error_count = 0
        if error_count >= 3:
            break
#def get_news(10)
#get_news(1,1)
#print(response)