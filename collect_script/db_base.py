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
    init_market_base_common()
    init_trade_detail()
    init_twitter()

def init_coin_base():
    print("init db")
    try:
        db_cur.execute("""CREATE TABLE `coin_base` (
            `id` BIGINT NOT NULL AUTO_INCREMENT,
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
        `coin_id` BIGINT NOT NULL,
        `article_id` BIGINT NOT NULL,
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
            `id` BIGINT NOT NULL AUTO_INCREMENT,
            `time_utc` BIGINT NOT NULL,
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

def init_market_base_common():
    try:
        db_cur.execute("""CREATE TABLE `coin`.`market_base_common`  (
            `id` int(0) NULL AUTO_INCREMENT,
            `coin_name` varchar(255) NOT NULL COMMENT '交易币种',
            `base_coin_name` varchar(255) NOT NULL COMMENT '报价币种',
            `price_precision` integer(255) NULL COMMENT '报价精度',
            `base_coin_precision` integer(255) NULL COMMENT '基础币种精度',
            `amount_precision` integer(255) NULL COMMENT '交易金额精度',
            `state` integer(255) NULL COMMENT '0可交易，1不可交易',
            `min_order_amount` decimal(30, 15) NULL COMMENT '最小下单量',
            `max_order_amount` decimal(30, 15) NULL COMMENT '最大下单量',
            `min_order_price` decimal(30, 15) NULL COMMENT '最小下单金额',
            `market` integer(255) NOT NULL COMMENT '0火币，1币安，2ok',
            PRIMARY KEY (`market`, `coin_name`, `base_coin_name`),
            INDEX `id`(`id`)
            );""")
        print("db_init ok")
    except:
        print("base table already exist")

def init_trade_detail():
    try:
        db_cur.execute("""CREATE TABLE `coin`.`trade_detail`  (
            `id` BIGINT(0) NOT NULL AUTO_INCREMENT,
            `trade_time` BIGINT(0) NOT NULL,
            `market` int(10) NULL,
            `order_coin` varchar(255) NULL,
            `base_coin` varchar(255) NULL,
            `amount` decimal(20, 10) NULL,
            `dir` int(255) NULL,
            `price` decimal(20, 10) NULL,
            PRIMARY KEY (`id`),
            INDEX `a`(`trade_time`, `market`, `order_coin`, `base_coin`, `amount`, `dir`, `price`)
            );

        ;""")
        print("db_init ok")
    except:
        print("base table already exist")

def init_twitter():
    try:
        db_cur.execute("""CREATE TABLE `coin`.`twitter`  (
            `id` bigint NOT NULL,
            `time` bigint NULL,
            `name` varchar(255) NULL,
            `username` varchar(255) NULL,
            `src` varchar(255) NULL,
            `content` text NULL,
            `coin_name` varchar(255) NULL,
            PRIMARY KEY (`id`),
            INDEX `a`(`time`),
            INDEX `b`(`coin_name`)
            );
        ;""")
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

def insert_market_base_common(coin_name ,
    base_coin_name,
    price_precision,
    base_coin_precision,
    amount_precision,
    state,
    min_order_amount,
    max_order_amount,
    min_order_price,
    market):
    sql = "insert into market_base_common values(DEFAULT, '%s','%s',%d,%d,%d,%d,'%f','%f','%f',%d)"%(coin_name ,
        base_coin_name,
        price_precision,
        base_coin_precision,
        amount_precision,
        state,
        min_order_amount,
        max_order_amount,
        min_order_price,
        market)
    try:
        db_cur.execute(sql)
        mydb.commit()
        print("交易对插入成功")
        return True
    except:
        print("交易对插入失败")
        sql = """update market_base_common set coin_name='%s', base_coin_name='%s', price_precision='%d',
        base_coin_precision='%d',
        amount_precision='%d',
        state='%d',
        min_order_amount='%f',
        max_order_amount='%f',
        min_order_price='%f',
        market='%d' where coin_name='%s' and base_coin_name='%s' and market=%d"""%(coin_name ,
        base_coin_name,
        price_precision,
        base_coin_precision,
        amount_precision,
        state,
        min_order_amount,
        max_order_amount,
        min_order_price,
        market,coin_name ,
        base_coin_name,market)
        try:
            db_cur.execute(sql)
            mydb.commit()
            print("交易对更新成功")
            return True
        except:
            print("交易对更新失败")
            return False
    '''
    `id` int(0) NOT NULL AUTO_INCREMENT,
            `trade_time` int(0) NOT NULL,
            `market` int(10) NULL,
            `order_coin` varchar(255) NULL,
            `base_coin` varchar(255) NULL,
            `amount` decimal(20, 10) NULL,
            `dir` int(255) NULL,
            `price` decimal(20, 10) NULL,
            '''
def insert_into_trade_detail(key, trade_list):
    try:
        threadLock.acquire()
        for trade in trade_list:
            sql = "insert into trade_detail values(DEFAULT, %d, %d, '%s', '%s', %f,%d, %f)"\
                %(trade['trade_time'], key[0], key[1], key[2], trade['amount'], trade['dir'], trade['price'])
            db_cur.execute(sql)
        mydb.commit()
        threadLock.release()
        return True
    except:
        threadLock.release()
        print("insert error!")
        return False

def insert_into_twitter(pram):
    try:
        sql = "insert into coin.twitter values(%d, %d, '%s', '%s', '%s', '%s','%s')"%(
            pram["id"],
            pram["time"],
            pram["name"],
            pram["user_name"],
            pram["src"],
            pram["content"],
            pram["coin_name"]
        )
        print("lalalaal:"+sql)
        db_cur.execute(sql)
        mydb.commit()
        return True
    except:
        return False






threadLock = threading.Lock()
