### 用户部分

#### 登录部分

##### 用户注册

类型：POST

url：/api/user/register

说明：用户提交用户名和密码，后端根据地址解析参数并解码，存入数据库

参数：username（编码过)、keyword（编码过）、name

注意事项：添加时要对username是否存在进行检查

示例：

- url: /api/user/register

- 附带json：

```json
// 原始数据
{
		"username":"chengfenggui",
		"keyword":"123456",
		"name":"钟源"
}

//  实际传送
{
		"username":"Y2hlbmdmZW5nZ3Vp",
		"keyword":"MTIzNDU2",
		"name":"6ZKf5rqQ"
}
```

- 回送：

```json
//  正常状态
{
		"ifSucess":true,
    "ifExist":false
}

//  用户名已存在
{
    "ifSucess":false,
    "ifExist":true
}
```



##### 用户登录

类型：GET

url：/api/user/login

说明：用户提交用户名和密码进行登录，后端通过数据库检查登录是否成功

参数：username、keyword

示例：

- url: /api/user/login
- 附带json:

```json
//  原始数据
{
    "username":"chengfenggui",
    "keyword":"123456",
}

//  实际传送数据
{
    "username":"Y2hlbmdmZW5nZ3Vp",
    "keyword":"MTIzNDU2",
}
```

- 回送：

```json
//  登录成功
{
    "ifSuccess":true,
    "username":"Y2hlbmdmZW5nZ3Vp",
    "name":"6ZKf5rqQ"
}
//  登录失败
{
    "ifSuccess":false,
    "username":"",
    "name":""
}
```

#### 地址管理

##### 查询所有地址

类型：GET

url：/api/user/address/queryall

说明：返回所有地址信息

参数：username

示例：

- url：/api/user/address/queryall?username="Y2hlbmdmZW5nZ3Vp"
- 附带json：无
- 回送：

```
[
    {
        "id":1,
        "accountUsername":"Y2hlbmdmZW5nZ3Vp",
        "receiverName":"钟源",
        "province":"湖北",
        "city":"武汉",
        "addressDetatil":"湖北省武汉市武汉大学信息学部",
        "addressLon":120,
        "addressLat":35,
        "phoneNum":18230152013
    },
    {
        ...
    }
]
```

##### 根据关键词搜索地址

类型：GET

url：/api/user/address/query

说明：根据关键词，搜索省/市/详细地址里包含指定关键词的字段

参数：username, search_keyword

示例：

- url:/api/user/address/query?username=Y2hlbmdmZW5nZ3Vp&&search_keyword=武汉大学
- 附带json：无
- 回送：如前

##### 添加地址

类型：POST

url：/api/user/address/add

说明：通过传入参数，添加新的数据库字段

参数：无

示例：

- url: /api/user/address/add
- 附带json：		

```
{
    "id":1,
    "accountUsername":"Y2hlbmdmZW5nZ3Vp",
    "receiverName":"钟源",
    "province":"湖北",
    "city":"武汉",
    "addressDetail":"湖北省武汉市武汉大学信息学部",
    "addressLon":120,
    "addressLat":35,
    "phoneNum":18230152013
}
```

- 回送：

```
{
    "ifSucess":true
}
```

##### 删除地址

类型：DELETE

url：/api/user/address/delete

说明：根据id，删除指定字段

参数：username, id

示例：

- url:/api/user/address/delete?username=Y2hlbmdmZW5nZ3Vp&&id=1
- 附带json：无
- 回送：

```
{
    "ifSuccess":true
}
```

##### 编辑地址

类型：PUT

url：/api/user/address/edit

说明：根据传入信息，修改相应字段

参数：无

示例：

- url:/api/user/address/edit
- 附带json：

```
{
    "id":1,
    "accountUsername":"Y2hlbmdmZW5nZ3Vp",
    "receiverName":"钟源",
    "province":"湖北",
    "city":"武汉",
    "addressDetail":"湖北省武汉市武汉大学信息学部",
    "addressLon":120,
    "addressLat":35,
    "phoneNum":18230152013
}
```

- 回送：

```
{
    "ifSuccess":true
}
```

#### 订单部分

##### 查询所有订单

类型：GET

url: /api/user/order/queryAll

说明：根据用户名查询所有订单

参数：username

示例：

- url: /api/user/order/queryall?username=Y2hlbmdmZW5nZ3Vp

- 附带json：无
- 回送：

```json
[
  {
    "id":"160834798171871",
    "accountUsername":"Y2hlbmdmZW5nZ3Vp",		// 此为登录账户的名称
    "goodDescription":"爱疯12",
    "receiverName":"钟源",		// 收货人姓名
    "deliverName":"淘宝卖家1",
    "addressDetail":"湖北省武汉市武汉大学",	// 这里要带有省市信息，可能需要字符串拼接
    "entryTime":"1608347981718",		// 13位毫秒级时间戳,
    "callbackState":0,
    "orderState":0,
    "desChangedTimes":0,
    "receivingOption":1
  },{
    // ......
  }
]
```



##### 添加订单

类型：POST

url: /api/user/order/add

说明：添加订单信息，但不生成路径

参数：username

示例：

- url: /api/user/order/add?username=Y2hlbmdmZW5nZ3Vp
- 附带json：

```json
{
  "id":"160834798171871",
  "receiverAddressId":1,
  "deliverUsername":"Y2hlbmdmZW5nZ3Vp"	// 卖家用户名
  "goodDescription":"爱疯12",
  "receivingOption":0
}
```

- 回送：

```json
{
  "ifSuccess":true
}
```

##### 查询未完成订单的数量

类型：GET

url: /api/user/order/unfinished/num

说明：根据用户订单的orderState字段，获取特定用户所有未完成订单的数量

参数：username

示例：

- url: /api/user/order/unfinished/num?username=Y2hlbmdmZW5nZ3Vp
- 附带json：无
- 回送：

```json
{
  "orderNum":12
}
```



##### 根据关键词查询订单

类型：GET

url：/api/user/order/query

说明：根据关键词，搜索 发货人/地址信息/货物 中包含相应字段的订单记录

参数：username, search_keyword

示例：

- url: /api/user/order/query?username=Y2hlbmdmZW5nZ3Vp&&search_keyword=武汉大学
- 附带json：无
- 回送：如查询所有订单API



##### 确认收货

类型：GET

url: /api/user/order/confirmReceiving

说明：根据订单编号，将订单orderState更改为5

参数：id（订单编号）

示例：

- url: /api/user/order/confirmReceiving?id=2012392104
- 附带json：无
- 回送：无

### 卖家部分

##### 查询所有卖家

类型：GET

url: /api/user/seller/queryAll

说明：查询所有卖家

参数：无

示例：

- url: /api/user/order/queryAll
- 附带json：无
- 回送：

```json
{
  "username":"Y2hlbmdmZW5nZ3Vp",
  "province":"湖北省",
  "city":"武汉市",
  "name":"钟源",
  "addressDetail":"武汉大学文理学部",
  "addressLon":113.123435,
  "addressLat":30.123432,
  "phoneNum":18211031231
}
```

