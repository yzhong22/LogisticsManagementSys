const validatePass = (rule, value, callback) => {
    if (value === '') {
        callback(new Error('请再次输入密码'));
    } else if (value !== vue.register_form.keyword) {
        callback(new Error('两次输入密码不一致!'));
    } else {
        callback();
    }
};

// Vue.use(VueBaiduMap.default, {
//     ak: 'MTMdfHzZv4SVWqauWpmqOwKjUEysvKpd'
// });

vue = new Vue({
    el: "#register",
    data: {
        register_form: {
            username: "",
            keyword: "",
            checkpass: "",
            phoneNum: "",
            name: "",
            province: "",
            city: "",
            addressDetail: ""
        },
        loading: false,
        register_rules: {
            username: [
                {required: true, message: '请输入用户名', trigger: 'change'},
                {min: 5, max: 16, message: '长度在 5 到 16 个字符', trigger: 'change'}
            ],
            keyword: [
                {required: true, message: '请输入密码', trigger: 'change'},
                {min: 6, max: 40, message: '请至少输入6位密码', trigger: 'change'}
            ],
            checkpass: [
                {validator: validatePass, trigger: 'change'}
            ],
            name: [
                {required: true, message: '请输入姓名', trigger: 'change'}
            ],
            phoneNum: [
                {required: true, message: '请输入电话号码', trigger: 'change'}
            ],
            province: [
                {required: true, message: '请输入所在省', trigger: 'change'}
            ],
            city: [
                {required: true, message: '请输入市', trigger: 'change'}
            ],
            addressDetail: [
                {required: true, message: '请输入详细地址', trigger: 'change'}
            ],
        }
    },
    methods: {
        onSubmit: function (form) {
            this.$refs[form].validate((valid) => {
                if (valid) {
                    this.loading = true;
                    let myGeo = new BMapGL.Geocoder();
                    myGeo.getPoint(this.register_form.addressDetail, function (point) {
                        if (point) {
                            let data = {
                                username: URLSafeBase64.encode(vue.register_form.username),
                                keyword: URLSafeBase64.encode(vue.register_form.keyword),
                                name: URLSafeBase64.encode(vue.register_form.name),
                                phoneNum: vue.register_form.phoneNum,
                                province: vue.register_form.province,
                                city: vue.register_form.city,
                                addressDetail: vue.register_form.addressDetail,
                                addressLon: point.lng,
                                addressLat: point.lat
                            };

                            axios.post('/api/seller/register', data)
                                .then(response => {
                                    if (response.data.ifExist == false) {
                                        vue.$message({
                                            message: '注册成功！即将为您跳转登录界面',
                                            type: 'success'
                                        });
                                        vue.loading = false;
                                        window.setTimeout("window.location='/seller/login'", 2000);
                                    } else {
                                        vue.register_form.username = "";
                                        vue.$message({
                                            message: '该用户名已存在！',
                                            type: 'warning'
                                        });
                                    }
                                })
                        } else {
                            vue.$message({
                                message: '坐标转换失败！',
                                type: 'warning'
                            });
                        }
                    }, this.register_form.city);
                } else {
                    return false;
                }
            });
        }
    },
})
;