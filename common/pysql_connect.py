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



def insert_case(Case_title, Case_belong, Case_discription=None):
    cursor, conn = conn_db()
    sql = "insert into android_testcases(Case_title, Case_belong, Case_discription) values( %s, %s, %s)"
    try:
        cursor.execute(sql, (Case_title, Case_belong, Case_discription))
    except Exception as e:
        cursor.close()
        conn.close()
        print(e)

def exec_sql(sql, *args):
    cursor, conn = conn_db()
    return cursor.execute(sql, args), cursor.fetchall()

def recover_checked_state():
    # sql = "update android_testcases set checked=0"
    sql = "update android_testcases set checked=0"
    exec_sql(sql)

def update_checked(case_title, state):
    sql = "update android_testcases set checked=%s where Case_title=%s"
    exec_sql(sql, int(state), case_title)

def select_case(condition):
    cursor, conn = conn_db()
    if condition.upper() == 'ALL':
        select_sql = "select * from android_testcases"
        rows = cursor.execute(select_sql)
        try:
            if rows:
                result = cursor.fetchall()
                return result
            else:
                return None
        except Exception:
            pass
        finally:
            cursor.close()
            conn.close()


