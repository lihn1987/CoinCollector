import urllib.request
import json
import _thread
import threading
import time
import mysql.connector
from pyquery import PyQuery as pq
import news_base

def url_open(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0',
    'accept-language': 'zh-CN,zh;q=0.9'}  
    req = urllib.request.Request(url=url, headers=headers)
    for i in range(10):
        try:
            response = urllib.request.urlopen(url=req, timeout=5).read().decode('utf-8')
            return response
        except :
            print("chainnewscrawl except:")
def get_content(url):
    response = url_open(url)
    source_doc = pq(response)
    rtn = ''
    try:
        rtn = source_doc(".article-text").text()
    except:
        pass
    return rtn

def get_news(page_count, cb):
    error_count = 0
    responce = url_open("https://www.bishijie.com/shendu.html")
    source_doc = pq(responce)
    article_title = []
    article_author = []
    article_content = []
    url = []
    #开始抓取
    print(time.time())

    try:
        for item in source_doc(".articles-title").items():
            article_title.append(item.text())
        #print(source_doc(".articles-title").length)

        for item in source_doc(".articles-text").items():
            article_content.append(item.text())
        #print(source_doc(".articles-text").length)

        for item in source_doc(".author-name").items():
            article_author.append(item.text())

        for item in source_doc(".articles-list a").items():
            if item.attr("href").find("/shendu_") == 0:
                tmp = item.attr("href")
                if tmp not in url:
                    url.append(tmp)
    except:
        print("B世界深度异常1")
        return
    if len(article_title) != 20 or len(article_content) != 20 or len(article_author) != 20 or len(url) != 20:
        print("B世界深度异常2")
        print(len(url))
        return
    for i in range(20):
        article_item = news_base.article_info(
                article_author[i],# 
                int(time.time()),# 
                article_title[i], #
                article_content[i],#
                'content', 
                "https://www.bishijie.com"+url[i]+".html",
                "币世界深度")
        article_item.content = get_content(article_item.source_addr)
        if not cb(article_item):
            error_count+=1
        else:
            error_count = 0
        if error_count >= 3:
            break
#def get_news(10)
#get_news(1,1)
#print(response)