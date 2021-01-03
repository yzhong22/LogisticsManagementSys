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


@app.route('/api/user/register', methods=['POST'])
def user_register():
    data = request.get_data()
    j_data = json.loads(data)
    provide_username = j_data['username']
    provide_keyword = j_data['keyword']
    provide_name = j_data['name']
    result = user.register(provide_username, provide_keyword, provide_name)
    return result


@app.route('/api/user/login', methods=['POST'])
def user_login_check():
    data = request.get_data()
    j_data = json.loads(data)
    provide_username = j_data['username']
    provide_keyword = j_data['keyword']
    result = user.login(provide_username, provide_keyword)
    return result


# return result


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
