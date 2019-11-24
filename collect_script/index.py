import sys
print(sys.argv[1])
if sys.argv[1]=='coin_crawl':
    import coin_crawl
elif sys.argv[1]=='news_crawl':
    import news_crawl