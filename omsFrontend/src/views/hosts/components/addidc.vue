<template>
  <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px">
    <el-form-item label="名称" prop="name">
      <el-input v-model="ruleForm.name"></el-input>
    </el-form-item>
    <el-form-item label="地址" prop="addr">
      <el-input v-model="ruleForm.addr"></el-input>
    </el-form-item>
    <el-form-item label="联系人" prop="user">
      <el-input v-model="ruleForm.user"></el-input>
    </el-form-item>
    <el-form-item label="联系人电话" prop="tel">
      <el-input v-model="ruleForm.tel"></el-input>
    </el-form-item>
    <el-form-item label="备注" prop="desc">
      <el-input v-model="ruleForm.desc" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm('ruleForm')">立即创建</el-button>
      <el-button @click="resetForm('ruleForm')">重置</el-button>
    </el-form-item>
  </el-form>
</template>
<script>
export default {
  data() {
    return {
      ruleForm: {
        name: '',
        addr: '',
        user: '',
        tel: '',
        desc: ''
      },
      rules: {
        name: [
          { required: true, message: '请输入一个正确的内容', trigger: 'blur' }
        ],
        user: [
          { required: true, message: '请输入一个正确的内容', trigger: 'blur' }
        ],
        tel: [
          { required: true, message: '请输入一个正确的内容', trigger: 'change' }
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
          this.$emit('formdata', this.ruleForm)
          this.ruleForm = {
            hostname: '',
            ip: '',
            other_ip: '',
            idc: '',
            asset_type: '',
            status: '',
            os: '',
            cpu: '',
            memory: '',
            disk: '',
            desc: ''
          }
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    }
  }
}
</script>
