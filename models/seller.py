import utils
from database_con import *
import json
import psycopg2
import time
import random


def register(provide_username, provide_keyword, provide_name, phoneNum, province, city, addressDetail, lon, lat):
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()

    truth_username = utils.base64decode(provide_username)
    truth_keyword = utils.base64decode(provide_keyword)
    truth_name = utils.base64decode(provide_name)

    IfSuccess = True
    IfExist = False

    sql = "select * from deliver where \"username\"='{0}'".format(truth_username)
    try:
        cursor.execute(sql)  # 执行SQL
        res = cursor.fetchall()
        if (len(res) != 0):
            IfSuccess = False
            IfExist = True
        else:
            cursor1 = conn.cursor()
            sql1 = "INSERT INTO deliver VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')".format(
                truth_username,
                truth_keyword,
                truth_name, province,
                city, addressDetail, lon, lat, phoneNum)
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

    sql = "select \"name\" from deliver where \"username\"='{0}' and \"keyword\"='{1}';" \
        .format(truth_username, truth_keyword)
    try:
        cursor.execute(sql)  # 执行SQL
        res = cursor.fetchall()
        if (len(res) != 0):
            IfSuccess = True
            truth_name = str(res[0][0])

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

    sql = "select * from deliver where \"username\"='{0}' and \"name\"='{1}'".format(username, name)
    cursor.execute(sql)  # 执行SQL
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    if (len(res) == 0):
        return False
    else:
        return True


def basic_info(username):
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()

    truth_username = utils.base64decode(username)

    sql = "select \"name\",\"addresslon\",\"addresslat\" from deliver where \"username\"='{0}';" \
        .format(truth_username)

    cursor.execute(sql)  # 执行SQL
    res = cursor.fetchall()
    name = res[0][0]
    lng = res[0][1]
    lat = res[0][2]

    text = {"username": username, "name": name, "lng": lng, "lat": lat}
    return json.dumps(text, ensure_ascii=False, indent=4)


def all_seller():
    conn = psycopg2.connect(database=database,
                            user=user,
                            password=password,
                            host=host, port=port)
    cursor = conn.cursor()
    sql = "select * from deliver"
    username = []
    name = []
    province = []
    city = []
    addressdetail = []
    addresslon = []
    addresslat = []
    phonenum = []
    try:
        cursor.execute(sql)  # 执行SQL
        res = cursor.fetchall()
        for list in res:
            username.append(list[0])
            name.append(list[2])
            province.append(list[3])
            city.append(list[4])
            addressdetail.append(list[5])
            addresslon.append(list[6])
            addresslat.append(list[7])
            phonenum.append(list[8])
    except Exception as e:
        print("异常信息为：", e)
        conn.rollback()  # 回滚
    cursor.close()
    conn.close()
    para = []
    for i in range(len(username)):
        text = {"username": username[i], "province": province[i], "city": city[i], "name": name[i],
                "addressDetail": addressdetail[i],
                "addressLon": addresslon[i], "addressLat": addresslat[i], "phoneNum": phonenum[i]
                }
        para.append(text)
    return json.dumps(para, ensure_ascii=False, indent=4)


def send_queryAll(username):
    truth_username = utils.base64decode(username)
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()

    para = []
    sql = "select t_order.id, t_address.receivername, t_order.gooddescription, t_address.city, t_address.addressdetail " \
          "from deliveryorder as t_order, receiveraddressinfo as t_address " \
          "where t_order.deliverusername='{0}' and t_order.orderstate=0 and t_order.receiverusername=t_address.accountusername " \
          "and t_order.receiveraddressid=t_address.id".format(
        truth_username)
    try:
        cursor.execute(sql)  # 执行SQL
        res = cursor.fetchall()
        for list in res:
            text = {"id": list[0], "receiverName": list[1], "goodDescription": list[2],
                    "receiverAddress": list[3] + list[4]}
            para.append(text)
    except Exception as e:
        print("异常信息为：", e)
        conn.rollback()  # 回滚
    return json.dumps(para, ensure_ascii=False, indent=4)


def send_query(username, search_keyword):
    all_orders = json.loads(send_queryAll(username))
    para = []
    for order in all_orders:
        if (search_keyword in order["receiverName"] or search_keyword in order["goodDescription"] or search_keyword in
                order["receiverAddress"]):
            para.append(order)

    return json.dumps(para, ensure_ascii=False, indent=4)


def send_nearbynodes(username):
    truth_username = utils.base64decode(username)
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    sql = "select * from deliver where username='%s'" % (truth_username)
    province = ""
    city = ""
    lat = 0
    lon = 0
    try:
        cursor.execute(sql)  # 执行SQL
        res = cursor.fetchall()
        province = res[0][3]
        city = res[0][4]
        lon = res[0][6]
        lat = res[0][7]
    except Exception as e:
        print("异常信息为：", e)
        conn.rollback()  # 回滚
    sql = "SELECT express.id,express.address,ST_Distance(ST_Transform(st_geomfromtext('POINT({0} {1})',4326), 32650), " \
          "ST_Transform(point_new.log_point, 32650)) as distance,point.longtitude, point.latitude,express.province,express.city " \
          "FROM point_new,express,point " \
          "where ST_DWithin(ST_Transform(st_geomfromtext('POINT({0} {1})',4326),32650),ST_Transform(point_new.log_point,32650),5000) " \
          "and point.address=express.address " \
          "and express.address=point_new.address " \
          "order by distance,express.id;".format(lon, lat)

    options = []
    all_address = []
    try:
        cursor.execute(sql)
        res = cursor.fetchall()
        for r in res:
            id = r[0]
            address = r[1]
            distance = r[2]
            lng = r[3]
            lat = r[4]
            node_province = r[5]
            node_city = r[6]
            if (node_city in city or node_province in city) and address not in all_address:
                option = {"id": id, "address": address, "distance": str(int(distance)) + "米", "lng": lng, "lat": lat}
                options.append(option)
                all_address.append(address)

    except Exception as e:
        print("异常信息为：", e)
        conn.rollback()  # 回滚
    return json.dumps(options)


def order_queryall(username):
    truth_username = utils.base64decode(username)
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    sql = "select t_order.id,t_add.receivername,t_add.addressdetail,t_order.gooddescription,t_order.orderstate,t_order.receivingoption " \
          "from deliveryorder as t_order, receiveraddressinfo as t_add " \
          "where deliverusername='{0}' and t_add.id=t_order.receiveraddressid and t_add.accountusername=t_order.receiverusername".format(
        truth_username)
    para = []
    try:
        cursor.execute(sql)  # 执行SQL
        res = cursor.fetchall()
        for list in res:
            text = {"id": list[0], "receiverName": list[1], "receiverAddress": list[2],
                    "goodDescription": list[3], "orderState": list[4]
                , "receivingOption": list[5]}
            para.append(text)
    except Exception as e:
        print("异常信息为：", e)
        conn.rollback()  # 回滚

    cursor.close()
    conn.close()
    return json.dumps(para, ensure_ascii=False, indent=4)


def order_query(search_keyword, username):
    res = json.loads(order_queryall(username))
    para = []
    for r in res:
        if (search_keyword in r["receiverName"] or search_keyword in r["receiverAddress"] or search_keyword in r[
            "goodDescription"]):
            para.append(r)
    return json.dumps(para, ensure_ascii=False, indent=4)


def order_callback_queryall(username):
    truth_username = utils.base64decode(username)
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    sql = "select t_order.id,t_add.receivername,t_add.addressdetail,t_order.gooddescription,t_order.callbackstate " \
          "from deliveryorder as t_order, receiveraddressinfo as t_add " \
          "where deliverusername='{0}' and t_add.id=t_order.receiveraddressid " \
          "and t_add.accountusername=t_order.receiverusername and t_order.orderstate=4".format(
        truth_username)
    para = []
    try:
        cursor.execute(sql)  # 执行SQL
        res = cursor.fetchall()
        for list in res:
            text = {"id": list[0], "receiverName": list[1], "receiverAddress": list[2],
                    "goodDescription": list[3], "callbackState": list[4]}
            para.append(text)
    except Exception as e:
        print("异常信息为：", e)
        conn.rollback()  # 回滚

    cursor.close()
    conn.close()
    return json.dumps(para, ensure_ascii=False, indent=4)


def order_callback_query(username, search_keyword):
    res = json.loads(order_callback_queryall(username))
    para = []
    for r in res:
        if search_keyword in r["receiverName"] or search_keyword in r["receiverAddress"] \
                or search_keyword in r["goodDescription"]:
            para.append(r)
    return json.dumps(para, ensure_ascii=False, indent=4)


def order_callback_agree(id):
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    sql_set_callbackstate = "update deliveryorder set callbackstate=2 where id='%s' " % (id)
    try:
        cursor.execute(sql_set_callbackstate)  # 执行SQL
        conn.commit()
    except Exception as e:
        print("异常信息为：", e)
        conn.rollback()  # 回滚
        return json.dumps({"ifSuccess": False}, ensure_ascii=False, indent=4)

    nodenumnow = 0
    nodestate = 0
    sql_select_nodenow = "select nodenumnow, nodestate from deliveryorder where id='%s'" % (id)
    try:
        cursor.execute(sql_select_nodenow)  # 执行SQL
        res = cursor.fetchall()
        nodenumnow = res[0][0]
        nodestate = res[0][1]
    except Exception as e:
        print("异常信息为：", e)
        return json.dumps({"ifSuccess": False}, ensure_ascii=False, indent=4)

    if (nodestate == 1):
        nodenumnow += 1

    if (nodenumnow == 1):
        return {"ifSuccess": True}

    sql_delete_append_nodes = "delete from routeinfo where sequenceid>%d and orderid='%s'" % (nodenumnow, id)
    try:
        cursor.execute(sql_delete_append_nodes)  # 执行SQL
        conn.commit()
    except Exception as e:
        print("异常信息为：", e)
        conn.rollback()  # 回滚
        return json.dumps({"ifSuccess": False}, ensure_ascii=False, indent=4)

    sql_query_past_nodes = "select nodeid from routeinfo where orderid='%s' order by sequenceid desc" % (id)
    nodeid = []
    try:
        cursor.execute(sql_query_past_nodes)  # 执行SQL
        res = cursor.fetchall()
        i = 0
        for list in res:
            i += 1
            if i == 1:
                continue
            nodeid.append(list[0])

    except Exception as e:
        print("异常信息为：", e)
        return json.dumps({"ifSuccess": False}, ensure_ascii=False, indent=4)

    length = len(nodeid)
    assert nodenumnow == length + 1

    for i in range(length):
        sql_insert_rest_nodes = 'insert into routeinfo(nodeid,orderid,sequenceid)'"VALUES(%d,'%s',%d)" % (
            nodeid[length - i - 2], id, length + 2 + i)
        try:
            cursor.execute(sql_insert_rest_nodes)  # 执行SQL
            conn.commit()
        except Exception as e:
            print("异常信息为：", e)
            conn.rollback()  # 回滚
            return json.dumps({"ifSuccess": False}, ensure_ascii=False, indent=4)
    cursor.close()
    conn.close()
    return json.dumps({"ifSuccess": True}, ensure_ascii=False, indent=4)


def order_callback_finish(id):
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    sql1 = "select arrivingtime, sequenceid from routeinfo where orderid='%s' order by sequenceid DESC" % (id)
    try:
        cursor.execute(sql1)  # 执行SQL
        res = cursor.fetchall()
        if (res[0][0] == None):
            text = {"ifSuccess": False, "content": "失败！退货商品尚未到达!"}
        else:
            ticks = int(round(time.time() * 1000))
            sql2 = "update deliveryorder set callbackstate=3, orderstate=5,finishtime='{0}' where id='{1}'".format(
                ticks, id)
            cursor.execute(sql2)  # 执行SQL
            conn.commit()
            text = {"ifSuccess": True}

        cursor.close()
        conn.close()
        return json.dumps(text, ensure_ascii=False, indent=4)
    except Exception as e:
        print("异常信息为：", e)
        conn.rollback()  # 回滚
        return json.dumps({"ifSuccess": False, "content": "失败！更新异常!"}, ensure_ascii=False, indent=4)


def make_route(nodeid, id):
    conn = psycopg2.connect(database=database,
                            user=user,
                            password=password,
                            host=host, port=port)
    cursor = conn.cursor()
    try:
        order_id = id;
        sql = "select receiveraddressid,receiverusername from deliveryorder where id='%s' " % (id)
        cursor.execute(sql)  # 执行SQL
        res = cursor.fetchall()
        receiveraddressid = res[0][0]
        receiverusername = res[0][1]

        sql0 = "select addresslon,addresslat,province,city from receiveraddressinfo where id=%d and accountusername='%s'" % (
            receiveraddressid, receiverusername)
        cursor.execute(sql0)  # 执行SQL
        res = cursor.fetchall()
        addresslon = res[0][0]
        addresslat = res[0][1]
        receiver_province = res[0][2]
        receiver_city = res[0][3]

        lng = addresslon
        lat = addresslat
        sql_query_nearby_nodes = "SELECT express.id,express.address,ST_Distance(ST_Transform(st_geomfromtext('POINT({0} {1})',4326), 32650), " \
                                 "ST_Transform(point_new.log_point, 32650)) as distance,point.longtitude, point.latitude,express.province,express.city " \
                                 "FROM point_new,express,point " \
                                 "where ST_DWithin(ST_Transform(st_geomfromtext('POINT({0} {1})',4326),32650),ST_Transform(point_new.log_point,32650),30000) " \
                                 "and point.address = express.address " \
                                 "and express.address = point_new.address " \
                                 "order by distance,express.id;".format(lng, lat)

        cursor.execute(sql_query_nearby_nodes)  # 执行SQL
        res = cursor.fetchall()

        express_id = []
        express_address = []
        express_distance = []
        express_lng = []
        express_lat = []
        for r in res:
            id = r[0]
            address = r[1]
            distance = r[2]
            e_lng = r[3]
            e_lat = r[4]
            province = r[5]
            city = r[6]
            if (city in receiver_city or province in receiver_province) and address not in express_address:
                express_id.append(id)
                express_address.append(address)
                express_distance.append(distance)
                express_lng.append(e_lng)
                express_lat.append(e_lat)

        sql1 = "select point.longtitude, point.latitude, point.province, point.city " \
               "from express,point where express.id=%d and point.address = express.address" % (
                   nodeid)
        cursor.execute(sql1)  # 执行SQL
        res = cursor.fetchall()
        deliver_lng = res[0][0]
        deliver_lat = res[0][1]
        deliver_province = res[0][2]
        deliver_city = res[0][3]

        if deliver_lng < express_lng[0]:
            min_lng = deliver_lng
            max_lng = express_lng[0]
        else:
            min_lng = express_lng[0]
            max_lng = deliver_lng
        if deliver_lat < express_lat[0]:
            min_lat = deliver_lat
            max_lat = express_lat[0]
        else:
            min_lat = express_lat[0]
            max_lat = deliver_lat

        random_receiver = random.randint(int(len(express_id) * 2 / 3), len(express_id))
        i = random_receiver
        while not (min_lat < express_lat[i] < max_lat and min_lng < express_lng[i] < max_lng):
            i += 1
            if i == len(express_id) - 1:
                i = int(len(express_id) * 1 / 3)

        receiver_node = express_id[i]

        sql_query_deliver_point = "SELECT express.id,express.address,ST_Distance(ST_Transform(st_geomfromtext('POINT({0} {1})',4326), 32650), " \
                                  "ST_Transform(point_new.log_point, 32650)) as distance,point.longtitude, point.latitude,express.province,express.city " \
                                  "FROM point_new,express,point " \
                                  "where ST_DWithin(ST_Transform(st_geomfromtext('POINT({0} {1})',4326),32650),ST_Transform(point_new.log_point,32650),30000) " \
                                  "and point.address = express.address " \
                                  "and express.address = point_new.address " \
                                  "order by distance, express.id;".format(deliver_lng, deliver_lat)
        cursor.execute(sql_query_deliver_point)  # 执行SQL
        res = cursor.fetchall()

        d_express_id = []
        d_express_address = []
        d_express_distance = []
        d_express_lng = []
        d_express_lat = []
        for r in res:
            id = r[0]
            address = r[1]
            distance = r[2]
            e_lng = r[3]
            e_lat = r[4]
            province = r[5]
            city = r[6]
            if (city == deliver_city or province == deliver_province) and address not in d_express_address:
                d_express_id.append(id)
                d_express_address.append(address)
                d_express_distance.append(distance)
                d_express_lng.append(e_lng)
                d_express_lat.append(e_lat)

        random_deliver = random.randint(int(len(d_express_id) * 2 / 3), len(d_express_id))
        i = random_deliver
        while not (min_lat < d_express_lat[i] < max_lat and min_lng < d_express_lng[i] < max_lng):
            i += 1
            if i == len(d_express_id) - 1:
                i = int(len(d_express_id) * 1 / 3)

        deliver_node = d_express_id[i]

        ticks = int(round(time.time() * 1000))
        sql_insert_deliver = "insert into routeinfo(nodeid,orderid,sequenceid,arrivingtime) values({0},'{1}',1,'{2}')".format(
            nodeid, order_id, ticks)

        cursor.execute(sql_insert_deliver)  # 执行SQL
        conn.commit()

        sql_insert_deliver_next = "insert into routeinfo(nodeid,orderid,sequenceid) values(%d,'%s',2)" % (
            deliver_node, order_id)
        cursor.execute(sql_insert_deliver_next)  # 执行SQL
        conn.commit()

        sql_insert_receiver_next = "insert into routeinfo(nodeid,orderid,sequenceid) values(%d,'%s',3)" % (
            receiver_node, order_id)
        cursor.execute(sql_insert_receiver_next)  # 执行SQL
        conn.commit()

        sql_insert_receiver = "insert into routeinfo(nodeid,orderid,sequenceid) values(%d,'%s',4)" % (
            express_id[0], order_id)
        cursor.execute(sql_insert_receiver)  # 执行SQL
        conn.commit()

        sql_update_orderid = "update deliveryorder set orderstate=1,nodenumnow=1,nodestate=0,callbackstate=0 where id='{0}'".format(
            order_id)
        cursor.execute(sql_update_orderid)
        conn.commit()

        cursor.close()
        conn.close()
        return {"ifSuccess": True}
    except Exception as e:
        print("异常信息为：", e)
        conn.rollback()  # 回滚
        return {"ifSuccess": False}
