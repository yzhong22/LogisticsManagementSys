import utils
from database_con import *
import json
import psycopg2


def register(provide_username, provide_keyword, provide_name):
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()

    truth_username = utils.base64decode(provide_username)
    truth_keyword = utils.base64decode(provide_keyword)
    truth_name = utils.base64decode(provide_name)

    IfSuccess = True
    IfExist = False

    sql = "select * from receiver where \"Username\"='{0}'".format(truth_username)
    try:
        cursor.execute(sql)  # 执行SQL
        res = cursor.fetchall()
        if (len(res) != 0):
            IfSuccess = False
            IfExist = True
        else:
            cursor1 = conn.cursor()
            sql1 = "INSERT INTO receiver VALUES('{0}','{1}','{2}')".format(truth_username, truth_keyword, truth_name)
            try:
                cursor1.execute(sql1)  # 执行SQL
                conn.commit()
            except Exception as e:
                print("异常信息为：", e)
                conn.rollback()  # 回滚
            cursor1.close()

    except Exception as e:
        print("异常信息为：", e)
        conn.rollback()  # 回滚

    cursor.close()
    conn.close()
    text = {"ifSucess": IfSuccess, "ifExist": IfExist}
    return json.dumps(text, ensure_ascii=False, indent=4)


def login(provide_username, provide_keyword):
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()

    IfSuccess = False
    truth_username = utils.base64decode(provide_username)
    truth_keyword = utils.base64decode(provide_keyword)
    provide_name = ""

    sql = "select \"Name\" from receiver where \"Username\"='{0}' and \"Keyword\"='{1}';" \
        .format(truth_username, truth_keyword)
    try:
        cursor.execute(sql)  # 执行SQL
        res = cursor.fetchall()
        if (len(res) != 0):
            IfSuccess = True
            truth_name = res[0][0]
            provide_name = utils.base64encode(truth_name)
    except Exception as e:
        print("异常信息为：", e)
        conn.rollback()  # 回滚
    cursor.close()
    conn.close()
    text = {"ifSuccess": IfSuccess, "username": provide_username, "name": provide_name}

    return json.dumps(text, ensure_ascii=False, indent=4)


def check_login(username, name):
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()

    sql = "select * from receiver where \"Username\"='{0}' and \"Name\"='{1}'".format(username, name)
    cursor.execute(sql)  # 执行SQL
    res = cursor.fetchall()
    if (len(res) == 0):
        return False
    else:
        return True
