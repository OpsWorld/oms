<template xmlns="http://www.w3.org/1999/html">
    <div>
        <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
            <el-form-item label="标题" prop="title">
                <el-input v-model="ruleForm.title"></el-input>
            </el-form-item>
            <el-form-item label="工单类型" prop="type">
                <el-select v-model="ruleForm.type" placeholder="请选择工单类型">
                    <el-option v-for="item in tickettypes" :key="item.name" :value="item.name"></el-option>
                </el-select>
                <el-tooltip class="item" effect="dark" content="添加新工单类型" placement="right">
                    <el-button type="success" icon="plus" @click="addForm=true"></el-button>
                </el-tooltip>
            </el-form-item>
            <el-form-item label="工单内容" prop="content">
                <el-input v-model="ruleForm.content" type="textarea" :autosize="{ minRows: 10, maxRows: 50}"></el-input>
            </el-form-item>
            <el-form-item label="工单等级" prop="level">
                <el-rate
                        v-model="ruleForm.level"
                        :colors="['#99A9BF', '#F7BA2A', '#ff1425']"
                        show-text
                        :texts="['E', 'D', 'C', 'B', 'A']">
                </el-rate>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="postForm('ruleForm')">提交</el-button>
                <el-button type="danger" @click="resetForm('ruleForm')">清空</el-button>
            </el-form-item>
        </el-form>
        <el-dialog :visible.sync="addForm">
            <add-group @formdata="addGroupSubmit" @DialogStatus="getDialogStatus"></add-group>
        </el-dialog>
    </div>
</template>
<script>
    import {postWorkticket, getTickettype, postTickettype} from 'api/workticket'
    import ElButton from "../../../node_modules/element-ui/packages/button/src/button";
    import addGroup from '../components/addgroup.vue'

    export default {
        components: {ElButton, addGroup},

        data() {
            return {
                ruleForm: {
                    title: '',
                    type: '',
                    content: '',
                    create_user: localStorage.getItem('username'),
                    level: null,
                    action_user: '',
                    create_group: ''
                },
                rules: {
                    title: [
                        {required: true, message: '请输入工单标题', trigger: 'blur'},
                    ],
                    type: [
                        {required: true, message: '请选择工单类型', trigger: 'change'}
                    ],
                    content: [
                        {required: true, message: '请输入工单内容', trigger: 'blur'}
                    ],
                    level: [
                        {required: true, type: 'number', message: '请确认工单等级', trigger: 'blur'},
                    ],
                },
                tickettypes: [],
                addForm: false
            };
        },

        created() {
            this.getTickettypes();
        },
        methods: {
            postForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        postWorkticket(this.ruleForm).then(response => {
                            if (response.statusText = 'ok') {
                                this.$message({
                                    type: 'success',
                                    message: '恭喜你，新建成功'
                                });
                            }
                            this.$refs[formName].resetFields();
                        });
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
                this.$emit('DialogStatus', false);
            },

            getDialogStatus(data) {
                this.addForm = data;
            },
            resetForm(formName) {
                this.$refs[formName].resetFields();
            },
            getTickettypes() {
                getTickettype().then(response => {
                    this.tickettypes = response.data.results;
                })
            },
            addGroupSubmit(formdata) {
                postTickettype(formdata).then(response => {
                    this.$message({
                        message: '恭喜你，添加成功',
                        type: 'success'
                    });
                    setTimeout(this.getTickettypes, 1000);
                    this.addForm = false
                }).catch(error => {
                    this.$message.error('添加失败');
                    console.log(error);
                });
            },
        }
    }
</script>

<style lang='scss'>

</style>