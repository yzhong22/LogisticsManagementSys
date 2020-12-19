# Web API设计说明

## Done

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



## Todo

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

```json
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

```json
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

```json
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

```json
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

```json
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

```json
{
    "ifSuccess":true
}
```

### 订单部分

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
[{
  	"orderId":"160834798171871",
  	"goodDescription":"爱疯12",
  	"receiver":{
      	"username":"Y2hlbmdmZW5nZ3Vp",
      	"name":"钟源",			// 此为登录账户的名称
      	"address":{
          	"receiverName":"ypy",		// 此为收货人的名称
          	"phoneNum":"18186113076",
          	"province":"湖北省",
          	"city":"武汉市",
          	"addressDetail":"信息学部",
          	"addressLon":114.366293,
          	"addressLat":30.535219,
        }
    },
  	"deliver":{
      	"username":"Y2hlbmdmZW5nZ3Vp",		// 此为卖家的用户名,
      	"name":"淘宝卖家1",
      	"phoneNum":"13025612302",
      	"province":"四川省",
      	"city":"成都市",
      	"addressDetail":"宽窄巷子",
      	"addressLon":113.345331,
      	"addressLat":30.120412,
    },
  	"route":[
      	// 此部分为路由信息，需根据派送路径进行排序
      	{
          	"id":1,
          	"province":"四川省",
          	"city":"成都市",
          	"addressDetail":"宽窄巷子韵达快递",
          	"nodeLon":113.123435,
          	"nodeLat":30.123432,
          	"ifFull":false,
          	"arrivingTime":"1608347981718",		// 13位毫秒级时间戳
          	"leavingTime":"1608347981718",		// 13位毫秒级时间戳
        }
    ],
  	"entryTime":"1608347981718",		// 13位毫秒级时间戳,
  	"callbackState":0,
  	"orderState":0,
  	"desChangedTimes":0
},{
  	......
}]
```

