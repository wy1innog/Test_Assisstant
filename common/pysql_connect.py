import pymysql


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
    cursor = conn_db()
    sql = "insert into android_testcases(Case_title, Case_belong, Case_discription) values(%s, %s, %s)"
    try:
        rows = cursor.execute(sql, (Case_title, Case_belong, Case_discription))
    except Exception as e:
        print(e)
        cursor.close()


def select_case(Case_title):
    cursor, conn = conn_db()
    if Case_title.upper() == 'ALL':
        select_sql = "select * from android_testcases"
        rows = cursor.execute(select_sql)
    else:
        select_sql = "select * from android_testcases where Case_title=%s"
        rows = cursor.execute(select_sql, Case_title)

    if rows:
        # cursor.scroll(1, 'absolute')
        return cursor.fetchall()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    # insert_case("蓝牙开关测试", "蓝牙测试", "测试蓝牙开关，检测状态变化")
    print(select_case("蓝牙开关测试"))
