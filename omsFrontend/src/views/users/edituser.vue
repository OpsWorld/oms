<template xmlns="http://www.w3.org/1999/html">
    <el-form :model="rowdata" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
        <el-form-item label="用户名" prop="username">
            <el-input v-model="rowdata.username"></el-input>
        </el-form-item>
        <el-form-item label="Email" prop="email">
            <el-input v-model="rowdata.email"></el-input>
        </el-form-item>
        <el-form-item label="中文名" prop="name">
            <el-input v-model="rowdata.name"></el-input>
        </el-form-item>
        <el-form-item label="用户分组" prop="group">
            <el-select v-model="rowdata.group" placeholder="请选择用户分组">
                <el-option v-for="item in groups" :key="item.name" :value="item.name"></el-option>
            </el-select>
        </el-form-item>
        <el-form-item label="是否激活" prop="is_active">
            <el-switch on-text="oo" off-text="xx" v-model="rowdata.is_active"></el-switch>
            <a v-if="changePass" style="color: #ff2ff7">有bug,需要点击这个开关显示密码</a>
        </el-form-item>
        <el-form-item label="角色" prop="group">
            <el-select v-model="rowdata.roles" placeholder="请选择用户角色">
                <el-option v-for="item in roles" :key="item.name" :value="item.name"></el-option>
            </el-select>
        </el-form-item>
        <el-form-item v-if="changePass" label="密码" prop="password">
            <el-input v-model="rowdata.password" :disabled="true">
                <template slot="append">
                    <el-button type="info" size="small" @click="setPasswd()">生成密码</el-button>
                </template>
            </el-input>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" @click="postForm('ruleForm')">提交</el-button>
            <el-button type="danger" @click="changePass=!changePass">重置密码</el-button>
        </el-form-item>
    </el-form>
</template>
<script>
    import {patchUser, getGroupList, getRoleList} from 'api/user';

    export default {
        components: {},

        props: ['rowdata'],
        data() {
            return {
                changePass: false,
                rules: {
                    username: [
                        {required: true, message: '请输入用户名', trigger: 'blur'},
                    ],
                    email: [
                        {required: true, type: 'email', message: '请输入正确的Email地址', trigger: 'blur'}
                    ],
                    name: [
                        {required: true, message: '请输入中文名', trigger: 'blur'}
                    ],
                    group: [
                        {required: true, message: '请选择项目分组', trigger: 'change'},
                    ],
                    roles: [
                        {required: true, message: '请选择角色', trigger: 'blur'},
                    ],
                },
                groups: '',
                roles: '',
            };
        },

        created() {
            this.getGroups();
            this.getRoles();
        },
        methods: {
            postForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        patchUser(this.rowdata.id, this.rowdata).then(response => {
                            if (response.statusText = 'ok') {
                                this.$message({
                                    type: 'success',
                                    message: '恭喜你，更新成功'
                                });
                            }
                        }).catch(error => {
                            this.$message.error('更新失败');
                            console.log(error);
                        });
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
                this.$emit('DialogStatus', false);
            },

            getHosts(data) {
                this.rowdata.hosts = data
            },
            getGroups() {
                getGroupList().then(response => {
                    this.groups = response.data.results;
                })
            },
            getRoles() {
                getRoleList().then(response => {
                    this.roles = response.data.results;
                })
            },
            setPasswd() {
                this.rowdata.password = Math.random().toString(35).slice(2);
                console.log(this.rowdata.password)
            },
        }
    }
</script>

<style lang='scss'>

</style>