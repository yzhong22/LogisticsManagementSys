import utils
from database_con import *
import json
import psycopg2


def search_node_options(keyword):
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()

    sql = "select id,address from express where address ~ '{0}'".format(keyword)
    result = []
    try:
        cursor.execute(sql)  # 执行SQL
        res = cursor.fetchall()
        for d in res:
            obj = {"id": d[0], "address": d[1]}
            result.append(obj)

        return json.dumps(result)
    except Exception as e:
        print("异常信息为：", e)
        conn.rollback()  # 回滚
