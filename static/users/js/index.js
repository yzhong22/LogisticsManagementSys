Vue.use(VueBaiduMap.default, {
    ak: 'MTMdfHzZv4SVWqauWpmqOwKjUEysvKpd'
});

let app = new Vue({
    el: "#app",
    data: {
        default_active: "1",
        login_user: {
            name: "钟源",
            username: ""
        },
        address: {
            all: [{id: 1, addressDetail: "当代国际花园", receiverName: "钟源", phoneNum: "18186113076"}],
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
            current: {},
            temporal_coor: {},  // 选择的经纬度暂存于此
            search_keyword: '',
            map: 0,
            routeMapInfo: {
                center: {lng: 114.372042, lat: 30.544861},
                zoom: 16
            },
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
            all: [{id: "12321", deliverName: "nihao", orderState: 1},
                {id: "13621", deliverName: "nihaoa", orderState: 4},
                {id: "13622", deliverName: "自取", orderState: 2, receivingOption: 1},
                {id: "13623", deliverName: "派送", orderState: 2, receivingOption: 0}],
            map: 0,
            BMap: 0,
            orderNum: 2,
            routeMapInfo: {
                center: {lng: 114.372042, lat: 30.544861},
                zoom: 16
            },
            mapVisible: false,
        },
        mapOrder: {
            map: 0,
            BMap: 0,
            mapInfo: {
                center: {lng: 114.372042, lat: 30.544861},
                zoom: 16
            },
        },
        seller: {
            all: [{username: "哈哈哈", name: "你好", city: "武汉市", province: "湖北省"}]
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
            switch (key) {
                case("1"):
                    document.getElementById('address_manage').style.display = 'block';
                    break;
                case("2-1"):
                    document.getElementById('all_order').style.display = 'block';
                    break;
                case("2-2"):
                    document.getElementById('tobe_received').style.display = 'block';
                    break;
                case("2-3"):
                    document.getElementById('map_orders').style.display = 'block';
                    break;
                default:
                    document.getElementById('address_manage').style.display = 'block';
                    break;
            }
        },
        // 用户旁设置键对应方法
        handle_command(command) {
            console.log(command);
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
            let newAddress = Object.assign([], this.address.all);
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
        },
        address_query() {

        },
        address_refresh() {

        },

        // 订单部分
        order_query() {

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
                    console.log(this.order.current);
                } else {
                    return false;
                }
            });
        },
        order_refresh() {

        },
        order_check_if_changeable(order) {
            if (order.orderState < 2 && order.desChangedTimes == 0) {
                return false;
            } else {
                return true;
            }
        },

        // 待收货订单部分
        unfinishedOrder_btnCommand(command) {

        },
        // 地图显示部分
        // 地图初始化时调用
        mapOrder_mapHandler({BMap, map}) {
            this.mapOrder.map = map;   //将map变量存储在全局
            this.mapOrder.BMap = BMap;
            let myGeo = new BMap.Geocoder();
        },
    }
});

app.handle_select(app.default_active, "");

