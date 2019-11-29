
import json
import threading
import time

import trade_detail_huobi
import trade_detail_ok



trade_detail = {}
def detail_callback(key, info_list):

    print("callback:")
    print(key)
    for info in info_list:
        info.dump()
    print(len(info_list))
    if key not in trade_detail:
        trade_detail[key] = []
    trade_detail[key] += info_list

trade_detail_huobi.run(detail_callback)
trade_detail_ok.run(detail_callback)
while True:
    time.sleep(1)