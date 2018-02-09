<template>
  <el-form :model="rowdata" :rules="rules" ref="ruleForm" label-width="100px">
    <el-form-item label="名称" prop="name">
      <el-input v-model="rowdata.name"></el-input>
    </el-form-item>
    <el-form-item label="地址" prop="addr">
      <el-input v-model="rowdata.addr"></el-input>
    </el-form-item>
    <el-form-item label="联系人" prop="user">
      <el-input v-model="rowdata.user"></el-input>
    </el-form-item>
    <el-form-item label="联系人电话" prop="tel">
      <el-input v-model="rowdata.tel"></el-input>
    </el-form-item>
    <el-form-item label="描述" prop="desc">
      <el-input v-model="rowdata.desc" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm('ruleForm')">立即更新</el-button>
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
          this.$emit('formdata', this.rowdata)
        } else {
          console.log('error submit!!')
          return false
        }
      })
    }
  }
}
</script>
