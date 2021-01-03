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

##### 申请更改地址

类型：POST

url: /api/user/order/changeDes/apply

说明：根据用户指定的新的收货地址，以及当前派送路径情况，生成新的路由信息。例如，当前正处于第3个节点和第4个节点的派送过程中（即NodeNumNow为2，NodeState为1），则保持前4个节点信息不变，以第4个节点为起始节点，使用最短路径算法，改变从第5个节点及以后的所有节点；若当前正处于第3个节点，但尚未从第3个节点发出（即NodeNumNow为2，NodeState为0），则以第3个节点为起始节点，使用最短路径算法，改变从第4个节点及以后的所有节点。（将已有节点从RouteInfo表中删除，并添加新的节点记录。更改时注意NodeId域，这是表征派送顺序的唯一参照，详情请参照“卖家发货“API）

操作：将订单DesChangedTimes加一，将ReceiverAddressId更改为相应ID。

参数：无

示例：

- url: /api/user/order/changeDes/apply
- 附带json：

```json
{
  "id":123213215,		// 订单编号
  "receiverUsername":"Y2hlbmdmZW5nZ3Vp",
  "newAddressId":2
}
```

- 回送：

```json
{
  "ifSuccess":true
}
// 或者检验已不能申请退货（orderState>=3）或已经申请过(DesChangedTimes!=0)
{
  "ifSuccess":false,
  "content":"xxx"	// 向用户进行提示
}
```

##### 申请退货

类型：GET

url: /api/user/order/callback/apply

说明：用户发送订单退货申请。还需将该订单orderState置为4，callbackState置为1。

参数：id（订单编号）

示例：

- url: /api/user/order/callback/apply?id=2012392104
- 附带json：无
- 回送：

```json
{
  "ifSuccess":true
}
// 或者检验已不能申请退货（orderState>=2）
{
  "ifSuccess":false,
  "content":"xxx"	// 向用户进行提示
}
```

##### 

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

#### 待发货订单

##### 返回卖家所有待发货的订单

类型：GET

url: /api/seller/send/queryAll

说明：查询特定卖家所有的待发货（即orderState为0）的快递订单

参数：username

示例：

- url: /api/seller/send/queryAll?username=Y2hlbmdmZW5nZ3Vp
- 附带json：无
- 回送：

```json
[{
  "id":123123,
  "receiverName":"钟源",
  "goodDescription":"爱疯12",
  "receiverAddress":"湖北省武汉市武汉大学"	// 注意这部分需要加上省市信息，可能需要字符串拼接
},
{
  // ...
}]
```



##### 根据关键字查询

类型：GET

url: /api/seller/send/query

说明：该部分关键词查询与上述其他查询相同，要求能查询 买家姓名/商品描述/买家地址 中含有特定关键词的记录，返回形式也同上API相似的数组，便不再赘述

参数：username、keyword



##### 返回卖家附近的物流节点

类型：GET

url: /api/seller/send/nearbyNodes

说明：根据卖家位置，查询附近的快递节点

参数：username

示例：

- url: /api/seller/send/nearbyNodes?username=Y2hlbmdmZW5nZ3Vp
- 附带json：无
- 回送：

```json
{
  // 这部分需要用到空间分析内容，可能需要geometry字段
  // 由于之前卖家和买家类没有用geometry字段保存位置信息，可能需要新建一个表
  // 把之前的经纬度字段转化为geometry保存
  // 原来的表不删除，以免对已完成对API做过多修改
  // 需要利用geometry字段的API将新旧表联合起来进行查询
  
  // 返回本市所有的快递节点信息，供卖家选择
  // 这部分需要根据与卖家的距离进行排序（最近的排在第一个）
  "options":[{
    "id":123,	// 快递节点编号
    "address":"xxxxx韵达快递",
    "distance":"12米"		// 与卖家的距离
  },{
    // ...
  }],
  
  // 下面返回与卖家最近的5个快递节点，供卖家可视化显示及选择
  // 这个就不用排序了
  "nearest_nodes":[{
    "id":123,
    "position": {
      "lng": 114.372042,
      "lat": 30.544861
    }
  },
  {
    // ...
  }]
}
```



##### 卖家发货

类型：POST

url: /api/seller/send

说明：卖家点击发货按钮，后台根据卖家选择的发货节点，使用最短路径算法生成路径信息（即在RouteInfo中添加相应记录），并更新订单OrderState为1。同时，卖家一发货，便到达第一个节点，将路径中第一个节点的RouteInfo的ArrivingTime更新为当前时间戳（13位毫秒级时间戳）。注意，这里根据最短路径添加节点信息在RouteInfo表里存储，应将NodeId字段按照派送顺序从0或1开始进行排序，以表征派送顺序

参数：无

示例：

- url: /api/seller/send
- 附带json：

```json
// 这里只附带基本信息，需根据最短路径算法生成路径
{
  "id":123123,	// 订单编号
  "chosenNodeId":123		// 卖家选择的起始节点编号
}
```

- 回送：

```json
{
  "ifSuccess":true
}
```



#### 全部订单

##### 返回特定卖家的全部订单

类型：GET

url: /api/seller/order/queryAll

说明：查询特定卖家的所有订单

参数：username

示例：

- url: /api/seller/order/queryAll?username=Y2hlbmdmZW5nZ3Vp
- 附带json：无
- 回送：

```json
[{
  "id":112213125,
  "receiverName":"钟源",
  "receiverAddress":"湖北省武汉市武汉大学",		// 需包含省市信息
  "goodDescription":"爱疯12",
  "orderState":0,
  "receivingOption":1
}]
```



##### 根据关键词查询

类型：GET

url: /api/seller/order/query

说明：查询 收货人姓名/收货人地址/商品描述 中包含关键词的记录

参数：username，keyword



##### 查询某一订单的路由信息

类型：GET

url: /api/seller/order/route

说明：与用户部分的查询路由相似，只是将username改为卖家的用户名，在deliver表中进行查询，不再赘述



#### 退货审批

##### 查询所有待处理的退货订单

类型：GET

url: /api/seller/order/callback/queryAll

参数：username

说明：查询特定卖家待处理的退货订单（即OrderState为4）

示例：

- url: /api/seller/order/callback/queryAll?username=Y2hlbmdmZW5nZ3Vp
- 附带json：无
- 回送：

```json
[{
  "id":123213124,
  "receiverName":"钟源",
  "goodDescription":"爱疯12",
  "receiverAddress":"湖北省武汉市武汉大学",	// 需要保护省市信息
  "callbackState":0		// 按理来说，应该只有1和2两种可能
},{
  // ....
}]
```



##### 卖家同意退货申请

类型：POST

url: /api/seller/order/callback/agree

参数：id（订单编号）

说明：与申请更改地址类似，根据目前运输情况，对订单后续节点进行更改，使之原路返回（该节点修改方式参照“申请更改地址API”。如已送到第3个节点，则更改后的信息总共有5个节点，起点和终点为同一节点）

操作：将订单callbackState置为2

示例：

- url: /api/seller/order/callback/agree?id=123124
- 附带json：无
- 回送：无



##### 卖家确认收货

类型：POST

url: /api/seller/order/callback/finish

参数：id（订单编号）

说明：卖家点击确认收货，完成这一事件

操作：将订单callbackState置为3，orderState置为5

示例：

- url: /api/seller/order/callback/agree?id=123124
- 附带json：无
- 回送：

```json
{
  "ifSuccess":true
}
// 检验最后一个节点的到达时间ArrivingTime是否为空（为空则代表还没到达），若为空，则不让用户确认收货
{
  "ifSuccess":false,
  "errorMessage":"退货商品尚未到达！"
}
```

