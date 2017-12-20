<template>
  <el-form :model="rowdata" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
    <el-form-item label="名称" prop="name">
      <el-input v-model="rowdata.name"></el-input>
    </el-form-item>
    <el-form-item label="描述" prop="desc">
      <el-input v-model="rowdata.desc" type="textarea" :autosize="{ minRows: 10, maxRows: 30}"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm('ruleForm')">立即创建</el-button>
    </el-form-item>
  </el-form>
</template>
<script>
export default {
  props: ['rowdata'],
  data() {
    return {
      rules: {
        name: [
          { required: true, message: '请输入一个风骚的名字', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$emit('formdata', this.rowdata)
          this.ruleForm = {
            name: '',
            desc: ''
          }
        } else {
          console.log('error submit!!')
          return false
        }
      })
    }
  }
}
</script>
