import pymysql
from common.log import Log

use_table = 'android_testcases'
def conn_db():
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='123456',
        database='jz_test_cases',
        port=3306,
        charset='utf8',
        autocommit=True,
        db='case_db'
    )
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    return cursor, conn


def insert_case(Case_title, Case_belong, Case_discription=None):
    cursor, conn = conn_db()
    sql = "insert into android_testcases(Case_title, Case_belong, Case_discription) values(%s, %s, %s)"
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




if __name__ == '__main__':
    # insert_case("蓝牙开关测试", "蓝牙测试", "测试蓝牙开关，检测状态变化")
    print(select_case("蓝牙开关测试"))
