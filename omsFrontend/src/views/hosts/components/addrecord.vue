<template>
  <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px">
    <el-form-item label="模块名称" prop="name">
      <el-input v-model="ruleForm.name"></el-input>
    </el-form-item>
    <el-form-item label="资产名称" prop="asset">
      <el-input v-model="ruleForm.asset"></el-input>
    </el-form-item>
    <el-form-item label="操作类型" prop="method">
      <el-select v-model="ruleForm.method" placeholder="请选择操作类型">
        <el-option v-for="item in methods" :key="item.id" :value="item"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="修改前数据" prop="before">
      <el-input v-model="ruleForm.before" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
    </el-form-item>
    <el-form-item label="修改后数据" prop="after">
      <el-input v-model="ruleForm.after" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
    </el-form-item>
    <el-form-item label="前后数据对比" prop="diff">
      <el-input v-model="ruleForm.diff" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
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
        name: 'hosts',
        asset: '',
        method: '',
        before: '',
        diff: '',
        after: ''
      },
      rules: {
        name: [
          { required: true, message: '请输入一个正确的内容', trigger: 'blur' }
        ],
        asset: [
          { required: true, message: '请输入一个正确的内容', trigger: 'blur' }
        ],
        method: [
          { required: true, message: '请输入一个正确的内容', trigger: 'change' }
        ]
      },
      methods: ['create', 'update', 'delete']
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
            name: 'hosts',
            asset: '',
            method: '',
            before: '',
            after: ''
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
