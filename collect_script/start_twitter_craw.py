
import json
import threading
import time
import mysql.connector
import gzip
import websocket
import redis
import pickle
import zlib
import numpy
from depth_info import DepthInfo


from config import config
import db_base
import twint

def run(user_name, coin_name):
    twitter_items = []
    twitter_item = {}
    tweets = []
    c = twint.Config()
    c.Username = user_name
    
    #c.Format = "{id}|{date}{time}|{timezone}|{username}|{tweet}|{mentions}|{link}|{photos}"
    if config["proxy_config"]["proxy_use"] == True:
        c.Proxy_type="HTTP"
        c.Proxy_host=config["proxy_config"]["proxy_ip"]
        c.Proxy_port=config["proxy_config"]["proxy_port"]
    c.Limit = 20
    c.Store_object = True
    c.Output = "none"
    c.Store_object_tweets_list = tweets
    twint.run.Search(c)
    for item in tweets:
        twitter_item = {}
        twitter_item["id"] = item.id
        twitter_item["time"] = item.datetime
        twitter_item["src"] = item.link    
        twitter_item["name"] = item.name
        twitter_item["user_name"] = item.username
        twitter_item["content"] = item.tweet
        twitter_item["image"] = item.photos
        twitter_item["reply"] = item.reply_to
        twitter_item["coin_name"] = coin_name
        if len(twitter_item["reply"]) == 1:
            twitter_items.append(twitter_item)
            db_base.insert_into_twitter(twitter_item)
    return twitter_items

twitter_config = {
"XLM":"StellarOrg",
"BSV":"BitcoinSVNode",
"EOS":"block_one_",
"LTC":"LitecoinProject",
"XRP":"Ripple",
"ETH":"VitalikButerin",
}
result = []
db_base.init_db()
for item in twitter_config:
    twitter_items = run(twitter_config[item], item)
    result.append(twitter_items)
print(result)









