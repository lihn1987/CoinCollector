import sys
import time
import article2coin_anylse
import news_crawl
while True:
    news_crawl.run()
    article2coin_anylse.run()
    time.sleep(60*10) 


'''
print(sys.argv[1])
if sys.argv[1]=='coin_crawl':
    import coin_crawl
elif sys.argv[1]=='news_crawl':
    import news_crawl
'''