import time
import market_base_common_ok
import market_base_common_binance
import market_base_common_huobi
while True:
    print("开始抓取火币币对信息>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    market_base_common_huobi.run()
    print("开始抓取火币币对信息<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print("开始抓取binance币对信息>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    market_base_common_binance.run()
    print("开始抓取binance币对信息<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print("开始抓取ok币对信息>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    market_base_common_ok.run()
    print("开始抓取ok币对信息<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    time.sleep(60*10) 
    


'''
print(sys.argv[1])
if sys.argv[1]=='coin_crawl':
    import coin_crawl
elif sys.argv[1]=='news_crawl':
    import news_crawl
'''