Vue.use(VueBaiduMap.default, {
    ak: 'MTMdfHzZv4SVWqauWpmqOwKjUEysvKpd'
});

let app = new Vue({
        el: "#app",
        data: {
            default_active: "1",
            login_user: {
                name: "",
                username: "",
                location: {lng: 114.372042, lat: 30.544861}
            },
            send: {
                all: [],
                current: {},
                search_keyword: '',
                map: 0,
                BMap: undefined,
                mapInfo: {
                    center: {},
                    zoom: 15
                },
                sending_options: [],
                addVisible: false,
                loading: false,
            },
            order: {
                all: [],
                current: {
                    diliveryInfo: []
                },
                search_keyword: '',
                map: 0,
                BMap: undefined,
                DrivingRoute: 0,
                routeVisible: false,
                mapInfo: {
                    center: {},
                    zoom: 15
                },
            },
            callback: {
                all: [],
                search_keyword: '',
            }
        },
        methods: {
            // 公共部分
            hideAll() {
                document.getElementById('sending_manage').style.display = 'none';
                document.getElementById('all_order').style.display = 'none';
                document.getElementById('callback').style.display = 'none';
            },
            handle_select(key, keyPath) {
                this.hideAll();
                switch (key) {
                    case("1"):
                        document.getElementById('sending_manage').style.display = 'block';
                        this.send_query();
                        break;
                    case("2"):
                        document.getElementById('all_order').style.display = 'block';
                        this.order_query();
                        break;
                    case("3"):
                        document.getElementById('callback').style.display = 'block';
                        this.callback_query();
                        break;
                    default:
                        document.getElementById('sending_manage').style.display = 'block';
                        break;
                }
            },
            // 用户旁设置键对应方法
            handle_command(command) {
                switch (command) {
                    case("1"):
                        break;
                    case("2"):
                        self.location = "/seller/login";
                        break;
                    default:
                        break;
                }
            },
            send_setRoute(order) {
                this.send.loading = false;
                axios.get('/api/seller/send/nearbyNodes?username=' + URLSafeBase64.encode(this.login_user.username))
                    .then(res => {
                        this.send.sending_options = res.data;
                        this.send.current = Object.assign({
                            sending_way: "1",
                            sending_nodeId: this.send.sending_options[0].id
                        }, order);
                        this.send.addVisible = true;

                        if (this.send.map !== 0) {
                            this.send_add_overlays();
                        }
                    });
            },
            send_add_overlays() {
                this.send.map.clearOverlays();

                let w = 30;
                let h = 30;
                let img_url = "/api/img?file=seller&&type=png&&width=" + w + "&&height=" + h;
                let myIcon = new BMap.Icon(img_url, new BMap.Size(w, h));
                var pt = new BMap.Point(this.login_user.location.lng, this.login_user.location.lat);
                var marker = new BMap.Marker(pt, {
                    icon: myIcon
                });
                this.send.map.addOverlay(marker);
                // this.send.map.centerAndZoom(pt,15);

                let i = 0;
                this.send.sending_options.forEach(point => {
                    let pt = new BMap.Point(point.lng, point.lat);
                    let myMarker = new BMap.Marker(pt, {
                        icon: new BMap.Icon("/api/img?file=express&&type=png&&width=" + 20 + "&&height=" + 20, new BMap.Size(20, 20))
                    });
                    this.send.map.addOverlay(myMarker);

                    let opts = {
                        width: 200,
                        height: 100,
                    };
                    let id = point.id;
                    let infoWindow = new BMap.InfoWindow(point.address, opts);
                    myMarker.addEventListener('click', function () {
                        app.send.map.openInfoWindow(infoWindow, pt);
                        app.send.current.sending_nodeId = id;
                    });
                    // let lab = new BMap.Label(point.address, {position: pt});
                    // this.send.map.addOverlay(lab);
                    i += 1;
                })
            },
            // 地图初始化时调用
            send_mapHandler({BMap, map}) {
                this.send.map = map;   //将map变量存储在全局
                this.send.BMap = BMap;

                this.send.mapInfo.center = Object.assign({}, this.login_user.location);
                this.send_add_overlays();
            },
            send_query() {
                let url = '/api/seller/send/';
                let keyword = this.send.search_keyword;
                if (keyword !== "") {
                    url = url + 'query?search_keyword=' + keyword + '&&username=' + URLSafeBase64.encode(this.login_user.username);
                } else {
                    url = url + 'queryAll?username=' + URLSafeBase64.encode(this.login_user.username);
                }
                axios.get(url)
                    .then(res => {
                        this.send.all = res.data;
                    });
            },
            send_refresh() {
                this.send.search_keyword = "";
                this.send_query();
            },
            send_submit() {
                let url = '/api/seller/send';
                let data = {
                    id: this.send.current.id,
                    chosenNodeId: this.send.current.sending_nodeId
                };
                console.log(data);
                this.send.loading = true;
                axios.post(url, data)
                    .then(res => {
                        this.send.loading = false;
                        this.send.addVisible = false;
                        if (res.data.ifSuccess) {
                            this.$message({
                                message: '发货成功！',
                                type: 'success'
                            });
                        } else {
                            this.$message.error('发货失败！');
                        }
                        this.send_query();
                    });
            },
            order_query() {
                let url = '/api/seller/order/';
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
            order_refresh() {
                this.order.search_keyword = "";
                this.order_query();
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

                this.order.mapInfo.center = Object.assign({}, this.login_user.location);
                this.order_map_addRoute();
            },
            callback_query() {
                let url = '/api/seller/order/callback/';
                let keyword = this.callback.search_keyword;
                if (keyword !== "") {
                    url = url + 'query?search_keyword=' + keyword + '&&username=' + URLSafeBase64.encode(this.login_user.username);
                } else {
                    url = url + 'queryAll?username=' + URLSafeBase64.encode(this.login_user.username);
                }
                axios.get(url)
                    .then(res => {
                        this.callback.all = res.data;
                    });
            },
            callback_fresh() {
                this.callback.search_keyword = "";
                this.callback_query();
            },
            callback_agree(order) {
                axios.get('/api/seller/order/callback/agree?id=' + order.id)
                    .then(res => {
                        if (res.data.ifSuccess) {
                            this.$message({
                                showClose: true,
                                message: '退单成功！',
                                type: "success"
                            });
                        } else {
                            this.$message.error('退单失败！');
                        }
                    })

            },
            callback_finish(order) {

            }
        }
    })
;

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

    axios.get('/api/seller/basicInfo?username=' + getUrlParam("username"))
        .then(response => {
            app.login_user.location.lng = response.data.lng;
            app.login_user.location.lat = response.data.lat;

            app.handle_select(app.default_active, "");
        });
}

onBegin();

