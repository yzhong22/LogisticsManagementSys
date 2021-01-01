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
                sending_options: [
                    {
                        id: 123,	// 快递节点编号
                        address: "xxxxx韵达快递",
                        distance: 12		// 与卖家的距离（单位：米）
                    }
                ],
                nearest_points: [{
                    id: 123,
                    position: {lng: 114.372042, lat: 30.544861},
                    address: "nihao",
                    show: false,
                },
                    {
                        id: 234,
                        position: {lng: 114.672042, lat: 30.244861},
                        address: "test",
                        show: false,
                    }],
                addVisible: false,
                loading: true,
            },
            order: {
                all: [],
                current: {
                    events: [{
                        content: '支持使用图标',
                        timestamp: '2018-04-12 20:46',
                        size: 'large',
                        type: 'primary',
                        icon: 'el-icon-more'
                    }, {
                        content: '支持自定义颜色',
                        timestamp: '2018-04-03 20:46',
                        color: '#0bbd87'
                    }, {
                        content: '支持自定义尺寸',
                        timestamp: '2018-04-03 20:46',
                        size: 'large'
                    }, {
                        content: '哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈',
                        timestamp: '2018-04-03 20:46'
                    }]
                },
                search_keyword: '',
                map: 0,
                BMap: undefined,
                routeVisible: false,
                mapInfo: {
                    center: {},
                    zoom: 15
                },
            },
            callback:{
                all:[{goodDescription: 'nihao',callbackState:1},{goodDescription: 'nihaoa',callbackState:2}],
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
                        this.send.mapInfo.center = Object.assign({}, this.login_user.location);
                        break;
                    case("2"):
                        document.getElementById('all_order').style.display = 'block';
                        this.order.mapInfo.center = Object.assign({}, this.login_user.location);
                        break;
                    case("3"):
                        document.getElementById('callback').style.display = 'block';
                        break;
                    default:
                        document.getElementById('sending_manage').style.display = 'block';
                        this.send.mapInfo.center = Object.assign({}, this.login_user.location);
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
                order = {};
                this.send.current = Object.assign({
                    sending_way: "1",
                    sending_nodeId: this.send.sending_options[0].id
                }, order);
                this.send.addVisible = true;
                if (this.send.map !== 0) {
                    this.send_add_overlays();
                }
            },
            send_add_overlays() {
                this.send.map.clearOverlays();
                let i = 0;
                this.send.nearest_points.forEach(point => {
                    let myMarker = new BMap.Marker(new BMap.Point(point.position.lng, point.position.lat));
                    myMarker.addEventListener('click', function () {
                        point.show = true;
                    });
                    this.send.map.addOverlay(myMarker);
                    i += 1;
                })
            },
            // 地图初始化时调用
            send_mapHandler({BMap, map}) {
                this.send.map = map;   //将map变量存储在全局
                this.send.BMap = BMap;

                this.send_add_overlays();
            },
            send_chosen_address(btn) {
                let or = btn.currentTarget.id;
                or = parseInt(or.charAt(or.length - 1));

                this.send.current.sending_nodeId = this.send.nearest_points[or].id;
                this.send.nearest_points[or].show = false;
            },
            order_queryAll() {

            },
            order_query() {
                let keyword = this.order.search_keyword;
            },
            order_showRoute(order) {
                order = {};
                this.order.routeVisible = true;
            },
            order_mapHandler({BMap, map}){
                this.order.map = map;   //将map变量存储在全局
                this.order.BMap = BMap;
            },
            callback_queryAll(){

            },
            callback_agree(order){

            },
            callback_finish(order){

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
    app.login_user.username = Base64.decode(getUrlParam("username"));
    app.login_user.name = Base64.decode(getUrlParam("name"));

    app.handle_select(app.default_active, "");
}

onBegin();

