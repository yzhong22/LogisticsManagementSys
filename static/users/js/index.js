Vue.use(VueBaiduMap.default, {
    ak: 'MTMdfHzZv4SVWqauWpmqOwKjUEysvKpd'
});

let app = new Vue({
    el: "#app",
    data: {
        default_active: "1",
        login_user: {
            name: "",
            username: ""
        },
        address: {
            all: [],
            current: {},
            temporal_coor: {},  // 选择的经纬度暂存于此
            search_keyword: '',
            map: 0,
            BMap: undefined,
            edit_mode: false,
            mapInfo: {
                center: {lng: 114.372042, lat: 30.544861},
                zoom: 16
            },
            addVisible: false,
            mapVisible: false,
            rules: {
                province: [
                    {required: true, message: '请输入省份', trigger: 'change'},
                ],
                receiverName: [
                    {required: true, message: '请输入省份', trigger: 'change'},
                ],
                city: [
                    {required: true, message: '请输入市区', trigger: 'change'},
                ],
                addressDetail: [
                    {required: true, message: '请输入详细地址', trigger: 'change'},
                ],
                phoneNum: [
                    {required: true, message: '请输入联系方式', trigger: 'change'},
                ],
            }
        },
        order: {
            all: [],
            current: {diliveryInfo: []},
            temporal_coor: {},  // 选择的经纬度暂存于此
            search_keyword: '',
            routeMapInfo: {
                center: {lng: 114.372042, lat: 30.544861},
                zoom: 16
            },
            map: 0,
            BMap: undefined,
            DrivingRoute: 0,
            routeVisible: false,
            addVisible: false,
            mapVisible: false,
            rules: {
                receiverAddressId: [
                    {required: true, message: '请选择收货地址', trigger: 'change'},
                ],
                deliverUsername: [
                    {required: true, message: '请选择卖家', trigger: 'change'},
                ],
                goodDescription: [
                    {required: true, message: '请输入货物信息', trigger: 'change'},
                ],
            }
        },
        unfinishedOrder: {
            all: [],
            current: {diliveryInfo: []},
            change_node_current: {},
            orderNum: 0,
            map: 0,
            BMap: undefined,
            DrivingRoute: 0,
            routeVisible: false,
            changenode_Visible: false,
            change_node_map: 0,
            change_node_BMap: undefined,
            receiving_options: [],
            change_node_mapInfo: {
                center: {lng: 114.372042, lat: 30.544861},
                zoom: 16
            },
            routeMapInfo: {
                center: {lng: 114.372042, lat: 30.544861},
                zoom: 16
            },
            mapVisible: false,
        },
        mapOrder: {
            all: [],
            map: 0,
            BMap: 0,
            mapInfo: {
                center: {lng: 114.372042, lat: 30.544861},
                zoom: 16
            },
            mapContent: []
        },
        seller: {
            all: []
        },

    },
    methods: {
        // 公共部分
        hideAll() {
            document.getElementById('address_manage').style.display = 'none';
            document.getElementById('all_order').style.display = 'none';
            document.getElementById('tobe_received').style.display = 'none';
            document.getElementById('map_orders').style.display = 'none';
        },
        handle_select(key, keyPath) {
            this.hideAll();
            axios.get('/api/user/order/unfinished/num?username=' + URLSafeBase64.encode(this.login_user.username))
                .then(res => {
                    this.unfinishedOrder.orderNum = res.data.orderNum;
                    switch (key) {
                        case("1"):
                            document.getElementById('address_manage').style.display = 'block';
                            this.address_query();
                            break;
                        case("2-1"):
                            document.getElementById('all_order').style.display = 'block';
                            axios.get('/api/user/seller/queryAll')
                                .then(res => {
                                    this.seller.all = res.data;
                                    this.address_query();
                                })
                                .then(res => this.order_query());
                            break;
                        case("2-2"):
                            document.getElementById('tobe_received').style.display = 'block';
                            this.unfinishedOrder_queryAll();
                            break;
                        case("2-3"):
                            document.getElementById('map_orders').style.display = 'block';
                            this.mapOrder_queryAll();
                            break;
                        default:
                            document.getElementById('address_manage').style.display = 'block';
                            break;
                    }
                });
        },
        // 用户旁设置键对应方法
        handle_command(command) {
            switch (command) {
                case("1"):
                    break;
                case("2"):
                    self.location = "/users/login";
                    break;
                default:
                    break;
            }
        },
        // 地址部分
        address_addoverlay(lng, lat) {
            var myMarker = new BMap.Marker(new BMap.Point(lng, lat));
            this.address.map.addOverlay(myMarker);
        },
        address_zoom_and_skip(encoded_address) {
            this.address.mapInfo.center = encoded_address;
            this.address_addoverlay(encoded_address.lng, encoded_address.lat);
            this.address.temporal_coor.addressLon = encoded_address.lng;
            this.address.temporal_coor.addressLat = encoded_address.lat;
        },
        address_showMap() {
            this.address.mapVisible = true;
            if (this.address.BMap !== undefined) {
                let myGeo = new this.address.BMap.Geocoder();
                let encoded_address = undefined;
                if (this.address.current.city !== undefined && this.address.current.addressDetail !== undefined) {
                    myGeo.getPoint(this.address.current.addressDetail, function (point) {
                        if (point) {
                            encoded_address = {lng: point.lng, lat: point.lat};
                        } else {
                            encoded_address = {lng: 114.372042, lat: 30.544861};
                        }
                        app.address_zoom_and_skip(encoded_address);
                    }, this.address.current.city);
                } else {
                    encoded_address = {lng: 114.372042, lat: 30.544861};
                    this.address_zoom_and_skip(encoded_address);
                }
            }
        },
        // 地图初始化时调用
        address_mapHandler({BMap, map}) {
            this.address.map = map;   //将map变量存储在全局
            this.address.BMap = BMap;
            let myGeo = new BMap.Geocoder();
            let encoded_address = undefined;
            if (this.address.current.city !== undefined && this.address.current.addressDetail !== undefined) {
                myGeo.getPoint(this.address.current.addressDetail, function (point) {
                    if (point) {
                        encoded_address = {lng: point.lng, lat: point.lat};
                    } else {
                        encoded_address = {lng: 114.372042, lat: 30.544861};
                    }
                    app.address_zoom_and_skip(encoded_address);
                }, this.address.current.city);
            } else {
                encoded_address = {lng: 114.372042, lat: 30.544861};
                this.address_zoom_and_skip(encoded_address);
            }
        },
        address_closemap() {
            this.address.temporal_coor = {};
            this.address.map.clearOverlays();
            this.address.mapVisible = false;
        },
        // 地图坐标选取
        address_pointPick(e) {
            this.address.map.clearOverlays();
            this.address_addoverlay(e.point.lng, e.point.lat);
            this.address.temporal_coor = {addressLon: e.point.lng, addressLat: e.point.lat};
        },
        address_location_select() {
            let myGeo = new this.address.BMap.Geocoder();
            myGeo.getLocation(new this.address.BMap.Point(this.address.temporal_coor.addressLon, this.address.temporal_coor.addressLat), function (result) {
                if (result) {
                    let addComp = result.addressComponents;
                    app.address.current.province = addComp.province;
                    app.address.current.city = addComp.city;
                    app.address.current.addressDetail = result.address;
                    app.address.current.addrsssLon = app.address.temporal_coor.addressLon;
                    app.address.current.addrsssLat = app.address.temporal_coor.addressLat;
                    app.address.mapVisible = false;
                }
            });
        },
        address_add() {
            this.address.current = {};
            axios.get('/api/user/address/queryAll?username=' + URLSafeBase64.encode(this.login_user.username))
                .then(res => {
                    let newAddress = Object.assign([], res.data);
                    let sort = newAddress.sort((a, b) => a.id - b.id);
                    let i = 0;
                    try {
                        sort.forEach(address => {
                            i++;
                            if (address.id !== i) {
                                this.address.current.id = i;
                                throw new Error("ending");  // 退出循环
                            }
                        });
                        this.address.current.id = i + 1;
                    } catch (e) {
                        return 0;
                    }

                    this.address.edit_mode = false;
                    this.address.addVisible = true;
                });
        },
        address_query() {
            let url = '/api/user/address/';
            let keyword = this.address.search_keyword;
            if (keyword !== "") {
                url = url + 'query?search_keyword=' + keyword + '&&username=' + URLSafeBase64.encode(this.login_user.username);
            } else {
                url = url + 'queryAll?username=' + URLSafeBase64.encode(this.login_user.username);
            }
            axios.get(url)
                .then(res => {
                    this.address.all = res.data;
                });
        },
        address_refresh() {
            this.address.search_keyword = "";
            this.address_query();
        },
        address_showEdit(address) {
            this.address.edit_mode = true;
            this.address.addVisible = true;
            this.address.current = Object.assign({}, address);
        },
        address_submit(form) {
            this.$refs[form].validate((valid) => {
                if (valid) {
                    let self = this;
                    let myGeo = new BMap.Geocoder();
                    let current = self.address.current;
                    myGeo.getPoint(current.addressDetail, function (point) {
                        let encoded_address = undefined;
                        if (point) {
                            encoded_address = {lng: point.lng, lat: point.lat};
                        } else {
                            encoded_address = {lng: 114.372042, lat: 30.544861};
                        }
                        if (current.addressLon == undefined || self.address.edit_mode) {
                            current.addressLon = encoded_address.lng;
                            current.addressLat = encoded_address.lat;
                        }

                        current.accountUsername = URLSafeBase64.encode(self.login_user.username);
                        if (self.address.edit_mode) {
                            axios.put('/api/user/address/edit', current)
                                .then(res => {
                                    self.address_query();
                                    self.address.addVisible = false;
                                    self.address.edit_mode = false;
                                })
                        } else {
                            axios.post('/api/user/address/add', current)
                                .then(res => {
                                    self.address_query();
                                    self.address.addVisible = false;
                                })
                        }
                    }, current.city);
                } else {
                    return false;
                }
            });
        },
        address_delete(address) {
            axios.delete('/api/user/address/delete?username=' + URLSafeBase64.encode(this.login_user.username) + '&&id=' + address.id)
                .then(res => this.address_query())
        },

        // 订单部分
        order_query() {
            let url = '/api/user/order/';
            let keyword = this.order.search_keyword;
            if (keyword !== "") {
                url = url + 'query?search_keyword=' + keyword + '&&username=' + URLSafeBase64.encode(this.login_user.username);
            } else {
                url = url + 'queryAll?username=' + URLSafeBase64.encode(this.login_user.username);
            }
            axios.get(url)
                .then(res => {
                    this.order.all = res.data;
                });
        },
        order_add() {
            this.order.current = {receivingOption: "0"};
            let timestamp = (new Date()).valueOf();
            let random_num = Math.floor(Math.random() * 100);
            this.order.current.id = timestamp.toString() + random_num.toString();

            this.order.addVisible = true;
        },
        submitNewOrder(form) {
            this.$refs[form].validate((valid) => {
                if (valid) {
                    let data = Object.assign({}, this.order.current);
                    data.deliverUsername = URLSafeBase64.encode(data.deliverUsername);
                    console.log(data);
                    axios.post('/api/user/order/add?username=' + URLSafeBase64.encode(this.login_user.username), data)
                        .then(res => {
                            this.order_query();
                            this.unfinishedOrder.orderNum++;
                            this.order.addVisible = false;
                        })
                } else {
                    return false;
                }
            });
        },
        order_refresh() {
            this.order.search_keyword = "";
            this.order_query();
        },
        order_check_if_changeable(order) {
            if (order.orderState < 3 && order.desChangedTimes == 0) {
                return true;
            } else {
                return false;
            }
        },
        order_check_if_callbackable(order) {
            if (order.orderState < 2) {
                return false
            } else {
                return true
            }
        },
        order_showRoute(order) {
            let self = this;
            let url = '/api/user/order/showCertainOrder?id=' + order.id;
            axios.get(url)
                .then(res => {
                    let deliveryInfo = res.data.route.deliveryInfo;

                    // 添加timeline样式
                    deliveryInfo.forEach(r => {
                        if (r.event == "create") {
                            r.icon = "el-icon-warning-outline";
                            r.type = "primary"
                            r.size = "large"
                        }
                        if (r.event == "sendOut" || r.event == "arrive") {
                            r.color = '#0bbd87';
                            r.size = "large"
                        }
                        if (r.event == "fetch") {
                            r.icon = "el-icon-bangzhu";
                            r.type = "warning"
                            r.size = "large"
                        }
                        if (r.event == "dispatch") {
                            r.icon = "el-icon-bicycle";
                            r.type = "warning"
                            r.size = "large"
                        }
                        if (r.event == "finish") {
                            r.icon = "el-icon-success";
                            r.type = "primary";
                            r.size = "large"
                        }
                        if (r.event == "callback") {
                            r.icon = "el-icon-remove";
                            r.type = "danger";
                            r.size = "large"
                        }
                    });
                    self.order.current.deliveryInfo = deliveryInfo;
                    console.log(this.order.current.deliveryInfo);
                    self.order.current.deliver = res.data.deliver;
                    self.order.current.receiver = res.data.receiver;
                    self.order.current.nodes = res.data.route.node;
                    self.order.current.route_now = res.data.route.now;

                    this.order.routeVisible = true;
                    if (self.order.map !== 0) {
                        self.order_map_addRoute();
                    }
                });
        },
        order_map_addRoute() {
            let self = this;
            let deliver = self.order.current.deliver;
            let receiver = self.order.current.receiver;
            let nodes = self.order.current.nodes;
            let route_now = self.order.current.route_now;

            self.order.DrivingRoute.clearResults();
            self.order.map.clearOverlays();

            // 卖家
            self.order_addMarker(deliver.lng, deliver.lat, "seller", "png",
                30, 30, "卖家：" + deliver.name, "<br>" + deliver.address);
            // 买家
            self.order_addMarker(receiver.lng, receiver.lat, "seller_position", "png",
                30, 30, "买家：" + receiver.name, "<br>" + receiver.address);

            let p_now = new BMap.Point(route_now.lon, route_now.lat);
            let now_label = new BMap.Label(route_now.content, {position: p_now});
            self.order.map.addOverlay(now_label);

            let p_receiver = new BMap.Point(receiver.lng, receiver.lat);
            let p_deliver = new BMap.Point(deliver.lng, deliver.lat);

            let nodes_num = nodes.length;
            if (nodes_num > 0) {
                let driving = this.order.DrivingRoute;
                for (let i = 0; i < nodes_num; i++) {
                    self.order_addMarker(nodes[i].lng, nodes[i].lat, "express", "png",
                        20, 20, "物流节点", "<br>" + nodes[i].address);
                    if (i < nodes_num - 1) {
                        let start = new this.order.BMap.Point(nodes[i].lng, nodes[i].lat);
                        let end = new this.order.BMap.Point(nodes[i + 1].lng, nodes[i + 1].lat);
                        driving.search(start, end);
                    }
                }

                // 开始加线
                driving.setSearchCompleteCallback(function () {
                    if (driving.getStatus() != BMAP_STATUS_SUCCESS) {
                        this.$message.error('查询路径错误！');
                        return;
                    }

                    let pts = driving.getResults().getPlan(0).getRoute(0).getPath();    //通过驾车实例，获得一系列点的数组
                    let polyl_get = new BMap.Polyline(pts);
                    self.order.map.addOverlay(polyl_get);

                    let first_node = new BMap.Point(nodes[0].lng, nodes[0].lat);
                    let last_node = new BMap.Point(nodes[nodes_num - 1].lng, nodes[nodes_num - 1].lat);

                    let pll_s = new BMap.Polyline([p_deliver, first_node], {
                        strokeColor: "#98FB98", strokeStyle: "dashed", strokeWeight: 3, strokeOpacity: 0.9
                    });
                    self.order.map.addOverlay(pll_s);
                    let pll_r = new BMap.Polyline([last_node, p_receiver], {
                        strokeColor: "#FFDEAD", strokeStyle: "dashed", strokeWeight: 3, strokeOpacity: 0.9
                    });
                    self.order.map.addOverlay(pll_r);

                    setTimeout(function () {
                        self.order.map.setViewport([p_deliver, p_receiver, first_node, last_node
                        ]);          //调整到最佳视野
                    }, 1000);
                })
            } else {
                setTimeout(function () {
                    self.order.map.setViewport([p_deliver, p_receiver
                    ]);          //调整到最佳视野
                }, 1000);
            }

        },
        order_addMarker(lng, lat, img_file, img_type, w, h, info_title, info_content) {
            let self = this;
            let p = new this.order.BMap.Point(lng, lat);
            let m = new this.order.BMap.Marker(p, {
                icon: new this.order.BMap.Icon("/api/img?file=" + img_file + "&&type=" + img_type +
                    "&&width=" + w + "&&height=" + h, new this.order.BMap.Size(w, h))
            });
            this.order.map.addOverlay(m);
            let opts = {
                width: 0,
                height: 0,
                title: info_title,
            };
            let infoWindow = new this.order.BMap.InfoWindow(info_content, opts);
            m.addEventListener('mouseover', function () {
                self.order.map.openInfoWindow(infoWindow, p);
            });
            m.addEventListener('mouseout', function () {
                self.order.map.closeInfoWindow(infoWindow, p);
            });
        },
        order_mapHandler({BMap, map}) {
            this.order.map = map;   //将map变量存储在全局
            this.order.BMap = BMap;
            this.order.DrivingRoute = new this.order.BMap.DrivingRoute(this.order.map);

            this.order_map_addRoute();
        },
        order_confirmReceive(order) {
            let url = '/api/user/order/confirmReceiving?id=' + order.id;
            axios.get(url)
                .then(res => {
                    if (res.data.ifSuccess) {
                        this.$message({
                            message: '收货成功！',
                            type: 'success'
                        });
                        this.unfinishedOrder.orderNum--;
                    } else {
                        this.$message.error('收获失败');
                    }
                    this.order_query();
                    this.unfinishedOrder_queryAll();
                })
        },
        // 待收货订单部分
        order_apply_callback(order) {
            axios.get('/api/user/order/callback/apply?id=' + order.id)
                .then(res => {
                    let ifSuccess = res.data.ifSuccess;
                    if (ifSuccess) {
                        this.$message({
                            message: '申请退货成功！',
                            type: 'success'
                        });
                    } else {
                        this.$message.error(res.data.content);
                    }
                    this.unfinishedOrder_queryAll();
                })
        },
        unfinishedOrder_queryAll() {
            axios.get('/api/user/order/unfinished/queryAll?username=' + URLSafeBase64.encode(this.login_user.username))
                .then(res => {
                    this.unfinishedOrder.all = res.data;
                })
        },
        order_change_last_node(order) {
            axios.get('/api/user/unfinishedOrder/nearbyNodes?id=' + order.id)
                .then(res => {
                    this.unfinishedOrder.receiving_options = res.data.options;
                    this.unfinishedOrder.change_node_current = Object.assign({
                        order_id: order.id,
                        changed_nodeId: res.data.options[0].id,
                        user_info: res.data.user_info
                    }, order);
                    this.unfinishedOrder.changenode_Visible = true;

                    if (this.unfinishedOrder.change_node_map !== 0) {
                        this.unfinishedOrder_changeNode_map_addOverlays();
                    }
                });
        },
        unfinishedOrder_changeNode_map_addOverlays() {
            this.unfinishedOrder.change_node_map.clearOverlays();

            let w = 30;
            let h = 30;
            let img_url = "/api/img?file=seller_position&&type=png&&width=" + w + "&&height=" + h;
            let myIcon = new BMap.Icon(img_url, new BMap.Size(w, h));
            var pt = new BMap.Point(this.unfinishedOrder.change_node_current.user_info.lng,
                this.unfinishedOrder.change_node_current.user_info.lat);
            var marker = new BMap.Marker(pt, {
                icon: myIcon
            });
            this.unfinishedOrder.change_node_map.addOverlay(marker);

            let i = 0;
            let self = this;
            this.unfinishedOrder.receiving_options.forEach(point => {
                let pt = new this.unfinishedOrder.change_node_BMap.Point(point.lng, point.lat);
                let myMarker = new this.unfinishedOrder.change_node_BMap.Marker(pt, {
                    icon: new this.unfinishedOrder.change_node_BMap.Icon("/api/img?file=express&&type=png&&width=" + 20 + "&&height=" + 20, new BMap.Size(20, 20))
                });
                this.unfinishedOrder.change_node_map.addOverlay(myMarker);

                let opts = {
                    width: 0,
                    height: 0,
                };
                let id = point.id;
                let infoWindow = new this.unfinishedOrder.change_node_BMap.InfoWindow(point.address, opts);
                myMarker.addEventListener('click', function () {
                    self.unfinishedOrder.change_node_map.openInfoWindow(infoWindow, pt);
                    self.unfinishedOrder.change_node_current.changed_nodeId = point.id;
                });
                // let lab = new BMap.Label(point.address, {position: pt});
                // this.send.map.addOverlay(lab);
                i += 1;
            })
        },
        // 地图初始化时调用
        unfinishedOrder_changeNode_mapHandler({BMap, map}) {
            this.unfinishedOrder.change_node_map = map;   //将map变量存储在全局
            this.unfinishedOrder.change_node_BMap = BMap;

            this.unfinishedOrder.change_node_mapInfo.center = Object.assign({}, {
                lng: this.unfinishedOrder.change_node_current.user_info.lng,
                lat: this.unfinishedOrder.change_node_current.user_info.lat
            });
            this.unfinishedOrder_changeNode_map_addOverlays();
        },
        unfinishedOrder_change_node_submit() {
            let id = this.unfinishedOrder.change_node_current.changed_nodeId;
            let data = {
                nodeId: id,
                orderId: this.unfinishedOrder.change_node_current.order_id
            };
            console.log(data)
            axios.post('/api/user/unfinishedOrder/changeNode', data)
                .then(res => {
                    if (res.data.ifSuccess) {
                        this.$message({
                            message: '改变节点成功！',
                            type: 'success'
                        });
                    } else {
                        this.$message.error('改变节点失败！');
                    }
                    this.unfinishedOrder.changenode_Visible = false;
                })
        },
        unfinishedOrder_showRoute(order) {
            let self = this;
            let url = '/api/user/order/showCertainOrder?id=' + order.id;
            axios.get(url)
                .then(res => {
                    let deliveryInfo = res.data.route.deliveryInfo;

                    // 添加timeline样式
                    deliveryInfo.forEach(r => {
                        if (r.event == "create") {
                            r.icon = "el-icon-warning-outline";
                            r.type = "primary"
                            r.size = "large"
                        }
                        if (r.event == "sendOut" || r.event == "arrive") {
                            r.color = '#0bbd87';
                            r.size = "large"
                        }
                        if (r.event == "fetch") {
                            r.icon = "el-icon-bangzhu";
                            r.type = "warning"
                            r.size = "large"
                        }
                        if (r.event == "dispatch") {
                            r.icon = "el-icon-bicycle";
                            r.type = "warning"
                            r.size = "large"
                        }
                        if (r.event == "finish") {
                            r.icon = "el-icon-success";
                            r.type = "primary";
                            r.size = "large"
                        }
                        if (r.event == "callback") {
                            r.icon = "el-icon-remove";
                            r.type = "danger";
                            r.size = "large"
                        }
                    });
                    self.unfinishedOrder.current.deliveryInfo = deliveryInfo;
                    self.unfinishedOrder.current.deliver = res.data.deliver;
                    self.unfinishedOrder.current.receiver = res.data.receiver;
                    self.unfinishedOrder.current.nodes = res.data.route.node;
                    self.unfinishedOrder.current.route_now = res.data.route.now;

                    this.unfinishedOrder.routeVisible = true;
                    if (self.unfinishedOrder.map !== 0) {
                        self.unfinishedOrder_map_addRoute();
                    }
                });
        },
        unfinishedOrder_map_addRoute() {
            let self = this;
            let deliver = self.unfinishedOrder.current.deliver;
            let receiver = self.unfinishedOrder.current.receiver;
            let nodes = self.unfinishedOrder.current.nodes;
            let route_now = self.unfinishedOrder.current.route_now;

            self.unfinishedOrder.DrivingRoute.clearResults();
            self.unfinishedOrder.map.clearOverlays();

            // 卖家
            self.unfinishedOrder_addMarker(deliver.lng, deliver.lat, "seller", "png",
                30, 30, "卖家：" + deliver.name, "<br>" + deliver.address);
            // 买家
            self.unfinishedOrder_addMarker(receiver.lng, receiver.lat, "seller_position", "png",
                30, 30, "买家：" + receiver.name, "<br>" + receiver.address);

            let p_now = new BMap.Point(route_now.lon, route_now.lat);
            let now_label = new BMap.Label(route_now.content, {position: p_now});
            self.unfinishedOrder.map.addOverlay(now_label);

            let p_receiver = new BMap.Point(receiver.lng, receiver.lat);
            let p_deliver = new BMap.Point(deliver.lng, deliver.lat);

            let nodes_num = nodes.length;
            if (nodes_num > 0) {
                let driving = this.unfinishedOrder.DrivingRoute;
                for (let i = 0; i < nodes_num; i++) {
                    self.unfinishedOrder_addMarker(nodes[i].lng, nodes[i].lat, "express", "png",
                        20, 20, "物流节点", "<br>" + nodes[i].address);
                    if (i < nodes_num - 1) {
                        let start = new this.unfinishedOrder.BMap.Point(nodes[i].lng, nodes[i].lat);
                        let end = new this.unfinishedOrder.BMap.Point(nodes[i + 1].lng, nodes[i + 1].lat);
                        driving.search(start, end);
                    }
                }

                // 开始加线
                driving.setSearchCompleteCallback(function () {
                    if (driving.getStatus() != BMAP_STATUS_SUCCESS) {
                        this.$message.error('查询路径错误！');
                        return;
                    }

                    let pts = driving.getResults().getPlan(0).getRoute(0).getPath();    //通过驾车实例，获得一系列点的数组
                    let polyl_get = new BMap.Polyline(pts);
                    self.unfinishedOrder.map.addOverlay(polyl_get);

                    let first_node = new BMap.Point(nodes[0].lng, nodes[0].lat);
                    let last_node = new BMap.Point(nodes[nodes_num - 1].lng, nodes[nodes_num - 1].lat);

                    let pll_s = new BMap.Polyline([p_deliver, first_node], {
                        strokeColor: "#98FB98", strokeStyle: "dashed", strokeWeight: 3, strokeOpacity: 0.9
                    });
                    self.unfinishedOrder.map.addOverlay(pll_s);
                    let pll_r = new BMap.Polyline([last_node, p_receiver], {
                        strokeColor: "#FFDEAD", strokeStyle: "dashed", strokeWeight: 3, strokeOpacity: 0.9
                    });
                    self.unfinishedOrder.map.addOverlay(pll_r);

                    setTimeout(function () {
                        self.unfinishedOrder.map.setViewport([p_deliver, p_receiver, first_node, last_node
                        ]);          //调整到最佳视野
                    }, 1000);
                })
            } else {
                setTimeout(function () {
                    self.unfinishedOrder.map.setViewport([p_deliver, p_receiver
                    ]);          //调整到最佳视野
                }, 1000);
            }

        },
        unfinishedOrder_addMarker(lng, lat, img_file, img_type, w, h, info_title, info_content) {
            let self = this;
            let p = new this.unfinishedOrder.BMap.Point(lng, lat);
            let m = new this.unfinishedOrder.BMap.Marker(p, {
                icon: new this.unfinishedOrder.BMap.Icon("/api/img?file=" + img_file + "&&type=" + img_type +
                    "&&width=" + w + "&&height=" + h, new this.unfinishedOrder.BMap.Size(w, h))
            });
            this.unfinishedOrder.map.addOverlay(m);
            let opts = {
                width: 0,
                height: 0,
                title: info_title,
            };
            let infoWindow = new this.unfinishedOrder.BMap.InfoWindow(info_content, opts);
            m.addEventListener('mouseover', function () {
                self.unfinishedOrder.map.openInfoWindow(infoWindow, p);
            });
            m.addEventListener('mouseout', function () {
                self.unfinishedOrder.map.closeInfoWindow(infoWindow, p);
            });
        },
        unfinishedOrder_mapHandler({BMap, map}) {
            this.unfinishedOrder.map = map;   //将map变量存储在全局
            this.unfinishedOrder.BMap = BMap;
            this.unfinishedOrder.DrivingRoute = new this.unfinishedOrder.BMap.DrivingRoute(this.unfinishedOrder.map);

            this.unfinishedOrder_map_addRoute();
        },
        change_receiving_option(order) {
            axios.post('/api/user/order/changeReceivingOpt?id=' + order.id)
                .then(res => {
                    if (res.data.ifSuccess) {
                        this.$message({
                            message: '改变收货方式成功！',
                            type: 'success'
                        });
                    } else {
                        this.$message.error('改变收货方式失败！');
                    }
                    this.unfinishedOrder_queryAll();
                });
        },
        mapOrder_queryAll() {
            let url = '/api/user/mapOrder/queryAll?username=' + URLSafeBase64.encode(this.login_user.username);
            axios.get(url)
                .then(res => {
                    this.mapOrder.all = res.data.basicInfo;
                    this.mapOrder.mapContent = res.data.mapInfo;

                    this.mapOrder_addOverlays();
                });
        },
        mapOrder_addOverlays() {
            let self = this;
            self.mapOrder.map.clearOverlays();

            self.mapOrder.mapContent.forEach(r => {
                let pt = new BMap.Point(r.nodeLon, r.nodeLat);
                let title = r.nodeAddress;

                let marker = new BMap.Marker(pt, {
                    icon: new BMap.Icon("/api/img?file=express&&type=png&&width=" + 20 + "&&height=" + 20, new BMap.Size(20, 20))
                });

                this.mapOrder.map.addOverlay(marker);
                let opts = {
                    width: 0,
                    height: 0,
                    title: title,
                };

                let content = "待取货订单数：" + r.orderNum + "<br>";
                r.orders.forEach(t => {
                    content += "<br>" + t.orderGood;
                });
                let infoWindow = new BMap.InfoWindow(content, opts);
                marker.addEventListener('mouseover', function () {
                    self.mapOrder.map.openInfoWindow(infoWindow, pt);
                });
                marker.addEventListener('mouseout', function () {
                    self.mapOrder.map.closeInfoWindow(infoWindow, pt);
                });
            });
        },
        orderMap_zoom(order) {
            this.mapOrder.mapInfo.center = {lng: order.nodeLon, lat: order.nodeLat};
        },
        // 地图显示部分
        // 地图初始化时调用
        mapOrder_mapHandler({BMap, map}) {
            this.mapOrder.map = map;   //将map变量存储在全局
            this.mapOrder.BMap = BMap;

            this.mapOrder_addOverlays();
        },
    }
});

function getUrlParam(name) {
    //构造一个含有目标参数的正则表达式对象
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    //匹配目标参数
    var r = window.location.search.substr(1).match(reg);
    //返回参数
    if (r != null) {
        return unescape(r[2]);
    } else {
        return null;
    }
}

function onBegin() {
    app.login_user.username = URLSafeBase64.decode(getUrlParam("username"));
    app.login_user.name = URLSafeBase64.decode(getUrlParam("name"));

    app.handle_select(app.default_active, "");
}

onBegin();

