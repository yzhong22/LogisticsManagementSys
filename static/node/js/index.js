Vue.use(VueBaiduMap.default, {
    ak: 'MTMdfHzZv4SVWqauWpmqOwKjUEysvKpd'
});

let app = new Vue({
        el: "#app",
        data: {
            default_active: "1",
            active_now: "",
            welcome_word: "请在左侧选择您所在的节点",
            login_user: {
                id: "",
                name: "",
                location: {lng: 114.372042, lat: 30.544861}
            },
            node_options: {
                all: [],
                loading: false
            },
            receive: {
                all: [],
                current: {},
                search_keyword: '',
            },
            send: {
                all: [{id: "123213214"}],
                current: {},
                search_keyword: '',
                node_change_visible: false,
                node_options: {
                    all: [],
                    loading: false,
                },
                node_change_process_loading: false
            },
            fetch: {
                all: []
            },
            dispatch: {
                all: [{id: 123213, receiverLng: 114.21, receiverLat: 30.23}],
                current: {},
                detail_visible: false,
                mapInfo: {
                    center: {lng: 0, lat: 0},
                    zoom: 14
                },
                map: 0,
                BMap: undefined,
                transit: undefined
            },

        },
        methods: {
            // 公共部分
            hideAll() {
                document.getElementById('sending_manage').style.display = 'none';
                document.getElementById('receiving_manage').style.display = 'none';
                document.getElementById('fetching').style.display = 'none';
                document.getElementById('dispatching').style.display = 'none';
            },
            handle_select(key, keyPath) {
                this.hideAll();
                this.active_now = key;
                switch (key) {
                    case("1"):
                        document.getElementById('receiving_manage').style.display = 'block';
                        break;
                    case("2"):
                        document.getElementById('sending_manage').style.display = 'block';
                        break;
                    case("3-1"):
                        document.getElementById('fetching').style.display = 'block';
                        break;
                    case("3-2"):
                        document.getElementById('dispatching').style.display = 'block';
                        break;
                    default:
                        document.getElementById('receiving_manage').style.display = 'block';
                        this.active_now = "1";
                        break;
                }
            },
            login_user_changed() {
                axios.get('api/node/info?id=' + this.login_user.id)
                    .then(res => {
                        this.login_user.name = res.data.address;
                        this.login_user.location.lng = res.data.lng;
                        this.login_user.location.lat = res.data.lat;
                        this.welcome_word = "欢迎您，" + this.login_user.name;
                        this.handle_select(this.active_now);
                    });
            },
            node_options_search(query) {
                if (query !== '') {
                    this.node_options.loading = true;
                    axios.get('/api/node/options/query?search_keyword=' + query)
                        .then(
                            res => {
                                this.node_options.all = res.data;
                                this.node_options.loading = false;
                            }
                        )
                }
            },
            next_node_search(query) {
                if (query !== '') {
                    this.send.node_options.loading = true;
                    axios.get('/api/node/options/query?search_keyword=' + query)
                        .then(
                            res => {
                                this.send.node_options.all = res.data;
                                this.send.node_options.loading = false;
                            }
                        )
                }
            },
            send_changeNode(order) {
                this.send.current = Object.assign({}, order)
                this.send.node_change_visible = true;
            },
            send_node_change() {
                console.log(this.send.current);
            },
            dispatch_show_detail(order) {
                this.dispatch.detail_visible = true;
                this.dispatch.current = Object.assign({planInfo: "路径计算中..."}, order);
                if (order.orderState == 3) {
                    this.dispatch.current.dispatcherInfo = "骑手：" + order.dispatcherName + "，电话：" + order.dispatcherPhoneNum + "。";
                } else {
                    this.dispatch.current.dispatcherInfo = "暂无骑手接单。";
                }
                this.dispatch.current.end = {lng: order.receiverLng, lat: order.receiverLat};

                if (this.dispatch.map !== 0) {
                    this.dispatch_map_process();
                }
            },
            dispatch_map_process() {
                let start = new this.dispatch.BMap.Point(this.login_user.location.lng, this.login_user.location.lat);
                let end = new this.dispatch.BMap.Point(this.dispatch.current.end.lng, this.dispatch.current.end.lat);

                if (this.dispatch.transit == undefined) {
                    let searchComplete = function (results) {
                        if (app.dispatch.transit.getStatus() != BMAP_STATUS_SUCCESS) {
                            app.dispatch.current.planInfo = "暂无派送路径信息！";
                            return;
                        }
                        let plan = results.getPlan(0);
                        let time = plan.getDuration(true);              //获取时间
                        let distance = plan.getDistance(true);            //获取距离
                        app.dispatch.current.planInfo = "预计派送时间：" + time + "，派送路程：" + distance + "。";
                    };

                    this.dispatch.transit = new this.dispatch.BMap.DrivingRoute(app.dispatch.map, {
                        renderOptions: {map: app.dispatch.map},
                        onSearchComplete: searchComplete,
                    });
                }
                this.dispatch.transit.clearResults();
                this.dispatch.transit.search(start, end);
            },
            dispatch_mapHandler({BMap, map}) {
                this.dispatch.map = map;
                this.dispatch.BMap = BMap;

                this.dispatch.mapInfo.center.lng = (this.login_user.location.lng + this.dispatch.current.end.lng) / 2;
                this.dispatch.mapInfo.center.lat = (this.login_user.location.lat + this.dispatch.current.end.lat) / 2;
                this.dispatch.mapInfo.zoom = 14;
                this.dispatch_map_process();
            }

        }
    })
;

function onBegin() {
    app.handle_select(app.default_active);
}

onBegin();

