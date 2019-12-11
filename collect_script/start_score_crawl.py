
import json
import threading
import time
import mysql.connector
import redis
from depth_info import DepthInfo


from config import config
import db_base


github_all_commit = 0
github_7d_commit = 0
news_related = 0
news_official = 0


db_base.init_db()
db_base.db_cur.execute("select * from github group by coin_name")
fetch_list = db_base.db_cur.fetchall()
for item in fetch_list:
    analyse_item = {}
    analyse_item["coin_name"] = item[0]
    analyse_item["commit_all"] = 0
    analyse_item["commit_7d"] = 0
    analyse_item["media_7d"] = 0
    analyse_item["media_official_7d"] = 0

    db_base.db_cur.execute("select * from github  where `time`>%d and coin_name='%s' order by `time` desc"%(time.time()-60*60*24*7,item[0]))
    #print("select * from github  where `time`>%d and coin_name='%s' order by `time` desc"%(time.time()-60*60*24*7,item[0]))
    tmp_list = db_base.db_cur.fetchall()
    if tmp_list :
        analyse_item["commit_all"] = tmp_list[0][2]
        analyse_item["commit_7d"] = tmp_list[0][2] - tmp_list[len(tmp_list)-1][2]

    db_base.db_cur.execute("""select count(*) from coin_base, article_2_coinbase, article
        where 
        name_en='%s' and 
        article_2_coinbase.coin_id = coin_base.id and
        article_2_coinbase.article_id = article.id and 
        article.time_utc > %d"""%(item[0], time.time()-60*60*24*70))
    tmp_list = db_base.db_cur.fetchall()
    if tmp_list:
        analyse_item["media_7d"] = tmp_list[0][0]

    db_base.db_cur.execute("""select count(*) from twitter where coin_name='%s' and time > %d """%(item[0], (time.time()-60*60*24*7)*1000))
    tmp_list = db_base.db_cur.fetchall()
    if tmp_list:
        analyse_item["media_official_7d"] = tmp_list[0][0]


    analyse_item["commit_all"] = 100 if analyse_item["commit_all"]>1000 else analyse_item["commit_all"]/1000*100
    analyse_item["commit_7d"] = 100 if analyse_item["commit_7d"]>7 else analyse_item["commit_7d"]/7*100
    analyse_item["media_7d"] = 100 if analyse_item["media_7d"]>7 else analyse_item["media_7d"]/7*100
    analyse_item["media_official_7d"] = 100 if analyse_item["media_official_7d"]>7 else analyse_item["media_official_7d"]/7*100
    analyse_item["score"] = \
        analyse_item["commit_all"]*0.3+\
        analyse_item["commit_7d"]*0.3+\
        analyse_item["media_7d"]*0.2+\
        analyse_item["media_official_7d"]*0.2
    param = [0]*20
    #print(param)
    param[0] = analyse_item["commit_all"]
    param[1] = analyse_item["commit_7d"]
    param[2] = analyse_item["media_7d"]
    param[3] = analyse_item["media_official_7d"]
    db_base.insert_into_score(analyse_item["coin_name"], time.time(), analyse_item["score"], param)

    print(analyse_item["coin_name"]+str(analyse_item["score"]))
    #break
    #tmp_list = db_base.db_cur.execute("select * from github group by coin_name where `time`>%d"%(time.time()-60*60*24,))
    #print(tmp_list)






