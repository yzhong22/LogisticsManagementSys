from flask import Flask, request, render_template, redirect, url_for, make_response
import utils
from models import user, seller, node, dispatcher
import json
import os
from PIL import Image

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
app = Flask('user_controller')


# 获取本地图片
@app.route('/api/img')
def get_imgs():
    file_name = request.args.get("file")
    file_type = request.args.get("type")
    w = int(request.args.get("width"))
    h = int(request.args.get("height"))
    basepath = os.path.dirname(__file__)  # 当前文件所在路径
    upload_path = os.path.join(basepath, 'static/img', file_name + '.' + file_type)
    temporal_path = os.path.join(basepath, 'static/img', file_name + '_temporal.png')

    img = Image.open(upload_path).resize((w, h), Image.ANTIALIAS)
    img.save(temporal_path)

    image_data = open(temporal_path, "rb").read()
    os.remove(temporal_path)  # 删除文件
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/png'
    return response


###############
### 用户部分 ###
###############

# 返回用户登录界面
@app.route('/users/login')
def users_login():
    return render_template('users/user_login.html')


# 返回用户注册界面
@app.route('/users/register')
def users_register():
    return render_template('users/user_register.html')


# 返回用户主页
@app.route('/users')
def users_welcome():
    id = request.args.get("username")
    name = request.args.get("name")

    try:
        tru_id = utils.base64decode(id)
        tru_name = utils.base64decode(name)
        res = user.check_login(tru_id, tru_name)

        if (res == True):
            return render_template('users/user_index.html')
        else:
            return redirect(url_for('users_login'))  # url重定向
    except:
        return redirect(url_for('users_login'))


# 用户注册
@app.route('/api/user/register', methods=['POST'])
def user_register():
    data = request.get_data()
    j_data = json.loads(data)
    provide_username = j_data['username']
    provide_keyword = j_data['keyword']
    provide_name = j_data['name']
    result = user.register(provide_username, provide_keyword, provide_name)
    return result


# 检验用户登录账号密码
@app.route('/api/user/login', methods=['POST'])
def user_login_check():
    data = request.get_data()
    j_data = json.loads(data)
    provide_username = j_data['username']
    provide_keyword = j_data['keyword']
    result = user.login(provide_username, provide_keyword)
    return result


# 查询所有地址
@app.route('/api/user/address/queryAll', methods=['GET'])
def user_query_all_address():
    username = request.args.get("username")
    result = user.address_query_all(username)
    return result


# 根据关键词检索地址
@app.route('/api/user/address/query', methods=['GET'])
def user_query_address():
    search_keyword = request.args.get("search_keyword")
    username = request.args.get("username")
    result = user.address_query(username, search_keyword)
    return result


# 添加地址
@app.route('/api/user/address/add', methods=['POST'])
def user_add_address():
    data = request.get_data()
    j_data = json.loads(data)
    id = j_data['id']
    accountUsername = j_data['accountUsername']
    receiverName = j_data['receiverName']
    province = j_data['province']
    city = j_data['city']
    addressdetail = j_data['addressDetail']
    addresslon = j_data['addressLon']
    addresslat = j_data['addressLat']
    phonenum = str(j_data['phoneNum'])
    result = user.add_address(id, accountUsername, receiverName, province, city, addressdetail, addresslon, addresslat,
                              phonenum)
    return result


# 删除地址
@app.route('/api/user/address/delete', methods=['DELETE'])
def user_delete_address():
    id = request.args.get("id")
    username = request.args.get("username")
    username = utils.base64decode(username)
    result = user.delete_address(id, username)
    return result


# 编辑地址
@app.route('/api/user/address/edit', methods=['PUT'])
def user_edit_address():
    data = request.get_data()
    j_data = json.loads(data)
    id = j_data['id']
    accountUsername = j_data['accountUsername']
    receiverName = j_data['receiverName']
    province = j_data['province']
    city = j_data['city']
    addressdetail = j_data['addressDetail']
    addresslon = j_data['addressLon']
    addresslat = j_data['addressLat']
    phonenum = str(j_data['phoneNum'])
    text = user.edit_address(id, accountUsername, receiverName, province, city, addressdetail, addresslon, addresslat,
                             phonenum)
    return text


# 查询所有卖家
@app.route('/api/user/seller/queryAll', methods=['GET'])
def query_all_seller():
    return seller.all_seller()


# 查询所有订单
@app.route('/api/user/order/queryAll', methods=['GET'])
def user_query_all_order():
    username = request.args.get("username")
    result = user.query_all_order(username)
    return result


# 添加订单
@app.route('/api/user/order/add', methods=['POST'])
def user_add_order():
    username = request.args.get("username")
    data = request.get_data()
    j_data = json.loads(data)
    id = j_data['id']
    receiverAddressId = j_data['receiverAddressId']
    deliverUsername = j_data['deliverUsername']
    goodDescription = j_data['goodDescription']
    receivingOption = j_data['receivingOption']
    result = user.add_order(id, receiverAddressId, deliverUsername, goodDescription, receivingOption, username)
    return result


# 查询未完成订单数量
@app.route('/api/user/order/unfinished/num', methods=['GET'])
def user_order_unfinished_num():
    username = request.args.get("username")
    result = user.order_unfinished_num(username)
    return result


# 根据关键词检索订单
@app.route('/api/user/order/query', methods=['GET'])
def user_order_query():
    search_keyword = request.args.get("search_keyword")
    username = request.args.get("username")
    result = user.query_order(search_keyword, username)
    return result


# 查询所有未完成的订单
@app.route('/api/user/order/unfinished/queryAll', methods=['GET'])
def user_unfinished_order_queryAll():
    username = request.args.get("username")
    result = user.query_all_unfinished_order(username)
    return result


@app.route('/api/user/order/confirmReceiving', methods=['GET'])
def user_order_confirmReceiving():
    id = request.args.get("id")
    result = user.confirm_receiving(id)
    return result


@app.route('/api/user/order/callback/apply', methods=['GET'])
def user_order_callback_apply():
    id = request.args.get("id")
    result = user.order_callback_apply(id)
    return result


@app.route('/api/user/order/changeReceivingOpt', methods=['POST'])
def user_order_changeReceivingOpt():
    id = request.args.get("id")
    result = user.order_changeReceivingOpt(id)
    return result


@app.route('/api/user/mapOrder/queryAll', methods=['GET'])
def user_mapOrder_queryAll():
    username = request.args.get("username")
    result = user.mapOrder_queryAll(username)
    return result


@app.route('/api/user/order/showCertainOrder')
def user_query_route():
    id = request.args.get("id")
    result = user.show_route(id)
    return result


@app.route('/api/user/unfinishedOrder/nearbyNodes', methods=['GET'])
def user_get_nearbynodes():
    id = request.args.get("id")
    result = user.query_user_nearbynodes(id)
    return result


@app.route('/api/user/unfinishedOrder/changeNode', methods=['POST'])
def user_change_last_node():
    data = request.get_data()
    j_data = json.loads(data)
    nodeId = j_data['nodeId']
    orderId = j_data['orderId']

    return user.change_last_node(orderId, nodeId)


###############
### 卖家部分 ###
###############

# 返回卖家注册页面
@app.route('/seller/register')
def seller_register_page():
    return render_template('seller/register.html')


# 返回卖家登录页面
@app.route('/seller/login')
def seller_login_page():
    return render_template('seller/login.html')


# 返回卖家主页
@app.route('/seller')
def seller_index_page():
    id = request.args.get("username")
    name = request.args.get("name")

    try:
        tru_id = utils.base64decode(id)
        tru_name = utils.base64decode(name)
        res = seller.check_login(tru_id, tru_name)

        if (res == True):
            return render_template('seller/index.html')
        else:
            return redirect(url_for('seller_login_page'))  # url重定向
    except:
        return redirect(url_for('seller_login_page'))


# 卖家注册
@app.route('/api/seller/register', methods=['POST'])
def seller_register():
    data = request.get_data()
    j_data = json.loads(data)
    provide_username = j_data['username']
    provide_keyword = j_data['keyword']
    provide_name = j_data['name']
    phoneNum = j_data['phoneNum']
    province = j_data['province']
    city = j_data['city']
    addressDetail = j_data['addressDetail']
    addressLon = j_data['addressLon']
    addressLat = j_data['addressLat']
    result = seller.register(provide_username, provide_keyword, provide_name, phoneNum, province, city, addressDetail,
                             addressLon, addressLat)
    return result


# 卖家登录检验（防止违法URL访问）
@app.route('/api/seller/login', methods=['POST'])
def seller_login_check():
    data = request.get_data()
    j_data = json.loads(data)
    provide_username = j_data['username']
    provide_keyword = j_data['keyword']
    result = seller.login(provide_username, provide_keyword)
    return result


# 获取卖家基本信息
@app.route('/api/seller/basicInfo')
def seller_basic_info():
    id = request.args.get("username")
    result = seller.basic_info(id)
    return result


@app.route('/api/seller/send/queryAll', methods=['GET'])
def seller_send_queryAll():
    username = request.args.get("username")
    result = seller.send_queryAll(username)
    return result


@app.route('/api/seller/send/query', methods=['GET'])
def seller_send_query():
    username = request.args.get("username")
    search_keyword = request.args.get("search_keyword")
    result = seller.send_query(username, search_keyword)
    return result


@app.route('/api/seller/send/nearbyNodes', methods=['GET'])
def seller_send_nearbynodes():
    username = request.args.get("username")
    result = seller.send_nearbynodes(username)
    return result


@app.route('/api/seller/order/queryAll', methods=['GET'])
def seller_order_queryAll():
    username = request.args.get("username")
    result = seller.order_queryall(username)
    return result


@app.route('/api/seller/order/query', methods=['GET'])
def seller_order_query():
    search_keyword = request.args.get("search_keyword")
    username = request.args.get("username")
    result = seller.order_query(search_keyword, username)
    return result


@app.route('/api/seller/order/callback/queryAll', methods=['GET'])
def seller_order_callback_queryAll():
    username = request.args.get("username")
    result = seller.order_callback_queryall(username)
    return result


@app.route('/api/seller/order/callback/query', methods=['GET'])
def seller_order_callback_query():
    username = request.args.get("username")
    search_keyword = request.args.get("search_keyword")
    result = seller.order_callback_query(username, search_keyword)
    return result


@app.route('/api/seller/order/callback/agree', methods=['GET'])
def seller_order_callback_agree():
    id = request.args.get("id")
    result = seller.order_callback_agree(id)
    return result


@app.route('/api/seller/order/callback/finish', methods=['POST'])
def seller_order_callback_finish():
    id = request.args.get("id")
    result = seller.order_callback_finish(id)
    return result


@app.route('/api/seller/send', methods=['POST'])
def get_provide_data():
    data = request.get_data()
    j_data = json.loads(data)
    id = j_data['id']
    chosennodeid = j_data['chosenNodeId']
    text = seller.make_route(chosennodeid, id)
    return text


###############
### 中间节点 ###
###############

@app.route('/node')
def node_index():
    return render_template('node/index.html')


@app.route('/api/node/options/query')
def node_search():
    keyword = request.args.get("search_keyword")
    result = node.search_node_options(keyword)
    return result


@app.route('/api/node/info')
def node_info():
    id = request.args.get("id")
    result = node.query_node_detail(id)
    return result


@app.route('/api/node/receive/queryAll', methods=['GET'])
def node_receive_queryAll():
    nodeid = request.args.get("nodeId")
    result = node.receive_queryAll(nodeid)
    return result


@app.route('/api/node/receive/query', methods=['GET'])
def node_receive_query():
    nodeid = request.args.get("nodeId")
    search_keyword = request.args.get("search_keyword")
    result = node.receive_query(nodeid, search_keyword)
    return result


@app.route('/api/node/receive/confirm', methods=['POST'])
def node_receive_confirm():
    id = request.args.get("id")
    result = node.receive_confirm(id)
    return result


@app.route('/api/node/send/queryAll', methods=['GET'])
def node_send_queryAll():
    nodeid = request.args.get("nodeId")
    result = node.send_queryAll(nodeid)
    return result


@app.route('/api/node/send/query', methods=['GET'])
def node_send_query():
    nodeid = request.args.get("nodeId")
    search_keyword = request.args.get("search_keyword")
    result = node.send_query(nodeid, search_keyword)
    return result


@app.route('/api/node/send/confirm', methods=['POST'])
def node_send_confirm():
    id = request.args.get("id")
    result = node.send_confirm(id)
    return result


@app.route('/api/node/send/changeNext', methods=['POST'])
def node_send_changenext():
    id = request.args.get("id")
    nextnodeid = request.args.get("nextNodeId")
    result = node.send_changenext(id, nextnodeid)
    return result


@app.route('/api/node/fetch/queryAll', methods=['GET'])
def node_fetch_queryAll():
    nodeid = request.args.get("nodeId")
    result = node.fetch_queryAll(nodeid)
    return result


@app.route('/api/node/fetch/query', methods=['GET'])
def node_fetch_query():
    nodeid = request.args.get("nodeId")
    search_keyword = request.args.get("search_keyword")
    result = node.fetch_query(nodeid, search_keyword)
    return result


@app.route('/api/node/dispatch/queryAll', methods=['GET'])
def node_dispatch_queryAll():
    nodeid = request.args.get("nodeId")
    result = node.dispatch_queryAll(nodeid)
    return result


@app.route('/api/node/dispatch/query', methods=['GET'])
def node_dispatch_query():
    nodeid = request.args.get("nodeId")
    search_keyword = request.args.get("search_keyword")
    result = node.dispatch_query(nodeid, search_keyword)
    return result


###############
### 派送骑手 ###
###############

# 返回用户登录界面
@app.route('/dispatcher/login')
def dispatcher_login():
    return render_template('dispatcher/login.html')


# 返回用户注册界面
@app.route('/dispatcher/register')
def dispatcher_register():
    return render_template('dispatcher/register.html')


# 返回用户主页
@app.route('/dispatcher')
def dispatcher_welcome():
    id = request.args.get("username")
    name = request.args.get("name")

    try:
        tru_id = utils.base64decode(id)
        tru_name = utils.base64decode(name)
        res = dispatcher.check_login(tru_id, tru_name)

        if (res == True):
            return render_template('dispatcher/index.html')
        else:
            return redirect(url_for('dispatcher_login'))  # url重定向
    except:
        return redirect(url_for('dispatcher_login'))


@app.route('/api/dispatcher/register', methods=['POST'])
def dispatcher_register_upload():
    data = request.get_data()
    j_data = json.loads(data)
    provide_username = j_data['username']
    provide_keyword = j_data['keyword']
    provide_name = j_data['name']
    phone_num = j_data['phoneNum']
    result = dispatcher.register(provide_username, provide_keyword, provide_name, phone_num)
    return result


@app.route('/api/dispatcher/login', methods=['POST'])
def dispatcher_login_check():
    data = request.get_data()
    j_data = json.loads(data)
    provide_username = j_data['username']
    provide_keyword = j_data['keyword']
    result = dispatcher.login(provide_username, provide_keyword)
    return result


@app.route('/api/dispatcher/queryNear', methods=['GET'])
def dispatcher_querynear():
    lng = request.args.get("lng")
    lat = request.args.get("lat")
    city = request.args.get("city")
    result = dispatcher.query_near(lng, lat, city)
    return result


@app.route('/api/dispatcher/grab', methods=['POST'])
def dispatcher_grab():
    data = request.get_data()
    j_data = json.loads(data)
    id = j_data['id']
    username = j_data['username']
    result = dispatcher.grab(id, username)
    return result

# from database_con import *
# import json
# import psycopg2


# @app.route('/process')
# def process_index():
#     return render_template('test.html')
#
#
# @app.route('/api/get', methods=['GET'])
# def get():
#     conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
#     cursor = conn.cursor()
#     sql = "select id,address,city,province from express"
#     cursor.execute(sql)  # 执行SQL
#     res = cursor.fetchall()
#     result = []
#     for e in res:
#         id = e[0]
#         city = e[2]
#         address = e[1]
#         province = e[3]
#         text = {"id": id, "city": city, "address": address, "province": province}
#         result.append(text)
#     return json.dumps(result)
#
#
# @app.route('/api/process', methods=['POST'])
# def process():
#     conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
#     cursor = conn.cursor()
#
#     data = request.get_data()
#     j_data = json.loads(data)
#     for e in j_data:
#         id = e["id"]
#         province = e["province"]
#         city = e["city"]
#         address = e["address"]
#         lng = e["lng"]
#         lat = e["lat"]
#         sql = "INSERT INTO express_geom(id,province,city,address,geom)" \
#               "VALUES({0},'{1}','{2}','{3}','{4}')"
#     cursor.execute(sql)  # 执行SQL
#     return 0
