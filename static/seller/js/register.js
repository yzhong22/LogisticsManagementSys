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
    el: "#register",
    data: {
        register_form: {
            username: "",
            keyword: "",
            checkpass: "",
            phoneNum: "",
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
            ],
            phoneNum: [
                {required: true, message: '请输入电话号码', trigger: 'change'}
            ]
        }
    },
    methods: {
        onSubmit: function (form) {
            this.$refs[form].validate((valid) => {
                if (valid) {
                    alert(this.register_form.username);
                } else {
                    return false;
                }
            });
        }
    },
})
;