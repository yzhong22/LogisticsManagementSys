const validatePass = (rule, value, callback) => {
    if (value === '') {
        callback(new Error('请再次输入密码'));
    } else if (value !== vue.register_form.keyword) {
        callback(new Error('两次输入密码不一致!'));
    } else {
        callback();
    }
};


vue = new Vue({
    el: "#user_register",
    data: {
        register_form: {
            username: "",
            keyword: "",
            checkpass: "",
            name: ""
        },
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
            ]
        }
    },
    methods: {
        onSubmit: function (form) {
            this.$refs[form].validate((valid) => {
                if (valid) {
                    let data = {
                        username: URLSafeBase64.encode(this.register_form.username),
                        keyword: URLSafeBase64.encode(this.register_form.keyword),
                        name: URLSafeBase64.encode(this.register_form.name)
                    };
                    axios.post('/api/user/register', data)
                        .then(response => {
                            if (response.data.ifExist == false) {
                                this.$message({
                                    message: '注册成功！即将为您跳转登录界面',
                                    type: 'success'
                                });
                                window.setTimeout("window.location='/users/login'",2000);
                                // self.location="/users/login"
                            } else {
                                this.register_form.username="";
                                this.$message({
                                    message: '该用户名已存在！',
                                    type: 'warning'
                                });
                            }
                        })
                } else {
                    return false;
                }
            });
        }
    },
})
;