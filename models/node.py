import utils
from database_con import *
import json
import psycopg2
import time


def search_node_options(keyword):
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()

    sql = "select id,address from express where address ~ '{0}'".format(keyword)
    result = []
    exist = []
    try:
        cursor.execute(sql)  # 执行SQL
        res = cursor.fetchall()
        for d in res:
            if (d[1] not in exist):
                obj = {"id": d[0], "address": d[1]}
                exist.append(d[1])
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


def receive_queryAll(nodeid):
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    sql = "select t_order.id, t_add.receivername, deliver.name, t_order.gooddescription, " \
          "t_add.city, t_add.addressdetail, deliver.city, deliver.addressdetail " \
          "from routeinfo, deliveryorder as t_order,receiveraddressinfo as t_add, deliver " \
          "where t_order.id = routeinfo.orderid and t_order.orderstate=1 " \
          "and routeinfo.nodeid={0} and t_order.nodestate = 1 " \
          "and t_order.nodenumnow = routeinfo.sequenceid - 1 " \
          "and t_order.receiverusername = t_add.accountusername " \
          "and t_order.receiveraddressid = t_add.id " \
          "and t_order.deliverusername = deliver.username" \
        .format(nodeid)
    try:
        cursor.execute(sql)  # 执行SQL
        res = cursor.fetchall()
        result = []
        for list in res:
            text = {"id": list[0], "receiverName": list[1], "deliverName": list[2], "goodDescription": list[3],
                    "receiverAddress": list[4] + list[5], "deliverAddress": list[6] + list[7]}
            result.append(text)

        return json.dumps(result, ensure_ascii=False, indent=4)
    except Exception as e:
        print("异常信息为：", e)


def receive_query(nodeid, search_keyword):
    res = json.loads(receive_queryAll(nodeid))
    result = []
    for r in res:
        if search_keyword in r["receiverName"] or search_keyword in r["deliverName"] or search_keyword in r[
            "goodDescription"] or search_keyword in r["receiverAddress"] or search_keyword in r["deliverAddress"]:
            result.append(r)
    return json.dumps(result, ensure_ascii=False, indent=4)


def receive_confirm(id):
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    sql_query_node_now = "select nodenumnow from deliveryorder where id='%s'" % (id)

    node_num_now = 0
    try:
        cursor.execute(sql_query_node_now)  # 执行SQL
        res = cursor.fetchall()
        node_num_now = res[0][0]
    except Exception as e:
        print("异常信息为：", e)
        conn.rollback()  # 回滚

    sql_query_node_num = "select sequenceid from routeinfo where orderid='{0}'".format(id)
    node_num = 0
    node_num_now += 1
    try:
        cursor.execute(sql_query_node_num)  # 执行SQL
        res = cursor.fetchall()
        node_num = len(res)
    except Exception as e:
        print("异常信息为：", e)
        conn.rollback()  # 回滚

    sql_update_state = "update deliveryorder set nodenumnow={0},nodestate=0 where id='{1}'".format(node_num_now, id)
    try:
        cursor.execute(sql_update_state)  # 执行SQL
        conn.commit()
    except Exception as e:
        print("异常信息为：", e)
        conn.rollback()  # 回滚

    if node_num_now == node_num:
        sql_if_arrive = "update deliveryorder set orderstate=2 where id='%s'" % (id)
        try:
            cursor.execute(sql_if_arrive)  # 执行SQL
            conn.commit()
        except Exception as e:
            print("异常信息为：", e)
            conn.rollback()  # 回滚

    ticks = int(round(time.time() * 1000))
    sql_update_arriving_time = "update routeinfo set arrivingtime='{0}' where orderid='{1}' and sequenceid={2}".format(
        ticks, id, node_num_now)
    try:
        cursor.execute(sql_update_arriving_time)  # 执行SQL
        conn.commit()
        text = {"ifSuccess": True}
    except Exception as e:
        print("异常信息为：", e)
        text = {"ifSuccess": False}
        conn.rollback()  # 回滚
    cursor.close()
    conn.close()
    return json.dumps(text, ensure_ascii=False, indent=4)


def send_queryAll(nodeid):
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    sql = "select t_order.id, t_add.receivername, deliver.name, t_order.gooddescription, " \
          "t_add.city, t_add.addressdetail, deliver.city, deliver.addressdetail, t_order.nodenumnow " \
          "from routeinfo, deliveryorder as t_order,receiveraddressinfo as t_add, deliver " \
          "where t_order.id = routeinfo.orderid and t_order.orderstate = 1 " \
          "and routeinfo.nodeid={0} and t_order.nodestate = 0 " \
          "and t_order.nodenumnow = routeinfo.sequenceid " \
          "and t_order.receiverusername = t_add.accountusername " \
          "and t_order.receiveraddressid = t_add.id " \
          "and t_order.deliverusername = deliver.username" \
        .format(nodeid)
    try:
        cursor.execute(sql)  # 执行SQL
        res = cursor.fetchall()
        result = []
        for list in res:
            text = {"id": list[0], "receiverName": list[1], "deliverName": list[2], "goodDescription": list[3],
                    "receiverAddress": list[4] + list[5], "deliverAddress": list[6] + list[7]}
            node_num_now = list[8]
            sql_next_node = "select express.address " \
                            "from routeinfo, express " \
                            "where routeinfo.orderid='{0}' and routeinfo.sequenceid={1} and routeinfo.nodeid = express.id" \
                .format(list[0], node_num_now + 1)
            cursor.execute(sql_next_node)
            res = cursor.fetchall()
            text["nextNodeAddress"] = res[0][0]
            result.append(text)

        return json.dumps(result, ensure_ascii=False, indent=4)
    except Exception as e:
        print("异常信息为：", e)


def send_query(nodeid, search_keyword):
    res = json.loads(send_queryAll(nodeid))
    result = []
    for r in res:
        if search_keyword in r["receiverName"] or search_keyword in r["deliverName"] or search_keyword in r[
            "goodDescription"] or search_keyword in r["receiverAddress"] or search_keyword in r["deliverAddress"]:
            result.append(r)
    return json.dumps(result, ensure_ascii=False, indent=4)


def send_confirm(id):
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    try:
        sql_update_node_state = "update deliveryorder set nodestate=1 where id ='%s'" % (id)
        cursor.execute(sql_update_node_state)  # 执行SQL
        conn.commit()

        sql_query_node_num = "select nodenumnow from deliveryorder where id='%s'" % (id)
        cursor.execute(sql_query_node_num)  # 执行SQL
        res = cursor.fetchall()
        nodenum = res[0][0]

        ticks = int(round(time.time() * 1000))
        sql_update_leaving_time = "update routeinfo set leavingtime='%s' where orderid='%s' and sequenceid=%d" % (
            ticks, id, nodenum)
        cursor.execute(sql_update_leaving_time)  # 执行SQL
        conn.commit()
        cursor.close()
        conn.close()
        return json.dumps({"ifSuccess": True}, ensure_ascii=False, indent=4)
    except Exception as e:
        print("异常信息为：", e)
        conn.rollback()  # 回滚
        return json.dumps({"ifSuccess": False}, ensure_ascii=False, indent=4)


def send_changenext(id, nextnodeid):
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    try:
        sql = "select nodenumnow from deliveryorder where id='%s' and nodestate=0" % (id)
        cursor.execute(sql)  # 执行SQL
        res = cursor.fetchall()
        node_num_now = res[0][0]
        node_num_next = node_num_now + 1

        sql2 = "update routeinfo set nodeid=%d where orderid='%s'and sequenceid=%d" % (nextnodeid, id, node_num_next)
        cursor.execute(sql2)  # 执行SQL
        conn.commit()

        cursor.close()
        conn.close()
        return json.dumps({"ifSuccess": True}, ensure_ascii=False, indent=4)
    except Exception as e:
        print("异常信息为：", e)
        conn.rollback()  # 回滚
        return json.dumps({"ifSuccess": False}, ensure_ascii=False, indent=4)


def fetch_queryAll(nodeid):
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    sql = "select t_order.id, t_add.receivername,t_add.phoneNum, t_order.gooddescription, " \
          "t_add.city, t_add.addressdetail, routeinfo.arrivingtime " \
          "from routeinfo, deliveryorder as t_order,receiveraddressinfo as t_add " \
          "where t_order.id = routeinfo.orderid and t_order.orderstate = 2 " \
          "and routeinfo.nodeid={0} and t_order.receivingoption = 1 " \
          "and t_order.nodenumnow = routeinfo.sequenceid " \
          "and t_order.receiverusername = t_add.accountusername " \
          "and t_order.receiveraddressid = t_add.id " \
        .format(nodeid)
    try:
        cursor.execute(sql)  # 执行SQL
        res = cursor.fetchall()
        result = []
        for list in res:
            text = {"id": list[0], "receiverName": list[1], "receiverPhoneNum": list[2], "goodDescription": list[3],
                    "receiverAddress": list[4] + list[5]}
            arriving_time = list[6]
            ticks = time.time()
            arrivingtime_local = int(arriving_time) / 1000
            diff_time = ticks - arrivingtime_local
            struct_time = time.gmtime(diff_time)
            detained_day = struct_time.tm_mday - 1
            detained_hour = struct_time.tm_hour
            detained_time = str(detained_day) + "天" + str(detained_hour) + "小时"
            text["detainedTime"] = detained_time

            result.append(text)

        return json.dumps(result, ensure_ascii=False, indent=4)
    except Exception as e:
        print("异常信息为：", e)


def fetch_query(nodeid, search_keyword):
    res = json.loads(fetch_queryAll(nodeid))
    result = []
    for r in res:
        if search_keyword in r["receiverName"] or search_keyword in r["receiverPhoneNum"] or search_keyword in r[
            "goodDescription"] or search_keyword in r["receiverAddress"]:
            result.append(r)
    return json.dumps(result, ensure_ascii=False, indent=4)


def dispatch_queryAll(nodeid):
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    sql = "select t_order.id, t_add.receivername,t_add.phoneNum, t_order.gooddescription, " \
          "t_add.city, t_add.addressdetail, t_order.orderstate, t_add.addresslon, t_add.addresslat, t_order.dispatcherusername " \
          "from routeinfo, deliveryorder as t_order,receiveraddressinfo as t_add " \
          "where t_order.id = routeinfo.orderid and t_order.orderstate > 1 and t_order.orderstate < 4 " \
          "and routeinfo.nodeid={0} and t_order.receivingoption = 0 " \
          "and t_order.nodenumnow = routeinfo.sequenceid " \
          "and t_order.receiverusername = t_add.accountusername " \
          "and t_order.receiveraddressid = t_add.id " \
        .format(nodeid)
    try:
        cursor.execute(sql)  # 执行SQL
        res = cursor.fetchall()
        result = []
        for list in res:
            text = {"id": list[0], "receiverName": list[1], "receiverPhoneNum": list[2], "goodDescription": list[3],
                    "receiverAddress": list[4] + list[5], "orderState": list[6], "receiverLng": list[7],
                    "receiverLat": list[8], "dispatcherName": "", "dispatcherPhoneNum": ""}
            dispatcher_username = list[9]
            if (dispatcher_username != None):
                sql_query_dispatcher = "select dispatcher.name, phonenum from dispatcher where username='{0}'".format(
                    dispatcher_username)
                cursor.execute(sql_query_dispatcher)
                r = cursor.fetchall()
                text["dispatcherName"] = r[0][0]
                text["dispatcherPhoneNum"] = r[0][1]
            result.append(text)
        return json.dumps(result, ensure_ascii=False, indent=4)
    except Exception as e:
        print("异常信息为：", e)


def dispatch_query(nodeid, search_keyword):
    res = json.loads(dispatch_queryAll(nodeid))
    result = []
    for r in res:
        if search_keyword in r["receiverName"] or search_keyword in r["receiverPhoneNum"] or search_keyword in r[
            "goodDescription"] or search_keyword in r["receiverAddress"] or search_keyword in r[
            "dispatcherName"] or search_keyword in r["dispatcherPhoneNum"]:
            result.append(r)
    return json.dumps(result, ensure_ascii=False, indent=4)
