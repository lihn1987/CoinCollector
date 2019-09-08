import urllib.request
import json
#from pyquery import PyQuery as pq
def get_basic_info(page_size = 100, page_start = 0, page_count = 2):
    rtn = []
    for page_idx in range(page_start, page_count):
        url = "https://web-market.niuyan.com/web/v1/coins?pagesize="+str(page_size)+"&offset="+str(page_size*page_idx)+"&lan=zh-cn";
        response = urllib.request.urlopen(url)
        print(url)
        if response.status ==200:
            print('get_basic_info success!')
        else:
            print('get_basic_info faild!')
            return
        json_data = json.loads(response.read().decode('utf-8'))
        info = json_data['data']['data']
        #print(info)
        for i in range(0, len(json_data['data']['data'])):
            print(str(i)+"...........")
            item = {}
            item["full_name"] = info[i][0]
            print(type(info[i][4]))
            item["name_cn"] = info[i][4]
            print(info[i][4])
            item["name_en"] = info[i][1]
            rtn.append(item)
    print(json.dumps(rtn, indent=4).encode('utf-8').decode('unicode_escape'))
    #print(rtn)
    return rtn


get_basic_info()