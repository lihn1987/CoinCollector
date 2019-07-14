import urllib.request
import json
from pyquery import PyQuery as pq


class coin_info:
    index = 0
    name = ''
    name_en = ''
    name_cn = ''
    price_now = 0.0

    def __init__(self, index = 0, name = '', name_en = '', name_cn = '', price_now = 0.0):
        self.index = int(index)
        self.name = name
        self.name_en = name_en
        self.name_cn = name_cn
        self.price_now = float(price_now)
        self.official_website = ''
    def print(self):
        print("index:%05d  full name:%28s  english name:%8s  chinese name:%8s  price now:%f" %(self.index , self.name ,self.name_en ,self.name_cn ,self.price_now));
        print("website:%40s"%(self.official_website))


def get_basic_info(count = 100):
    response = urllib.request.urlopen("https://web-market.niuyan.com/web/v1/coins?pagesize="+str(count)+"&offset=0&lan=zh-cn")
    if response.status ==200:
        print('get_basic_info success!')
    else:
        print('get_basic_info faild!')
        return
    #print(response.read().decode('utf-8'))
    json_data = json.loads(response.read().decode('utf-8'))
    #print(json_data)
    info = json_data['data']['data']
    #print(info)
    for i in range(0, len(json_data['data']['data'])):
        xx = coin_info(info[i][2], info[i][0], info[i][1], info[i][4], info[i][5]);   
        xx.official_website = get_official_website(xx.name)
        xx.print()

#通过coin_name拼接网址，获取官方网站
def get_official_website(coin_name):
    response = urllib.request.urlopen("https://niuyan.com/zh/currencies/"+coin_name)
    if response.status ==200:
        print('get_official_website seccess!')
    else:
        print('get_official_website faild!')
        return
    web_source = response.read().decode('utf-8')
    flag_str = '''"websites":"'''
    index_begin = web_source.find(flag_str, 0)+len(flag_str)
    if index_begin == -1:
        return
    index_end = web_source.find("\"", index_begin)
    if index_end == -1:
        return
    rtn = web_source[index_begin: index_end]
    rtn = rtn.replace("\\u002F", "\\")
    return rtn
get_basic_info(100);
