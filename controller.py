from flask import Flask, request, render_template, redirect, url_for
import utils
import models.user as user
import models.seller as seller
import json
import os

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
app = Flask('user_controller')


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

# 返回卖家注册
@app.route('/seller/register')
def seller_register_page():
    return render_template('seller/register.html')


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


@app.route('/api/seller/login', methods=['POST'])
def seller_login_check():
    data = request.get_data()
    j_data = json.loads(data)
    provide_username = j_data['username']
    provide_keyword = j_data['keyword']
    result = seller.login(provide_username, provide_keyword)
    return result


@app.route('/api/seller/basicInfo')
def seller_basic_info():
    id = request.args.get("username")
    result = seller.basic_info(id)
    return result
