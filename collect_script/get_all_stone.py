import json
import urllib.request

from pyquery import PyQuery as pq


def get_basic_info():
    rtn = []
    for page_idx in range(0, 31):
        url = "http://app.finance.ifeng.com/list/stock.php?t=ha&f=chg_pct&o=desc&p="+str(page_idx)
        response = urllib.request.urlopen(url)
        print(url)
        if response.status ==200:
            print('get_basic_info success!')
        else:
            print('get_basic_info faild!')
            return
        doc = pq(response.read().decode('utf-8'))
        item_list = doc('.tab01 tr td').items()
        item = {}
        for i,item_tmp in enumerate(item_list):
            if i % 11 == 0:
                item["code"] = item_tmp('a').text()
            elif i % 11 == 1:
                item["name"] = item_tmp("a").text()
                rtn.append(item.copy())

    for page_idx in range(0,45):
        url = "http://app.finance.ifeng.com/list/stock.php?t=sa&f=chg_pct&o=desc&p="+str(page_idx)
        response = urllib.request.urlopen(url)
        print(url)
        if response.status ==200:
            print('get_basic_info success!')
        else:
            print('get_basic_info faild!')
            return
        doc = pq(response.read().decode('utf-8'))
        item_list = doc('.tab01 tr td').items()
        item = {}
        for i,item_tmp in enumerate(item_list):
            if i % 11 == 0:
                item["code"] = item_tmp('a').text()
            elif i % 11 == 1:
                item["name"] = item_tmp("a").text()
                rtn.append(item.copy())

    print(rtn)
    print("len:", len(rtn))
    #print(json.dumps(rtn, indent=4).encode('utf-8').decode('unicode_escape'))
    


get_basic_info()
