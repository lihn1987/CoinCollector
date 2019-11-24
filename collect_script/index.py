import sys
import time
import article2coin_anylse
import news_crawl
while True:
    print("开始抓取新闻>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    news_crawl.run()
    print("完成抓取新闻<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print("开始分析新闻>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    article2coin_anylse.run()
    time.sleep(60*10) 
    print("完成分析新闻<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")


'''
print(sys.argv[1])
if sys.argv[1]=='coin_crawl':
    import coin_crawl
elif sys.argv[1]=='news_crawl':
    import news_crawl
'''