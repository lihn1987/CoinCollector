
import jieba
import mysql.connector
import db_base
from pyquery import PyQuery as pq
import word_import 
def run():
    db_base.init_db()
    #通过数据库初始化币名称的关键词
    db_coin_list = db_base.get_all_coin()
    coin_base = {}
    for db_coin_row in db_coin_list:
        coin_base[db_coin_row[1]] = db_coin_row[0]
        coin_base[db_coin_row[2]] = db_coin_row[0]
        coin_base[db_coin_row[3]] = db_coin_row[0]
        for db_coin_item in db_coin_row:
            if type(db_coin_item) is not int:
                word_import.add_word_list.add(db_coin_item.upper())
            
    print("##############################1")
    for word in word_import.add_word_list:
            jieba.add_word(word.upper())
    #获取所有文章内容
    content_list = db_base.get_all_content(0)
    content_list = db_base.get_all_content(1)
    print("##############################2")
    max_size = 100000

    process=0
    well_break = False
    error_count = 0
    for i in range(max_size):
        content_list = db_base.get_all_content(i)
        #遍历所有信息
        for row in range(len(content_list)):
            process+=1
            word_list = set(jieba.cut(content_list[row][1], cut_all=False, HMM=False))
            #移除要删除的文字
            for word in word_import.del_word_list:
                if word in word_list:
                    word_list.remove(word)
            #如果币种的关键词在分词中则得到id
            for item in coin_base:
                if item in word_list:
                    if db_base.insert_article2coinbase(coin_base[item], content_list[row][0]):
                        error_count+=1
                    else:
                        return
                    break
            print(process)
        if len(content_list) == 0:
            break

        print("!!!!!!!!!!")
#run()