import utils
from database_con import *
import json
import psycopg2


def register(provide_username, provide_keyword, provide_name, phoneNum):
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()

    truth_username = utils.base64decode(provide_username)
    truth_keyword = utils.base64decode(provide_keyword)
    truth_name = utils.base64decode(provide_name)

    IfSuccess = True
    IfExist = False

    sql = "select * from dispatcher where \"username\"='{0}'".format(truth_username)
    try:
        cursor.execute(sql)  # 执行SQL
        res = cursor.fetchall()
        if (len(res) != 0):
            IfSuccess = False
            IfExist = True
        else:
            cursor1 = conn.cursor()
            sql1 = "INSERT INTO dispatcher VALUES('{0}','{1}','{2}','{3}')".format(truth_username, truth_keyword,
                                                                                   truth_name, phoneNum)
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

    sql = "select \"name\" from dispatcher where \"username\"='{0}' and \"keyword\"='{1}';" \
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

    sql = "select * from dispatcher where \"username\"='{0}' and \"name\"='{1}'".format(username, name)
    cursor.execute(sql)  # 执行SQL
    res = cursor.fetchall()
    if (len(res) == 0):
        return False
    else:
        return True


def query_near(lng, lat, dispatcher_city):
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()

    sql_query_nearby_nodes = "SELECT express.id,express.address,ST_Distance(ST_Transform(st_geomfromtext('POINT({0} {1})',4326), 32650), " \
                             "ST_Transform(point_new.log_point, 32650)) as distance,point.longtitude, point.latitude,express.province,express.city " \
                             "FROM point_new,express,point " \
                             "where ST_DWithin(ST_Transform(st_geomfromtext('POINT({0} {1})',4326),32650),ST_Transform(point_new.log_point,32650),5000) " \
                             "and point.address = express.address " \
                             "and express.address = point_new.address " \
                             "order by distance,express.id;".format(lng, lat)
    print(sql_query_nearby_nodes)
    try:
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
            if (city in dispatcher_city or province in dispatcher_city) and address not in express_address:
                express_id.append(id)
                express_address.append(address)
                express_distance.append(distance)
                express_lng.append(e_lng)
                express_lat.append(e_lat)

        express_num = len(express_id)
        nearby_nodes = []
        orders = []
        for i in range(express_num):
            e_id = express_id[i]
            sql_query_orders = "select t_order.id, t_add.receivername, t_add.phonenum, t_order.gooddescription,t_add.city," \
                               " t_add.addressdetail, t_add.addresslon, t_add.addresslat " \
                               "from deliveryorder as t_order, routeinfo, receiveraddressinfo as t_add " \
                               "where t_order.orderstate=2 and t_order.receivingoption=0 and routeinfo.nodeid = {0} " \
                               "and t_order.id = routeinfo.orderid and t_order.nodenumnow = routeinfo.sequenceid " \
                               "and t_order.receiveraddressid = t_add.id and t_order.receiverusername = t_add.accountusername" \
                .format(e_id)
            cursor.execute(sql_query_orders)  # 执行SQL
            res = cursor.fetchall()

            nearby_node = {"lng": express_lng[i], "lat": express_lat[i], "orderNums": len(res),
                           "address": express_address[i], "distance": str(int(express_distance[i])) + "米"}
            nearby_nodes.append(nearby_node)

            for r in res:
                order = {"id": r[0], "receiverName": r[1], "receiverPhoneNum": r[2], "goodDescription": r[3],
                         "receiverAddress": r[4] + r[5], "receiverLng": r[6], "receiverLat": r[7]}
                order["nodeAddress"] = express_address[i]
                order["distance"] = str(int(express_distance[i])) + "米"
                order["nodeLng"] = express_lng[i]
                order["nodeLat"] = express_lat[i]

                orders.append(order)

        result = {"nearby_nodes": nearby_nodes, "orders": orders}
        return json.dumps(result, ensure_ascii=False, indent=4)
    except Exception as e:
        print("异常信息为：", e)
        conn.rollback()  # 回滚


def grab(id, username):
    conn = psycopg2.connect(database=database,
                            user=user,
                            password=password,
                            host=host, port=port)
    cursor = conn.cursor()
    sql = "update deliveryorder set orderstate=3,dispatcherusername='%s' where id='%s'" % (username, id)
    try:
        cursor.execute(sql)  # 执行SQL
        conn.commit()
        text = {"ifSuccess": True}

    except Exception as e:
        print("异常信息为：", e)
        text = {"ifSuccess": False}
        conn.rollback()  # 回滚

    cursor.close()
    conn.close()
    return json.dumps(text, ensure_ascii=False, indent=4)
