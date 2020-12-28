import mysql.connector
from pyquery import PyQuery as pq


db_cur = object
def init_db(ip, user, pw, db_name):
    global db_cur
    global mydb
    mydb = mysql.connector.connect(
        host=ip,       # 数据库主机地址
        port="3306",
        user=user,    # 数据库用户名
        passwd=pw,   # 数据库密码
        database=db_name
    )
    print(mydb)
    db_cur = mydb.cursor()

def get_all_website():
    rtn = []
    db_cur.execute("select * from coin_base order by cast(`index` as UNSIGNED INTEGER)")
    fetch_list = db_cur.fetchall()
    for item in fetch_list:
        rtn.append(item)
    return rtn
init_db("localhost", "user1", "123", "coin")
#去掉空的
weblist = get_all_website()


weblist_tmp = weblist[:]
for web_item in weblist_tmp:
    if  web_item[5]==(''):
        weblist.remove(web_item)

coinlist = []
for i in range(len(weblist)):
    coinlist.append(weblist[i][2])
    weblist[i] = weblist[i][5]

#print(coinlist)

for i in range(len(weblist)):
    weblist[i] = weblist[i].replace('https://','')
    weblist[i] = weblist[i].replace('http://','') 
    idx = weblist[i].find('/')
    if idx != -1:
        weblist[i] = weblist[i][:idx]
import urllib.request
import json
import csv
def url_open(url):
    while True:
        try:
            response = urllib.request.urlopen(url, timeout=10).read().decode('utf-8')
            return response
        except:
            print("url:%s open errer retry"%(url))

base_url = 'http://apidata.chinaz.com/CallAPI/Ip?key=a0e3929177d5436893273835b2cf94aa&ip='

i=0
datacsv = open("./XXX.csv","w",newline="")
for item in weblist:
    url=base_url+item.strip()
    response = url_open(url)
    json_obj = json.loads(response)
    if json_obj['StateCode'] == 1:
        print(coinlist[i])
        print(item)
        print(json_obj['Result']['Country'])
        print(json_obj['Result']['Province'])
        print(json_obj['Result']['City'])
        print("from:"+json_obj['Result']['Isp'])
        print("===============%d/%d========================="%(i, len(weblist)))
        
        #dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
        csvwriter = csv.writer(datacsv,dialect = ("excel"))
        #csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
        csvwriter.writerow([coinlist[i],item,json_obj['Result']['Country'],json_obj['Result']['Province'], json_obj['Result']['City'], json_obj['Result']['Isp']])
    i=i+1
    

#http://apidata.chinaz.com/CallAPI/Ip/key=a0e3929177d5436893273835b2cf94aa&ip=www.bitgogo.com
#print(weblist)
#print(response)