<template>
  <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px">
    <el-form-item label="platform" prop="platform">
      <el-select v-model="ruleForm.platform" placeholder="请选择平台">
        <el-option v-for="item in platforms" :key="item.id" :value="item.name"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="名称" prop="name">
      <el-input v-model="ruleForm.name"></el-input>
    </el-form-item>
    <el-form-item label="商户id" prop="m_id">
      <el-input v-model="ruleForm.m_id"></el-input>
    </el-form-item>
    <el-form-item label="业务经理" prop="three">
      <el-input v-model="ruleForm.three"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm('ruleForm')">立即创建</el-button>
      <el-button @click="resetForm('ruleForm')">重置</el-button>
    </el-form-item>
  </el-form>
</template>
<script>
import { getPlatform } from '@/api/threeticket'
export default {
  data() {
    return {
      ruleForm: {
        platform: '',
        name: '',
        m_id: '',
        three: ''
      },
      rules: {
        platform: [
          { required: true, message: '请选择一个平台', trigger: 'change' }
        ],
        name: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        m_id: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        three: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ]
      },
      platforms: [],
      paychannels: []
    }
  },
  created() {
    this.getPlatforms()
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$emit('formdata', this.ruleForm)
          this.ruleForm = {
            platform: '',
            name: '',
            m_id: '',
            three: ''
          }
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    getPlatforms() {
      getPlatform().then(response => {
        this.platforms = response.data
      })
    }
  }
}
</script>
