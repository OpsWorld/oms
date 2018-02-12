<template>
  <el-form :model="rowdata" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
    <el-form-item label="用户组" prop="usergroups">
      <el-input v-model="rowdata.usergroups" disabled></el-input>
    </el-form-item>
    <el-form-item label="选择主机" prop="hosts">
      <sesect-hosts :selecthost="rowdata.objs" @gethosts="getHosts"></sesect-hosts>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm('ruleForm')">立即更新</el-button>
    </el-form-item>
  </el-form>
</template>
<script>
import sesectHosts from 'views/components/hosttransfer.vue'

export default {
  components: { sesectHosts },

  props: ['rowdata'],
  data() {
    return {
      rules: {
        usergroups: [
          { required: true, message: '请输入一个正确的内容', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
  },

  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$emit('formdata', this.rowdata)
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    getHosts(data) {
      this.rowdata.objs = data
    }
  }
}
</script>
