import mysql.connector
import news_base
import threading
db_cur = object
def init_db(ip="localhost", user="root", pw="", db_name="coin"):
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
    init_coin_base()
    init_news_base()
    init_article2coinbase()

def init_coin_base():
    print("init db")
    try:
        db_cur.execute("""CREATE TABLE `coin_base` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `index` varchar(45) DEFAULT NULL,
            `name` varchar(45) DEFAULT NULL,
            `name_en` varchar(45) DEFAULT NULL,
            `name_cn` varchar(45) DEFAULT NULL,
            `official_website` text,
            `description` text,
            PRIMARY KEY (`id`),
            UNIQUE KEY `name_UNIQUE` (`name`)
            ) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8;
            """)

        print("db_init ok")
    except:
        print("base table already exist")

def init_article2coinbase():
    try:
        db_cur.execute("""
        CREATE TABLE `coin`.`article_2_coinbase`  (
        `coin_id` int(0) NOT NULL,
        `article_id` int(0) NOT NULL,
        PRIMARY KEY (`coin_id`, `article_id`),
        CONSTRAINT `a` FOREIGN KEY (`coin_id`) REFERENCES `coin`.`coin_base` (`id`),
        CONSTRAINT `b` FOREIGN KEY (`article_id`) REFERENCES `coin`.`article` (`id`)
        );
        """)
    except:
        print("base table already exist")

def init_news_base():
    print("init db")
    try:
        db_cur.execute("""CREATE TABLE `coin`.`article` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `time_utc` INT NOT NULL,
            `title` VARCHAR(45) NOT NULL,
            `desc` TEXT NULL,
            `author` VARCHAR(45) NULL,
            `source_media` text NULL,
            `source_addr` text NULL,
            `content` TEXT NULL,
            KEY `id` (`id`),
            PRIMARY KEY (`time_utc`, `title`)) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8;
            """)
        print("db_init ok")
    except:
        print("base table already exist")
    
def insert_coin_info(index, name, name_en, name_cn, official_website, description):
    try:
        sql_str = """
            insert into `coin_base` values(DEFAULT,'%s','%s','%s','%s','%s','%s') 
            """%(index, 
            name, 
            name_en, 
            name_cn,
            official_website,
            description)
        sql_str = sql_str.replace('\\', '\\\\')
        threadLock.acquire()
        db_cur.execute(sql_str)
        mydb.commit()
        threadLock.release()
        return True
    except:
        threadLock.release()
        return False

def insert_article(article_item):
    try:
        sql = """insert into article values(DEFAULT, %d,'%s','%s','%s','%s','%s','%s')
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

def insert_article2coinbase(coin_id, article_id):
    try:
        sql = """insert into article_2_coinbase values(%d, %d)
            """%(coin_id, article_id)
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

def get_all_content(index):
    sql = "select `id`, `content` from coin.article order by time_utc desc limit %d, 10"%(index*10)
    db_cur.execute(sql)
    fetch_list = db_cur.fetchall()
    return fetch_list

def get_all_coin():
    db_cur.execute("select `id`, `name`,`name_en`, `name_cn` from coin.coin_base;")
    fetch_list = db_cur.fetchall()
    return fetch_list


threadLock = threading.Lock()
