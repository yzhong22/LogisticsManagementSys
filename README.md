# 放心递：物流管理系统

## 系统配置

- Python 3.6
- Chrome
- PostgreSQL 13.1
- PostGIS 3.1

## 使用说明

- 下载[数据库备份文件](https://pan.baidu.com/s/1eDBgKf9pAepLDfNyF8NjiQ)及部分示例数据（提取码：vq9r）

- 新建PostgreSQL连接及数据库，恢复数据库结构和数据

- 在database_con.py中配置数据库连接设置

- 运行main.py文件，启动服务器

- 浏览器进行测试

  - 买家登录入口：http://localhost:5000/users/login

    > ##### 已注册用于测试的买家
    >
    > - 钟源
    >   - 用户名：2018300003089
    >   - 密码：312725802

  - 卖家登录入口：http://localhost:5000/seller/login

    > ##### 已注册用于测试的卖家
    >
    > - 成都宽窄巷子熊猫点
    >   - 用户名：kzxzxm
    >   - 密码：123456
    > - 上海龙吴进口水果批发市场
    >   - 用户名：shlwsg
    >   - 密码：123456
    > - Apple官方（西湖店）
    >   - 用户名：applehzxh
    >   - 密码：123456
    > - 北京片皮烤鸭（武林店）
    >   - 用户名：bjppky
    >   - 密码：123456
    > - 阿迪达斯(森林摩尔折扣店)
    >   - 用户名：njadds
    >   - 密码：123456

  - 物流节点管理主页：http://localhost:5000/node

  - 派送骑手登录入口：http://localhost:5000/dispatcher/login

    > ##### 已注册的派送骑手
    >
    > - 赵强
    >   - 用户名：chengfenggui
    >   - 密码：123456

## 第三方框架及文档

- [Vue](https://cn.vuejs.org/)
- [Vue Baidu Map](https://dafrok.github.io/vue-baidu-map/#/zh/start/installation)

- [Element UI](https://element.eleme.cn/#/zh-CN/component/custom-theme)
- [百度地图API](http://lbsyun.baidu.com/index.php?title=jspopularGL)
- [axios](http://www.axios-js.com/)

