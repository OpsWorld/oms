<template>
    <div id="menu">
        <div class="login-container">
            <el-form autoComplete="on" :model="loginForm" :rules="loginRules" ref="loginForm" label-position="left"
                     label-width="0px"
                     class="card-box login-form">
                <h3 class="title">OMS运维系统</h3>
                <el-form-item prop="username">
                    <span class="svg-container"><icon class="user-icon" name="user"></icon></span>
                    <el-input name="username" type="text" v-model="loginForm.username" autoComplete="on"
                              placeholder="用户名"></el-input>
                </el-form-item>
                <el-form-item prop="password">
                    <span class="svg-container"><icon name="key"></icon></span>
                    <el-input name="password" type="password" @keyup.enter.native="handleLogin"
                              v-model="loginForm.password"
                              autoComplete="on" placeholder="密码"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" style="width:100%;" :loading="loading"
                               @click.native.prevent="handleLogin">
                        登录
                    </el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<script>
    import {Login} from "@/api/auth"
    import {mapState, mapActions} from 'vuex'

    export default {
        components: {},
        name: 'login',
        data() {
            return {
                loginForm: {
                    username: '',
                    password: ''
                },
                loginRules: {
                    username: [
                        {required: true, message: '请输入用户名', trigger: 'blur'},
                        {min: 3, message: '用户名长度不能小于3位', trigger: 'blur'}
                    ],
                    password: [
                        {required: true, message: '请输入密码', trigger: 'blur'},
                        {min: 6, message: '密码长度不能小于6位', trigger: 'blur'}
                    ]
                },
                loading: false,
                showDialog: false
            }
        },

        methods: {
            ...mapActions(['Login']),
            handleLogin() {
                this.$refs.loginForm.validate(valid => {
                    if (valid) {
                        this.loading = true;
                        this.Login(this.loginForm).then(response => {
                            this.$router.push('/');
                        }).catch(error => {
                            console.log(error);
                        });
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
        }
    }
</script>

<style rel="stylesheet/scss" lang="scss">
    @import "src/styles/mixin.scss";

    .tips {
        font-size: 14px;
        color: #fff;
        margin-bottom: 5px;
    }

    .login-container {
        @include relative;
        height: 100vh;
        /*background: url('../../assets/bg/bg2.jpg');*/
        background-color: #293444;
        background-size:cover;

        /*input:-webkit-autofill {*/
            /*-webkit-box-shadow: 0 0 0px 1000px #293444 inset !important;*/
            /*-webkit-text-fill-color: #fff !important;*/
        /*}*/
        input {
            background: transparent;
            border: 0px;
            -webkit-appearance: none;
            border-radius: 0px;
            padding: 12px 5px 12px 15px;
            color: #eeeeee;
            height: 47px;
        }
        .el-input {
            display: inline-block;
            height: 47px;
            width: 85%;
        }
        .svg-container {
            padding: 6px 5px 6px 15px;
            color: #889aa4;
        }
        .user-icon {
            margin-left: 4px;
        }

        .title {
            font-size: 26px;
            font-weight: 400;
            color: #eeeeee;
            margin: 0px auto 40px auto;
            text-align: center;
        }

        .login-form {
            position: absolute;
            left: 0;
            right: 0;
            width: 400px;
            padding: 35px 35px 15px 35px;
            margin: 120px auto;
        }

        .el-form-item {
            border: 1px solid rgba(255, 255, 255, 0.1);
            background: rgba(0, 0, 0, 0.1);
            border-radius: 5px;
            color: #454545;
        }

        .forget-pwd {
            color: #fff;
        }
    }
</style>