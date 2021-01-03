Vue.use(VueBaiduMap.default, {
    ak: 'MTMdfHzZv4SVWqauWpmqOwKjUEysvKpd'
});

let app = new Vue({
    el: "#app",
    data: {
        login_user: {
            name: "",
            username: "",
            location: {
                city: '武汉市',
                address: '',
                lng: 0,
                lat: 0
            },
        },
        location_mapInfo: {
            center: {lng: 0, lat: 0},
            zoom: 14,
            map: 0,
            BMap: undefined,
        },
        order: {
            all: [{distance: '100米', receiverLng: 120.2, receiverLat: 30.1, nodeLng: 119.4, nodeLat: 29.5}],
            current: {},
            map: 0,
            BMap: undefined,
            DrivingRoute: undefined,
            mapInfo: {
                center: {lng: 0, lat: 0},
                zoom: 14
            },
            route_visible: false,
            route_disabled: true
        }

    },
    methods: {
        // 用户旁设置键对应方法
        handle_command(command) {
            switch (command) {
                case("1"):
                    break;
                case("2"):
                    self.location = "/dispatcher/login";
                    break;
                default:
                    break;
            }
        },
        locate() {
            let city = this.login_user.location.city;
            let address = this.login_user.location.address;
            let self = this;
            if (address != '' && city != '') {
                let myGeo = new self.location_mapInfo.BMap.Geocoder();
                myGeo.getPoint(address, async function (point) {
                    if (point) {
                        self.position_changed(self, point);
                        setTimeout(function () {
                            self.login_user.location.city = city;
                            self.login_user.location.address = address;
                        }, 500);
                    } else {
                        alert('您选择的地址没有解析到结果！');
                    }
                }, city)
            }
        },
        position_changed(self, point) {
            self.login_user.location.lng = point.lng;
            self.login_user.location.lat = point.lat;
            self.location_mapInfo.center = Object.assign({}, self.login_user.location);

            self.location_mapInfo.map.clearOverlays();

            let w = 30;
            let h = 30;
            let img_url = "/api/img?file=rider&&type=png&&width=" + w + "&&height=" + h;
            let myIcon = new BMap.Icon(img_url, new BMap.Size(w, h));
            let pt = new BMap.Point(self.login_user.location.lng, self.login_user.location.lat);
            let marker = new BMap.Marker(pt, {
                icon: myIcon
            });
            self.location_mapInfo.map.addOverlay(marker);

            let gc = new BMap.Geocoder();//创建地理编码器
            gc.getLocation(point, function (rs) {
                let addComp = rs.addressComponents;
                self.login_user.location.city = addComp.city;
                self.login_user.location.address = addComp.district + addComp.street + addComp.streetNumber;
                self.order.route_disabled = false;
            });
        },
        locationMap_handler({BMap, map}) {
            this.location_mapInfo.map = map;
            this.location_mapInfo.BMap = BMap;
            let self = this;

            // 创建定位控件
            let locationControl = new BMap.GeolocationControl({
                // 控件的停靠位置（可选，默认左上角）
                anchor: BMAP_ANCHOR_TOP_RIGHT,
                // 控件基于停靠位置的偏移量（可选）
                offset: new BMap.Size(20, 20)
            });

            let location_success = function (self) {
                let geolocation = new BMap.Geolocation();
                geolocation.enableSDKLocation();
                geolocation.getCurrentPosition(function (r) {
                    if (this.getStatus() == BMAP_STATUS_SUCCESS) {
                        self.position_changed(self, r.point);
                    } else {
                        alert("failed" + this.getStatus());
                    }
                });
            };

            // 将控件添加到地图上
            self.location_mapInfo.map.addControl(locationControl);
            locationControl.addEventListener("locationSuccess", function (e) {
                location_success(self);
            });
            location_success(self);
        },
        location_pick(e) {
            let self = this;
            self.position_changed(self, e.point);
        },
        grab(order) {

        },
        show_route(order) {
            this.order.route_visible = true;
            this.order.current = Object.assign({planInfo: "路径计算中..."}, order);
            this.order.current.end = {lng: order.receiverLng, lat: order.receiverLat};

            if (this.order.map !== 0) {
                this.dispatch_map_process();
            }
        },
        dispatch_map_process() {
            let location = new this.order.BMap.Point(this.login_user.location.lng, this.login_user.location.lat);
            let end = new this.order.BMap.Point(this.order.current.end.lng, this.order.current.end.lat);
            let node = new this.order.BMap.Point(this.order.current.nodeLng, this.order.current.nodeLat);
            let self = this;

            this.order.DrivingRoute.clearResults();
            this.order.map.clearOverlays();

            let driving = this.order.DrivingRoute;
            driving.search(location, node);
            driving.search(node, end);
            driving.setSearchCompleteCallback(function () {
                if (driving.getStatus() != BMAP_STATUS_SUCCESS) {
                    self.order.current.planInfo = "暂无派送路径信息！";
                    return;
                }

                let pts = driving.getResults().getPlan(0).getRoute(0).getPath();    //通过驾车实例，获得一系列点的数组
                let distance = driving.getResults().getPlan(0).getDistance(true);
                let time = driving.getResults().getPlan(0).getDuration(true);

                self.order.current.planInfo = "预计共计时间：" + time + "，路程：" + distance + "。";
                let polyl_get = new BMap.Polyline(pts);
                self.order.map.addOverlay(polyl_get);

                let w = 20;
                let h = 20;

                let location_m = new BMap.Marker(location, {
                    icon: new BMap.Icon("/api/img?file=rider&&type=png&&width=" + w + "&&height=" + h, new BMap.Size(w, h))
                });
                let node_m = new BMap.Marker(node, {
                    icon: new BMap.Icon("/api/img?file=express&&type=png&&width=" + w + "&&height=" + h, new BMap.Size(w, h))
                });
                let end_m = new BMap.Marker(end, {
                    icon: new BMap.Icon("/api/img?file=seller_position&&type=png&&width=" + w + "&&height=" + h, new BMap.Size(w, h))
                });

                self.order.map.addOverlay(location_m);
                self.order.map.addOverlay(node_m);
                self.order.map.addOverlay(end_m);
                setTimeout(function () {
                    self.order.map.setViewport([location, node, end]);          //调整到最佳视野
                }, 1000);
            })
        },
        dispatch_mapHandler({BMap, map}) {
            this.order.map = map;
            this.order.BMap = BMap;
            this.order.DrivingRoute = new this.order.BMap.DrivingRoute(this.order.map);

            this.order.mapInfo.center.lng = (this.login_user.location.lng + this.order.current.end.lng) / 2;
            this.order.mapInfo.center.lat = (this.login_user.location.lat + this.order.current.end.lat) / 2;
            this.dispatch_map_process();
        },
        grab_dialog() {
            this.grab(this.order.current);
            this.order.route_visible = false;
        }
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
}

onBegin();