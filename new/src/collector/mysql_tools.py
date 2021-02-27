import pymysql
from DBUtils.PooledDB import PooledDB
import time
db = None
db_cursor = None
sql_ip = "mysql"
sql_user = "root"
sql_passwd = "123456"
sql_db = "coin"
while True:
    time.sleep(1)
    try:
        pool = PooledDB(pymysql, 5, host=sql_ip, user=sql_user, passwd=sql_passwd, db=sql_db)  # 5为连接池里的最少连接数
        break
    except:
        time.sleep(1)
        pass
""" init db """
def GetDB():
    conn = pool.connection()
    return conn