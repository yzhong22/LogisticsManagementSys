from flask import Flask, request, render_template
import utils

app = Flask('user_controller')


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
    id = request.args.get("user_id")
    if (id != None):
        return render_template('users/user_index.html')
    else:
        return users_login()

###############
### 卖家部分 ###
###############

# 返回卖家注册
@app.route('/seller/register')
def seller_register():
    return render_template('seller/register.html')