import utils
from database_con import *
import json
import psycopg2
import time


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


def address_query_all(username):
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    sql = "select * from receiveraddressinfo"
    id = []
    accountusername = []
    province = []
    city = []
    addressdetail = []
    addresslon = []
    addresslat = []
    phonenum = []
    receivername = []
    try:
        cursor.execute(sql)  # 执行SQL
        res = cursor.fetchall()
        for list in res:
            id.append(list[0])
            accountusername.append(list[1])
            province.append(list[3])
            city.append(list[4])
            addressdetail.append(list[5])
            addresslon.append(list[6])
            addresslat.append(list[7])
            phonenum.append(list[8])
            receivername.append(list[2])
    except Exception as e:
        print("异常信息为：", e)
        conn.rollback()  # 回滚
    cursor.close()
    conn.close()
    provide_username = username
    para = []
    truth_username = utils.base64decode(provide_username)
    for i in range(len(id)):
        if (truth_username == accountusername[i]):
            text = {"id": id[i], "accountUsername": provide_username, "receiverName": receivername[i],
                    "province": province[i], "city": city[i], "addressDetail": addressdetail[i],
                    "addresslon": addresslon[i], "addresslat": addresslat[i], "phoneNum": phonenum[i]
                    }
            para.append(text)
    return json.dumps(para, ensure_ascii=False, indent=4)


def address_query(username, search_keyword):
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()

    provide_username = username
    para = []
    truth_username = utils.base64decode(provide_username)

    id = []
    accountusername = []
    province = []
    city = []
    addressdetail = []
    addresslon = []
    addresslat = []
    phonenum = []
    receivername = []

    sql = "select * from receiveraddressinfo where accountusername='{0}'".format(truth_username)
    try:
        cursor.execute(sql)  # 执行SQL
        res = cursor.fetchall()
        for list in res:
            id.append(list[0])
            accountusername.append(list[1])
            province.append(list[3])
            city.append(list[4])
            addressdetail.append(list[5])
            addresslon.append(list[6])
            addresslat.append(list[7])
            phonenum.append(list[8])
            receivername.append(list[2])
    except Exception as e:
        print("异常信息为：", e)
        conn.rollback()  # 回滚

    cursor.close()
    conn.close()

    for i in range(len(id)):
        if (search_keyword in addressdetail[i] or search_keyword in province[i] or search_keyword in city[i]):
            text = {"id": id[i], "accountUsername": provide_username, "receiverName": receivername[i],
                    "province": province[i], "city": city[i], "addressDetail": addressdetail[i],
                    "addresslon": addresslon[i], "addresslat": addresslat[i], "phoneNum": phonenum[i]
                    }
            para.append(text)
    return json.dumps(para, ensure_ascii=False, indent=4)


def add_address(id, accountUsername, receiverName, province, city, addressdetail, addresslon, addresslat, phonenum):
    truth_username = utils.base64decode(accountUsername)
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    sql = (
              'INSERT INTO receiveraddressinfo(id,accountusername,receivername,province,city,addressdetail,addresslon,addresslat,phonenum)'
              "VALUES('%d','%s','%s','%s','%s','%s','%lf','%lf','%s')") % (
              id, truth_username, receiverName, province, city, addressdetail, addresslon, addresslat, phonenum)
    try:
        cursor.execute(sql)  # 执行SQL
        conn.commit()
        text = {"ifSucess": True}
    except Exception as e:
        print("异常信息为：", e)
        text = {"ifSucess": False}
        conn.rollback()  # 回滚
    cursor.close()
    conn.close()
    return json.dumps(text, ensure_ascii=False, indent=4)


def delete_address(id, username):
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    id = int(id)
    sql0 = "select id,accountusername from receiveraddressinfo where id=%d and accountusername='%s'" % (id, username)

    try:
        cursor.execute(sql0)  # 执行SQL
        res = cursor.fetchall()
        if (len(res) == 0):
            text = {"ifSucess": False}
            return json.dumps(text, ensure_ascii=False, indent=4)
    except Exception as e:
        print("异常信息为：", e)
        conn.rollback()  # 回滚

    sql = "delete from receiveraddressinfo where id=%d and accountusername='%s'" % (id, username)
    try:
        cursor.execute(sql)  # 执行SQL
        conn.commit()
        text = {"ifSucess": True}
    except Exception as e:
        print("异常信息为：", e)
        text = {"ifSucess": False}
        conn.rollback()  # 回滚
    cursor.close()
    conn.close()
    return json.dumps(text, ensure_ascii=False, indent=4)


def edit_address(id, accountUsername, receiverName, province, city, addressdetail, addresslon, addresslat, phonenum):
    truth_username = utils.base64decode(accountUsername)
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    id = int(id)
    sql0 = "select id,accountusername from receiveraddressinfo where id=%d and accountusername='%s'" % (
        id, truth_username)
    id_new = []
    username_new = []
    try:
        cursor.execute(sql0)  # 执行SQL
        res = cursor.fetchall()
        for list in res:
            id_new.append(list[0])
            username_new.append(list[1])
    except Exception as e:
        print("异常信息为：", e)
        conn.rollback()  # 回滚
    if (len(id_new) == 0):
        text = {"ifSucess": False}
        return json.dumps(text, ensure_ascii=False, indent=4)
    sql = "update receiveraddressinfo set receivername='%s',province='%s',city='%s',addressdetail='%s',addresslon=%lf,addresslat=%lf,phonenum='%s'" \
          "where id=%d and accountusername='%s'" % (
              receiverName, province, city, addressdetail, addresslon, addresslat, phonenum, id, truth_username)
    try:
        cursor.execute(sql)  # 执行SQL
        conn.commit()
        text = {"ifSucess": True}
    except Exception as e:
        print("异常信息为：", e)
        text = {"ifSucess": False}
        conn.rollback()  # 回滚
    cursor.close()
    conn.close()
    return json.dumps(text, ensure_ascii=False, indent=4)


########
## 订单部分
########
def query_all_order(username):
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    provide_username = username
    truth_username = utils.base64decode(provide_username)

    para = []

    sql = "select torder.id,torder.gooddescription,tadd.receivername," \
          "deliver.name,tadd.city,tadd.addressdetail,torder.entrytime,torder.callbackstate," \
          "torder.orderstate,torder.deschangedtimes,torder.receivingoption " \
          "from receiveraddressinfo as tadd,deliveryorder as torder,deliver " \
          "where torder.receiverusername='{0}' " \
          "and tadd.accountusername=torder.receiverusername " \
          "and torder.receiveraddressid = tadd.id " \
          "and deliver.username=torder.deliverusername".format(
        truth_username)

    try:
        cursor.execute(sql)  # 执行SQL
        res = cursor.fetchall()
        for list in res:
            text = {"id": list[0], "accountUsername": provide_username, "goodDescription": list[1],
                    "receiverName": list[2], "deliverName": list[3],
                    "addressDetail": list[4] + list[5],
                    "entryTime": list[6], "callbackState": list[7], "orderState": list[8],
                    "desChangedTimes": list[9],
                    "receivingOption": list[10]
                    }
            para.append(text)
    except Exception as e:
        print("异常信息为：", e)
        conn.rollback()

    cursor.close()
    conn.close()

    return json.dumps(para, ensure_ascii=False, indent=4)


def add_order(id, receiverAddressId, deliverUsername, goodDescription, receivingOption, username):
    truth_username = utils.base64decode(username)
    truth_deliverusername = utils.base64decode(deliverUsername)
    receiverAddressId = int(receiverAddressId)
    receivingOption = int(receivingOption)
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()

    t = time.time()
    now_time = round(t * 1000)

    sql = (
              'INSERT INTO deliveryorder(id,receiveraddressid,receiverusername,deliverusername,gooddescription,receivingoption,'
              'callbackstate,orderstate,deschangedtimes,entrytime)'
              "VALUES('%s',%d,'%s','%s','%s',%d,0,0,0,%d)") % (
              id, receiverAddressId, truth_username, truth_deliverusername, goodDescription, receivingOption, now_time)
    try:
        cursor.execute(sql)  # 执行SQL
        conn.commit()
        text = {"ifSucess": True}
    except Exception as e:
        print("异常信息为：", e)
        text = {"ifSucess": False}
        conn.rollback()  # 回滚
    cursor.close()
    conn.close()
    return json.dumps(text, ensure_ascii=False, indent=4)


def order_unfinished_num(username):
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    truth_username = utils.base64decode(username)
    sql = "select * from deliveryorder where receiverusername='%s' and orderstate!=5" % (truth_username)
    unfinished_num = 0
    try:
        cursor.execute(sql)  # 执行SQL
        res = cursor.fetchall()
        unfinished_num = len(res)

        text = {"orderNum": unfinished_num}
        cursor.close()
        conn.close()
        return json.dumps(text, ensure_ascii=False, indent=4)
    except Exception as e:
        print("异常信息为：", e)
        conn.rollback()  # 回滚


def query_order(search_keyword, username):
    para = []
    all_order = json.loads(query_all_order(username))
    for order in all_order:
        if (search_keyword in order["goodDescription"] or search_keyword in order["receiverName"] or
                search_keyword in order["deliverName"] or search_keyword in order["addressDetail"]):
            para.append(order)
    return json.dumps(para, ensure_ascii=False, indent=4)


def query_all_unfinished_order(username):
    para = []
    all_order = json.loads(query_all_order(username))

    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()

    for order in all_order:
        if (order["orderState"] != 5):
            sql = "select express.address from routeinfo as route, express where" \
                  " express.id=route.nodeid and route.orderid='{0}' order by route.sequenceid desc".format(
                order["id"])
            try:
                cursor.execute(sql)  # 执行SQL
                res = cursor.fetchall()
                if order["orderState"] == 4:
                    order["fetchAddress"] = "该订单已退货"
                elif len(res) == 0:
                    order["fetchAddress"] = "尚未生成路径"
                elif order["receivingOption"] == 0:
                    order["fetchAddress"] = "该订单将由骑手派送"
                else:
                    order["fetchAddress"] = res[0][0]
            except Exception as e:
                print("异常信息为：", e)
                conn.rollback()  # 回滚

            para.append(order)
    return json.dumps(para, ensure_ascii=False, indent=4)


def confirm_receiving(id):
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    sql = "update deliveryorder set orderstate=5 where id='%s' " % (id)
    try:
        cursor.execute(sql)  # 执行SQL
        conn.commit()
        text = {"ifSuccess": True}

        ticks = int(round(time.time() * 1000))
        sql_set_finish_time = "update deliveryorder set finishtime='{0}' where id='{1}'".format(ticks, id)
        cursor.execute(sql_set_finish_time)
        conn.commit()
    except Exception as e:
        print("异常信息为：", e)
        text = {"ifSuccess": False}
        conn.rollback()  # 回滚
    cursor.close()
    conn.close()
    return json.dumps(text, ensure_ascii=False, indent=4)


def order_callback_apply(id):
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    sql = "select * from deliveryorder where id='%s' " % (id)
    orderstate = None
    try:
        cursor.execute(sql)  # 执行SQL
        res = cursor.fetchall()
        orderstate = res[0][6]
    except Exception as e:
        print("异常信息为：", e)
        conn.rollback()  # 回滚
    if (orderstate is None):
        text = {"ifSuccess": False, "content": "未知错误，请联系管理员！"}
    elif (orderstate == 0):
        text = {"ifSuccess": True}
        sql1 = "update deliveryorder set orderstate=5 where id='%s' " % (id)
        sql2 = "update deliveryorder set callbackstate=3 where id='%s' " % (id)
        try:
            cursor.execute(sql1)  # 执行SQL
            conn.commit()
        except Exception as e:
            print("异常信息为：", e)
            conn.rollback()  # 回滚
        try:
            cursor.execute(sql2)  # 执行SQL
            conn.commit()
        except Exception as e:
            print("异常信息为：", e)
            conn.rollback()  # 回滚
    elif (orderstate == 1):
        text = {"ifSuccess": True}
        sql1 = "update deliveryorder set orderstate=4 where id='%s' " % (id)
        sql2 = "update deliveryorder set callbackstate=1 where id='%s' " % (id)
        try:
            cursor.execute(sql1)  # 执行SQL
            conn.commit()
        except Exception as e:
            print("异常信息为：", e)
            conn.rollback()  # 回滚
        try:
            cursor.execute(sql2)  # 执行SQL
            conn.commit()
        except Exception as e:
            print("异常信息为：", e)
            conn.rollback()  # 回滚
    elif (orderstate == 2):
        text = {"ifSuccess": False, "content": "订单已到达，不能申请退货！"}
    elif (orderstate == 3):
        text = {"ifSuccess": False, "content": "订单正在派送中，不能申请退货！"}
    elif (orderstate == 4):
        text = {"ifSuccess": False, "content": "订单正在退货中，无法反复申请！"}
    else:
        text = {"ifSuccess": False, "content": "订单已经完成，无法申请退货！"}
    cursor.close()
    conn.close()
    return json.dumps(text, ensure_ascii=False, indent=4)


def order_changeReceivingOpt(id):
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    sql = "select receivingoption from deliveryorder where id='%s'" % (id)
    receving_option = 0
    try:
        cursor.execute(sql)  # 执行SQL
        res = cursor.fetchall()
        receving_option = res[0][0]
    except Exception as e:
        print("异常信息为：", e)
        conn.rollback()  # 回滚
    receving_option = 1 - receving_option
    sql1 = "update deliveryorder set receivingoption={0} where id='{1}'".format(receving_option, id)

    try:
        cursor.execute(sql1)  # 执行SQL
        conn.commit()
        text = {"ifSuccess": True}
    except Exception as e:
        print("异常信息为：", e)
        text = {"ifSuccess": False}
        conn.rollback()  # 回滚
    cursor.close()
    conn.close()
    return json.dumps(text, ensure_ascii=False, indent=4)


def mapOrder_queryAll(username):
    truth_username = utils.base64decode(username)
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    try:
        sql = "select id,nodenumnow,gooddescription from deliveryorder where receivingoption=1 and orderstate=2 and receiverusername='%s'" % (
            truth_username)
        cursor.execute(sql)  # 执行SQL
        res = cursor.fetchall()

        id = []
        nodenumnow = []
        gooddescription = []
        node_addressdetail = []
        nodelon = []
        nodelat = []
        isgroup = []
        for list in res:
            id.append(list[0])
            nodenumnow.append(list[1])
            gooddescription.append(list[2])

        nodeid = []
        for i in range(len(id)):
            sql1 = "select nodeid from routeinfo where orderid='%s' and sequenceid=%d" % (id[i], nodenumnow[i])
            cursor.execute(sql1)  # 执行SQL
            res = cursor.fetchall()

            node_id = res[0][0]
            nodeid.append(node_id)

            sql2 = "select express.address, point.longtitude, point.latitude " \
                   "from express,point where express.id={0} and express.address = point.address".format(
                node_id)

            cursor.execute(sql2)  # 执行SQL
            res = cursor.fetchall()
            node_addressdetail.append(res[0][0])

            nodelon.append(res[0][1])
            nodelat.append(res[0][2])
            isgroup.append(False)

        basicinfo = []
        for i in range(len(id)):
            text = {"id": id[i], "addressDetail": (node_addressdetail[i]),
                    "goodDescription": gooddescription[i],
                    "nodeLon": nodelon[i], "nodeLat": nodelat[i]}
            basicinfo.append(text)

        mapinfo = []
        groupid = []
        groupnumber = 1
        for i in range(len(id)):
            groupid.append(0)
        for i in range(len(id)):
            if (isgroup[i] == True):
                continue

            isgroup[i] = True
            groupid[i] = groupnumber
            for j in range(len(id)):
                if (i == j or isgroup[j] == True):
                    continue
                if (nodeid[i] == nodeid[j]):
                    isgroup[j] = True
                    groupid[j] = groupnumber
            groupnumber += 1
        groupnumber -= 1

        for i in range(groupnumber):
            groupnum = i + 1
            orders = []
            ordernum = 0
            for j in range(len(groupid)):
                if (groupid[j] == groupnum):
                    ordernum += 1
                    nodeaddress = node_addressdetail[j]
                    nodeLon = nodelon[j]
                    nodeLat = nodelat[j]
                    text = {"orderId": id[j], "orderGood": gooddescription[j]}
                    orders.append(text)
            text = {"nodeAddress": nodeaddress, "nodeLon": nodeLon, "nodeLat": nodeLat, "orderNum": ordernum,
                    "orders": orders}
            mapinfo.append(text)
        final_result = {"basicInfo": basicinfo, "mapInfo": mapinfo}
        return json.dumps(final_result, ensure_ascii=False, indent=4)
    except Exception as e:
        print("异常信息为：", e)
        conn.rollback()  # 回滚


def show_route(id):
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    try:
        # 查询收货人
        sql_select_receiver = "select t_add.receivername, t_add.city, t_add.addressdetail, t_add.addresslon, t_add.addresslat, t_order.orderstate, " \
                              "t_order.entrytime, t_order.finishtime, t_order.receivingoption, t_order.dispatcherusername " \
                              "from deliveryorder as t_order, receiveraddressinfo as t_add " \
                              "where t_order.id='{0}' and t_order.receiverusername=t_add.accountusername " \
                              "and t_order.receiveraddressid = t_add.id" \
            .format(id)
        cursor.execute(sql_select_receiver)  # 执行SQL
        res = cursor.fetchall()
        receiver = {"name": res[0][0], "address": res[0][1] + res[0][2], "lng": res[0][3], "lat": res[0][4]}
        order_state = int(res[0][5])
        entry_time = int(res[0][6])
        finish_time = res[0][7]
        receving_option = int(res[0][8])
        dispatcher_username = res[0][9]

        # 查询发货人
        sql_select_deliver = "select deliver.name, deliver.city, deliver.addressdetail, deliver.addresslon, deliver.addresslat " \
                             "from deliveryorder as t_order, deliver " \
                             "where t_order.id='{0}' and t_order.deliverusername = deliver.username" \
            .format(id)
        cursor.execute(sql_select_deliver)  # 执行SQL
        res = cursor.fetchall()
        deliver = {"name": res[0][0], "address": res[0][1] + res[0][2], "lng": res[0][3], "lat": res[0][4]}

        # 查询路由
        sql_select_nodes = "select express.id, express.address,routeinfo.arrivingtime,routeinfo.leavingtime  " \
                           "from routeinfo, express " \
                           "where routeinfo.orderid = '{0}' and routeinfo.nodeid = express.id " \
                           "order by routeinfo.sequenceid" \
            .format(id)
        cursor.execute(sql_select_nodes)  # 执行SQL
        res = cursor.fetchall()

        nodes = []
        node_times = []
        arrived_node_address = []
        for r in res:
            express_id = r[0]
            express_address = r[1]
            arriving_time = r[2]
            leaving_time = r[3]

            node_times.append({"arrive": arriving_time, "leave": leaving_time})

            sql_select_loc = "select longtitude, latitude " \
                             "from point " \
                             "where address = '{0}'".format(express_address)

            cursor.execute(sql_select_loc)  # 执行SQL
            res_loc = cursor.fetchall()
            nodes.append({"id": express_id, "address": express_address, "lng": res_loc[0][0], "lat": res_loc[0][1]})

        deliveryInfo = []
        deliveryInfo.append({"content": "商品已下单", "timestamp": timestamp2date(entry_time), "event": "create"})

        now_info = {"content": "商品已下单", "lon": receiver["lng"], "lat": receiver["lat"]}

        if order_state >= 1:
            if len(nodes) == 0 and order_state == 4:
                deliveryInfo.append({
                    "content": "商品进入退货流程",
                    "timestamp": deliveryInfo[len(deliveryInfo) - 1]["timestamp"],
                    "event": "callback"
                })
                now_info = {"content": "商品已退货", "lon": deliver["lng"], "lat": deliver["lat"]}

            for i in range(len(nodes)):
                arriving_time = node_times[i]["arrive"]
                leaving_time = node_times[i]["leave"]
                address = nodes[i]["address"]

                # 判断第一个节点
                if i == 0:
                    if order_state == 4 and arriving_time is None:
                        deliveryInfo.append({
                            "content": "商品进入退货流程",
                            "timestamp": deliveryInfo[len(deliveryInfo) - 1]["timestamp"],
                            "event": "callback"
                        })
                        now_info = {"content": "商品已退货", "lon": deliver["lng"], "lat": deliver["lat"]}

                    elif arriving_time is not None:
                        deliveryInfo.append(
                            {"content": "商品已发货", "timestamp": timestamp2date(arriving_time),
                             "event": "sendOut"})

                if address in arrived_node_address and order_state == 4:
                    deliveryInfo.append({
                        "content": "商品进入退货流程",
                        "timestamp": deliveryInfo[len(deliveryInfo) - 1]["timestamp"],
                        "event": "callback"
                    })
                    now_info = {"content": "商品已退货", "lon": deliver["lng"], "lat": deliver["lat"]}

                if arriving_time is not None:
                    deliveryInfo.append(
                        {"content": "【" + address + "】您的快递已到达",
                         "timestamp": timestamp2date(arriving_time), "event": "normal"})
                    now_info = {"content": "商品已到达 " + address, "lon": nodes[i]["lng"], "lat": nodes[i]["lat"]}

                if leaving_time is not None:
                    deliveryInfo.append(
                        {"content": "【" + address + "】您的快递已发出", "timestamp": timestamp2date(leaving_time),
                         "event": "normal"})
                    now_info = {"content": "商品已离开 " + address, "lon": nodes[i]["lng"], "lat": nodes[i]["lat"]}

                arrived_node_address.append(address)

            # 商品到达最后一个节点
            nodes_num = len(nodes)
            if order_state >= 2 and nodes_num > 0 and order_state != 4:
                nodes_num -= 1
                deliveryInfo.append({
                    "content": deliveryInfo[len(deliveryInfo) - 1]["content"] + "终点站",
                    "timestamp": deliveryInfo[len(deliveryInfo) - 1]["timestamp"],
                    "event": "arrive"
                })

                now_info = {"content": "商品已到达终点站 " + nodes[nodes_num]["address"], "lon": nodes[nodes_num]["lng"],
                            "lat": nodes[nodes_num]["lat"]}

                if receving_option == 1:
                    deliveryInfo.append({
                        "content": "【代收点】您的快递暂存于 " + arrived_node_address[
                            len(arrived_node_address) - 1] + " 快递点，请及时领取！",
                        "timestamp": deliveryInfo[len(deliveryInfo) - 1]["timestamp"],
                        "event": "fetch"
                    })
                    now_info = {"content": "商品暂存于 " + nodes[nodes_num]["address"], "lon": nodes[nodes_num]["lng"],
                                "lat": nodes[nodes_num]["lat"]}

                if receving_option == 0 and dispatcher_username is not None:
                    sql_select_dispatcher = "select dispatcher.name, phonenum from dispatcher where username = '{0}'".format(
                        dispatcher_username)
                    cursor.execute(sql_select_dispatcher)
                    res = cursor.fetchall()
                    dispatcher_name = res[0][0]
                    dispatcher_phone_num = res[0][1]

                    deliveryInfo.append({
                        "content": "【派送中】您的快递正由 " + dispatcher_name + " 骑手进行派送，联系方式 " + dispatcher_phone_num + " ，请注意查收！",
                        "timestamp": deliveryInfo[len(deliveryInfo) - 1]["timestamp"],
                        "event": "dispatch"
                    })
                    now_info = {"content": "商品正由骑手 " + dispatcher_name + " 派送", "lon": nodes[nodes_num]["lng"],
                                "lat": nodes[nodes_num]["lat"]}

            if order_state == 5 and finish_time is not None:
                deliveryInfo.append({
                    "content": "您的订单已完成！",
                    "timestamp": timestamp2date(int(finish_time)),
                    "event": "finish"
                })
                now_info = {"content": "订单已完成！", "lon": receiver["lng"], "lat": receiver["lat"]}

        result = {"receiver": receiver, "deliver": deliver,
                  "route": {"node": nodes, "deliveryInfo": deliveryInfo, "now": now_info}}
        return json.dumps(result)
    except Exception as e:
        print("异常信息为：", e)
        conn.rollback()  # 回滚


def timestamp2date(timestamp):
    now = int(timestamp)
    now = float(now / 1000)
    timeArray = time.localtime(now)
    return str(time.strftime("%Y-%m-%d %H:%M:%S", timeArray))


def query_user_nearbynodes(id):
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    sql = "select t_add.city, t_add.province, t_add.addresslon, t_add.addresslat,t_add.addressdetail" \
          " from receiveraddressinfo as t_add, deliveryorder as t_order" \
          " where t_order.id='{0}' and t_order.receiveraddressid = t_add.id " \
          "and t_order.receiverusername = t_add.accountusername" \
        .format(id)
    try:
        cursor.execute(sql)  # 执行SQL
        res = cursor.fetchall()
        province = res[0][1]
        city = res[0][0]
        user_lon = res[0][2]
        user_lat = res[0][3]
        address_detail = res[0][4]

        sql = "SELECT express.id,express.address,ST_Distance(ST_Transform(st_geomfromtext('POINT({0} {1})',4326), 32650), " \
              "ST_Transform(point_new.log_point, 32650)) as distance,point.longtitude, point.latitude,express.province,express.city " \
              "FROM point_new,express,point " \
              "where ST_DWithin(ST_Transform(st_geomfromtext('POINT({0} {1})',4326),32650),ST_Transform(point_new.log_point,32650),5000) " \
              "and point.address=express.address " \
              "and express.address=point_new.address " \
              "order by distance,express.id;".format(user_lon, user_lat)

        options = []
        all_address = []

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

        user_info = {"address": city + address_detail, "lng": user_lon, "lat": user_lat}
        result = {"user_info": user_info, "options": options}

        return json.dumps(result)

    except Exception as e:
        print("异常信息为：", e)
        conn.rollback()  # 回滚


def change_last_node(orderid, nodeid):
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    try:
        sql = "select * from routeinfo where orderid='{0}'".format(orderid)
        cursor.execute(sql)
        res = cursor.fetchall()
        node_num = len(res)

        sql_update = "update routeinfo set nodeid = {0} where sequenceid ={1} and orderid='{2}'".format(nodeid,
                                                                                                         node_num,
                                                                                                         orderid)
        cursor.execute(sql_update)
        conn.commit()
        return {"ifSuccess": True}

    except Exception as e:
        print("异常信息为：", e)
        conn.rollback()  # 回滚
        return {"ifSuccess": False}
