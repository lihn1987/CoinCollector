# 脚本采集部分 
## 当前已实现功能
- 能够采集所有币种(通过牛眼财经)
- 能够采集下列网站的新闻
    - 链闻
    - 8btc<br/>
    - 区势传媒
    - 金色财经
    - 链向财经
- 能够分析每篇文章和哪个币种相关
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

### 此法分析工具的安装
```
pip3 install jieba
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
### 定期采集各个站点的新闻
python3 index.py

# 网站端
./website

#网站后端
./website/back