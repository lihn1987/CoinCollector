# 脚本采集部分 
## 前置环境
### 安装mysql
```
mysql请自行安装，这里使用的是xampp一套带的
```

### Python数据库连接工具的安装

```
pip3 install mysql-connector
```

### Python页面分析工具的安装

```
pip3 install PyQuery
```

### 需要支持https
linux ubuntu 操作
```
sudo apt-get install openssl-dev
```

mac 操作(Python版本根据本机的来)
```
/Applications/Python\ 3.7/Install\ Certificates.command
```

### 需要配置数据库连接字段
首先，需要在mysql中创建名称为coin的表
然后
修改db_base.py中的
```
def init_db(ip="localhost", user="root", pw="", db_name="coin"):
```
将其设置为自己的数据库连接字符串，主要是user（用户名）和pw（密码）
## 采集所有区块链币种信息
运行
```
python3 CoinNewsCollector.py
```
能够采集到每个币种的
```
名称
英文名
中文名
市值排名
官方网站
介绍
```

## 采集区块链新闻
目前的新闻来源为
```
链闻
8btc
区势传媒
金色财经
链向财经
```
运行
```
python3 news_crawl.py
```
能够抓取到近期的所有新闻，其中包括
```
新闻标题
发布时间
简介
作者
媒体来源
新闻源地址
新闻内容
```

## 分析新闻同币种之间的关系
运行
```
python3 article2coin_anylse.py 
```


##  分析区块链新闻高频词
在抓取了币种信息和新闻信息后，能够对词进行频率分析

# 网站端
./website

#网站后端
./website/back