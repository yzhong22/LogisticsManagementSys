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


def query_node_detail(id):
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()

    sql = "select express.address,longtitude,latitude from express,point where express.id={0} and express.address=point.address".format(
        id)
    try:
        cursor.execute(sql)  # 执行SQL
        res = cursor.fetchall()
        address = res[0][0]
        lng = res[0][1]
        lat = res[0][2]
        text = {"address": address, "lng": lng, "lat": lat}
        return json.dumps(text)
    except Exception as e:
        print("异常信息为：", e)
        conn.rollback()  # 回滚
