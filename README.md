# Web API设计说明

## Todo

### 用户部分

#### 订单部分

##### 查询某一订单的路由信息

类型：GET

url: /api/user/order/showCertainOrder

说明：根据特性信息查询订单的路由信息

参数：username, orderId

示例：

- url: /api/user/order/showCertainOrder?username=Y2hlbmdmZW5nZ3Vp&&orderId=160834798171871
- 附带json：无
- 回送：

```json
{
  "orderId":"160834798171871",
  "goodDescription":"爱疯12",
  "receiver":{
    "username":"Y2hlbmdmZW5nZ3Vp",
    "name":"钟源",			// 此为登录账户的名称
    "address":{
      "receiverName":"ypy",		// 此为收货人的名称
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
    "province":"四川省",
    "city":"成都市",
    "addressDetail":"宽窄巷子",
    "i":113.345331,
    "addressLat":30.120412,
  },
  "route":{
    // 此处为新增内容
    // 此处为新增内容
    // 此处为新增内容
    "nodeNow":{
      "nodeNumNow":0,
      "nodeState":0
    },
    // 这部分是 卖家地址、买家地址、所有路由节点 计算的bounding box
    "box":{
      "minLon":100,
      "minLat":30,
      "maxLon":110,
      "maxLat":32
    },
    
    // 上述为新增内容
    // 上述为新增内容
    // 上述为新增内容
    "node":[
      // 此部分为路由信息，需根据派送路径进行排序，方便地图可视化显示
      {
        "id":1,
        "province":"四川省",
        "city":"成都市",
        "addressDetail":"宽窄巷子韵达快递",
        "nodeLon":113.123435,
        "nodeLat":30.123432,
        "arrivingTime":"1608347981718",		// 13位毫秒级时间戳
        "leavingTime":"1608347981718",		// 13位毫秒级时间戳
      },
      {
        // ......
      }
    ],
    // 下面是时间线描述信息，需要根据路径等节点信息生成
    "deliverInfo":[
      // 订单创建的时间entryTime
      {
        "content":"商品已下单",
        "timestamp":"2020/4/13  22:14",
        "event":"create"
      },
      // 卖家发货的时间，即第一个node的arrivingTime
      {
        "content":"卖家已发货",
        "timestamp":"2020/4/14  5:27",
        "event":"sendOut"
      },
      // 到达第一个节点
      {
        "content":"【成都市】您的快递已到达【xxx快递公司】",
        "timestamp":"2020/4/14  5:27",
        "event":"normal"
      },
      // 由节点送出
      {
        "content":"【成都市】xxx快递公司 已发出",
        "timestamp":"2020/4/14  6:27",
        "event":"normal"
      },
      // 到达最后一个节点
      {
        "content":"已到达 xxx快递公司",
        "timestamp":"2020/4/16  16:27",
        "event":"arrive"
      },
      // 如果是选择自己上门收取
      {
        "content":"【代收点】您的快递已暂存于 xxx快递公司，地址：xxxx，请及时领取",
        "timestamp":"2020/4/16  16:27",
        "event":"fetch"
      },
      // 第三方派送员揽件
      {
        "content":"【派送中】您的快递正由 xxx骑手进行派送，联系方式：xxxx，请注意查收",
        "timestamp":"2020/4/16  18:23",
        "event":"dispatch"
      },
      // 快递查收
      {
        "content":"您的快递已确认查收",
        // 对应finishTime
        "timestamp":"2020/4/16  20:54",
        "event":"finish"
      },
      // 下面是特殊情况
      // 若用户发起退货申请，则订单到达下一节点后，便显示退货信息，后续返回节点路由信息不显示，最后快递到达起始节点并且卖家确认收货后，显示完成信息
      {
        "content":"进入退货流程",
        "timestamp":"2020/4/15  17:43",
        "event":"callback"
      },
      // 更改地址时只涉及到路由的更新，这里不额外显示
    ]
  }
}
```

##### 查询所有未完成订单（有更改）

类型：GET

url: /api/user/order/unfinished/queryAll

说明：查询所有未完成的（即OrderState!=5的）订单

参数：username

示例：

- url: /api/user/order/unfinished/queryAll?username=Y2hlbmdmZW5nZ3Vp
- 附带json：无
- 回送：

```json
[{
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
  "receivingOption":1,
  // 以下是更改部分
  // 这里是需要买家取货的地方，即最后一个节点
  // 如果receivingOption为1，即买家自取
  "fetchAddress":"xxxx韵达快递",
  // 如果receivingOption为0，则不提示具体信息
  "fetchAddress":""
  },{
    // ......
  }]
```

##### 更改收货方式

类型：POST

url: /api/user/order/changeReceivingOpt

说明：将特定订单receivingOption由1改为0（或由0改为1）

参数：id（订单id）

示例：

- url: /api/user/order/changeReceivingOpt?id=12321423
- 附带json：无
- 回送：无

#### 收货站点可视化

##### 查询用户所有待取货订单

类型：GET

url: /api/user/mapOrder/queryAll

说明：查询特定用户所有orderState为2，且receivingOption为1的订单

参数：username

示例：

- url: /api/user/mapOrder/queryAll?username=Y2hlbmdmZW5nZ3Vp
- 附带json：无
- 回送：

```json
{
  // 第一部分是基本的快递信息
  "basicInfo":[{
    "id":"12321512312",		// 订单id
    "addressDetail":"武汉市xxxx韵达快递",		// 站点的名称
    "goodDescription":"爱疯12",
    "nodeLon":124.2,
    "nodeLat":30.2
  },{
    // ...
  }],
  // 第二部分需要返回分节点的快递信息，是根据快递节点分组
  "mapInfo":[{
    "nodeAddress":"武汉市xxxx韵达快递",
    "nodeLon":124.2,
    "nodeLat":30.2,
    // 下面是该节点的订单信息，需要根据订单的NodeNumNow查询
    "orderNum":3,			// 该节点的订单数
    "orders":[{
      "orderId":"123211234123",
      "orderGood":"爱疯12"
    },{
      // ...
    }]
  },{
    // ...
  }]
}

```



### 卖家部分

### 物流节点部分

#### 收货管理

##### 查询所有即将到达本节点的订单

类型：GET

url: /api/node/receive/queryAll

说明：查询所有即将到达本节点的订。（即若某订单NodeNumNow为3，NodeState为1，且第5个节点则为本节点，则将该节点提取出）

参数：nodeId

示例：

- url: /api/node/receive/queryAll?nodeId=12
- 附带json：无
- 回送：

```json
[{
  "id":1231254213,		// 订单编号
  "receiverName":"钟源",
  "deliverName":"老北京烤鸭",
  "goodDescription":"烤鸭",
  "receiverAddress":"武汉市武汉大学",		// 老样子，记得带上市区信息
  "deliverAddress":"北京市xxx烤鸭店",		// 带上市区信息
},
{
  // ...
}]
```



##### 根据关键词查询

类型：GET

url: /api/node/receive/query

说明：查询 收货人/送货人/商品描述/收货地址/送货地址 中包含关键字的记录。回送结构与上相同，不再赘述

参数：nodeId，search_keyword



##### 确认收货

类型：POST

url: /api/node/receive/confirm

说明：确认订单收货，将订单NodeNumNow加一，NodeState为0。并判断该订单是否到达最后一个节点，若是，则将OrderState改为2。并更新RouteInfo中对应节点的ArrivingTime时间戳信息（13位）

参数：id（订单编号）

示例：

- url :/api/node/receive/confirm?id=123125213
- 附带json：无
- 回送：无



#### 发货管理

##### 查询所有在本节点的订单

类型：GET

url :/api/node/send/queryAll

说明：查询所有在本节点的订单（即根据订单的NodeNumNow，查询其所在节点的信息是否与该节点吻合）

参数：nodeId

示例：

- url: /api/node/send/queryAll?nodeId=123
- 附带json：无
- 回送：

```json
[{
  "id":1231254213,		// 订单编号
  "receiverName":"钟源",
  "nextNodeAddress":"xxx韵达快递",
  "deliverName":"老北京烤鸭",
  "goodDescription":"烤鸭",
  "receiverAddress":"武汉市武汉大学",		// 老样子，记得带上市区信息
  "deliverAddress":"北京市xxx烤鸭店",		// 带上市区信息
}]
```



##### 根据关键词查询

类型：GET

url: /api/node/send/query

说明：查询 收货人/送货人/商品描述/收货地址/送货地址/下一节点 中包含关键字的记录。回送结构与上相同，不再赘述

参数：nodeId，search_keyword



##### 确认发货

类型：POST

url: /api/node/send/confirm

说明：订单发货

操作：将NodeState改为1

参数：id（订单id）

示例：

- url: /api/node/send/confirm?id=123125213
- 附带json：无
- 回送：无



##### 更改下一节点

类型：POST

url: /api/node/send/changeNext

说明：根据NodeNumNow，对下一个节点的信息进行更新，即更改路由

参数：id（订单id），nextNodeId

示例：

- url: /api/node/send/changeNext?id=1232135123&&nextNodeId=132
- 附带json：无
- 回送：无



#### 上门取货管理

##### 查询所有暂存在本节点等待取件的订单

类型：GET

url: /api/node/fetch/queryAll

说明：根据NodeNumNow，查询所有在本节点，并OrderState为2，receivingOption为1的订单

参数：nodeId

示例：

- url: /api/node/fetch/queryAll?nodeId=1231
- 附带json：无
- 回送：

```json
[{
  "id":1231254213,		// 订单编号
  "receiverName":"钟源",
  "receiverPhoneNum":"18186113076",
  "goodDescription":"烤鸭",
  "receiverAddress":"武汉市武汉大学",		// 老样子，记得带上市区信息
  "detainedTime":"1天20时",		// 滞留时间，根据当前时间戳和到达该节点的时间戳计算，精确到小时
},
{
  // ....
}]
```



##### 根据关键词查询

类型：GET

url: /api/node/fetch/query

说明：根据关键词，查询  收货人姓名/收货人电话/商品描述/收获人地址  中含有关键词的结果，不再赘述

参数：nodeId，search_keyword



#### 第三方骑手派送管理

##### 查询所有终点为本节点的派送订单

类型：GET

url: /api/node/dispatch/queryAll

说明：根据NodeNumNow，查询所有在本节点，并OrderState为2或3，receivingOption为0的订单

参数：nodeId

示例：

- url: /api/node/dispatch/queryAll?nodeId=1231
- 附带json：无
- 回送：

```json
[{
  "id":1231254213,		// 订单编号
  "receiverName":"钟源",
  "receiverPhoneNum":"18186113076",
  "goodDescription":"烤鸭",
  "receiverAddress":"武汉市武汉大学",		// 老样子，记得带上市区信息
  "orderState":2,
  "receiverLng":143.1,
  "receiverLat":30.2,
  // 下面是骑手信息，若尚未接单，为空即可
  "dispatcherName":"外卖骑手xxx",
  "dispatcherPhoneNum":"1231235231"
},
{
  // ....
}]
```



##### 根据关键词查询

类型：GET

url: /api/node/fetch/query

说明：查询订单中  收货人/收货人电话/物品信息/骑手名称/骑手号码  中包含关键词的订单，回送结构与上相同

参数：nodeId，search_keyword



### 第三方骑手部分

##### 根据骑手的位置获取附近节点订单

类型：GET

url :/api/dispatcher/queryNear

说明：根据骑手的位置，获取附近（3km以内）节点的位置和这些节点待派送（orderState为2，receivingOption为0）的订单

参数：lng，lat（骑手的经纬度）

示例：

- url: /api/dispatcher/queryNear?lng=120&&lat=30&&city=武汉市
- 附带json：无
- 返回：

```json
{
  // 第一部分为附近节点信息
  "nearby_nodes":[{
    "lng":120,
    "lat":30,
    "orderNums":3
  },{
    // ...
  }],
  // 第二部分为附近节点的订单
  // 这部分要根据距离远近排序，最近的在最前面
  "orders":[{
    "id":"21321312312312", 	// 订单id
    "receiverName":"钟源",
    "receiverPhoneNum":"18186113076",
    "goodDescription":"爱疯12",
    "receiverAddress":"武汉市武汉大学",	// 带上市区信息
    "nodeAddress":"xxxx韵达快递",
    "distance":"100米",
    "receiverLng":120.3,
    "receiverLat":30.2,
    "nodeLng":119.4,
    "nodeLat":30.1
  },{
    // ...
  }]
}
```



##### 骑手接单

类型：POST

url: /api/dispatcher/grab

说明：骑手选择接单，将指定订单的orderState改为3，并将订单的dispatcherUsername改为自己的username

参数：无

示例：

- url: /api/dispatcher/grab
- 附带json：

```json
{
  "username":"chengfenggui",
  "id":"123124123123"	// 订单id
}
```

- 回送：无