let vue = new Vue({
    el: "#dispatcher_login",
    data: {
        login_form: {
            username: "",
            keyword: ""
        },
        rules: {
            username: [
                {required: true, message: '请输入用户名', trigger: 'change'},
            ],
            keyword: [
                {required: true, message: '请输入密码', trigger: 'change'},
            ],
        }
    },
    methods: {
        onSubmit: function (form) {
            this.$refs[form].validate((valid) => {
                if (valid) {
                    let data = {
                        username: URLSafeBase64.encode(this.login_form.username),
                        keyword: URLSafeBase64.encode(this.login_form.keyword)
                    };

                    axios.post('/api/dispatcher/login', data)
                        .then(response => {
                            if (response.data.ifSuccess === false) {
                                this.$message.error('用户名或密码错误！')
                            } else {
                                self.location = "/dispatcher?username=" + response.data.username + "&&name=" + response.data.name;
                            }
                        })
                } else {
                    return false;
                }
            });
        },

    }
});