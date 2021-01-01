# Web API设计说明

## Todo

### 用户部分

#### 订单部分

##### 查询某一订单的路由信息（有更改）

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
    "addressLon":113.345331,
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



### 卖家部分

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
  [{
    "id":123,	// 快递节点编号
    "address":"xxxxx韵达快递",
    "distance":"12米"		// 与卖家的距离
  },{
    // ...
  }],
  
  // 下面返回与卖家最近的5个快递节点，供卖家可视化显示及选择
  // 这个就不用排序了
  [{
    "id":123,
    position: {
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

说明：卖家点击发货按钮，后台根据卖家选择的发货节点，使用最短路径算法生成路径信息（即在RouteInfo中添加相应记录），并更新订单OrderState为1。同时，卖家一发货，便到达第一个节点，将路径中第一个节点的RouteInfo的ArrivingTime更新为当前时间戳（13位毫秒级时间戳）

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
  "orderState":0
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