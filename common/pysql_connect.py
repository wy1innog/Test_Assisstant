import pymysql
import yaml
from common.log import Log

config_path = 'config/config.yml'
log = Log(__name__).getlog()


def conn_db():
    global conn
    with open(config_path, 'r', encoding='utf-8') as f:
        content = yaml.load(f.read(), yaml.FullLoader)
        try:
            conn = pymysql.connect(
                host=content['db_info']['host'],
                user=content['db_info']['user'],
                password=content['db_info']['password'],
                database=content['db_info']['database'],
                port=content['db_info']['port'],
                charset=content['db_info']['charset'],
                autocommit=True,
            )
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            return cursor, conn
        except pymysql.err.OperationalError:
            log.error("数据库连接异常")

def conn_db_tuble():
    global conn
    with open(config_path, 'r', encoding='utf-8') as f:
        content = yaml.load(f.read(), yaml.FullLoader)
        try:
            conn = pymysql.connect(
                host=content['db_info']['host'],
                user=content['db_info']['user'],
                password=content['db_info']['password'],
                database=content['db_info']['database'],
                port=content['db_info']['port'],
                charset=content['db_info']['charset'],
                autocommit=True,
            )
            # cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            cursor = conn.cursor()
            return cursor, conn
        except pymysql.err.OperationalError:
            log.error("数据库连接异常")


def exec_sql(sql):
    cursor, conn = conn_db()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def recover_checked_state():
    sql = "update ap_testcases set checked=0"
    exec_sql(sql)


def update_checked(table, title, state):
    cursor, conn = conn_db()
    sql = "update %s set checked=%s where title='%s'"%(table, int(state), title)
    cursor.execute(sql)
    cursor.close()
    conn.close()

