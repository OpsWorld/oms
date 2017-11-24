<template>
    <el-form :model="rowdata" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
        <el-form-item label="名称" prop="name">
            <el-input v-model="rowdata.name"></el-input>
        </el-form-item>
        <el-form-item label="描述" prop="desc">
            <el-input v-model="rowdata.desc" type="textarea"></el-input>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
        </el-form-item>
    </el-form>
</template>
<script>
    import {putTickettype} from 'api/workticket'
    export default {
        props: ['rowdata'],
        data() {
            return {
                rules: {
                    name: [
                        {required: true, message: '请陛下输入一个风骚的名字', trigger: 'blur'},
                    ]
                }
            };
        },
        methods: {
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        putTickettype(this.rowdata.id, this.rowdata).then(response => {
                            if (response.statusText = 'ok') {
                                this.$message({
                                    type: 'success',
                                    message: '恭喜你，更新成功'
                                });
                            }
                        });
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
                this.$emit('DialogStatus', false);
            }
        }
    }
</script>