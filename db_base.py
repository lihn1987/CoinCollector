import mysql.connector
import news_base
import threading
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
    db_cur = mydb.cursor()

def init_news_base():
    print("init db")
    try:
        db_cur.execute("""CREATE TABLE `coin`.`article` (
            `time_utc` INT NOT NULL,
            `title` VARCHAR(45) NOT NULL,
            `desc` TEXT NULL,
            `author` VARCHAR(45) NULL,
            `source_media` text NULL,
            `source_addr` text NULL,
            `content` TEXT NULL,
            PRIMARY KEY (`time_utc`, `title`)) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8;
            """)
        print("db_init ok")
    except:
        print("base table already exist")

def insert_article(article_item):
    try:
        sql = """insert into article values(%d,'%s','%s','%s','%s','%s','%s')
            """%(article_item.time_utc,
            article_item.title,
            article_item.desc.replace("'","""\'"""),
            article_item.author.replace("'","""\'"""),
            article_item.source_media.replace("'","""\'"""),
            article_item.source_addr.replace("'","""\'"""),
            article_item.content.replace("'","""\'"""))
        print("add artical:"+article_item.source_media+":"+article_item.title)
        threadLock.acquire()
        db_cur.execute(sql)
        mydb.commit()
        threadLock.release()
        print("insert ok~")
        return True
    except:
        threadLock.release()
        
        print("insert error!")
        return False

def get_all_content():
    db_cur.execute("select content from coin.article;")
    fetch_list = db_cur.fetchall()
    return fetch_list

def get_all_coin():
    db_cur.execute("select `name`,`name_en`, `name_cn` from coin.coin_base;")
    fetch_list = db_cur.fetchall()
    return fetch_list
threadLock = threading.Lock()