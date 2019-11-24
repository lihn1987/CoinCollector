import db_base
import news_chainfor
import news_jinse
import news_8btc
import news_55coin
import news_chainnews
import threading

test = "1234"
test = test.replace("'","""\'""")
class myThread (threading.Thread):
    def __init__(self, func, arg1, arg2):
        threading.Thread.__init__(self)
        self.func = func
        self.arg1 = arg1
        self.arg2 = arg2
    def run(self):
        print ("开始线程：" + self.name)
        self.func(self.arg1, self.arg2)
        print ("退出线程：" + self.name)

db_base.init_db()

thread_list = [
    myThread(news_55coin.get_news, 10, db_base.insert_article),
    myThread(news_8btc.get_news, 10, db_base.insert_article),
    myThread(news_jinse.get_news, 10, db_base.insert_article),
    myThread(news_chainfor.get_news, 10, db_base.insert_article),
    myThread(news_chainnews.get_news, 10, db_base.insert_article)
    ]
for i in range(len(thread_list)):
    thread_list[i].start()

for i in range(len(thread_list)):
    thread_list[i].join()
