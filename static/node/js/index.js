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
        },
        methods: {
            // 公共部分
            hideAll() {
                document.getElementById('sending_manage').style.display = 'none';
                document.getElementById('receiving_manage').style.display = 'none';
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
                    case("3"):
                        document.getElementById('dispatching').style.display = 'block';
                        break;
                    default:
                        document.getElementById('receiving_manage').style.display = 'block';
                        this.active_now = "1";
                        break;
                }
            },
            login_user_changed() {
                for (let i = 0; i < this.node_options.all.length; i++) {
                    let option = this.node_options.all[i];
                    if (option.id === this.login_user.id) {
                        this.login_user.name = option.address;
                        this.welcome_word = "欢迎您，" + this.login_user.name;
                        break;
                    }
                }
                this.handle_select(this.active_now);
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
            order_queryAll() {

            },
            order_query() {
                let keyword = this.order.search_keyword;
            },
            order_showRoute(order) {
                order = {};
                this.order.routeVisible = true;
            },
            order_mapHandler({BMap, map}) {
                this.order.map = map;   //将map变量存储在全局
                this.order.BMap = BMap;

                this.order.mapInfo.center = Object.assign({}, this.login_user.location);
            },
            callback_queryAll() {

            },
            callback_agree(order) {

            },
            callback_finish(order) {

            }
        }
    })
;

function onBegin() {
    app.handle_select(app.default_active);
}

onBegin();

