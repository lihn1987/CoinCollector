# 脚本采集部分 
## 当前已实现功能
- 能够采集所有币种(通过牛眼财经)
- 能够采集下列网站的新闻
    - 链闻
    - 8btc
    - 区势传媒
    - 金色财经
    - 链向财经
- 能够分析每篇文章和哪个币种相关
- 能够抓取火币，币安，ok的币种消息
## 前置环境

### linux需要的基本工具
```
sudo apt-get install git python3 python3-pip redis-server 
```
### 安装mysql
```
mysql请自行安装，这里使用的是xampp一套带的
```

### Python需要的基础工具

```
pip3 install mysql-connector PyQuery websocket-client  redis  jieba pytz SimpleWebSocketServer numpy
```


### 需要支持https
linux ubuntu 操作
```
sudo apt-get install openssl
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
默认情况下，连接字符串你不需要改
### 初始化所有币种 
```
python3 coin_crawl.py
```

### 定期采集各个站点的新闻服务
```
python3 start_news_service.py &
```
### 开启深度服务
```
python3 start_depth_service.py&
```

### 开启交易信息服务
```
python3 start_detail_service.py&
```
### 开启分析服务
```
python3 start_analyse.py
```
# 网站端
./website

#网站后端
./website/back