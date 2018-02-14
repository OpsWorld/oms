<template>
  <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
    <el-form-item label="关联任务" prop="project">
      <el-select v-model="ruleForm.project" filterable placeholder="请选择关联任务">
        <el-option v-for="item in projects" :key="item.id" :value="item.name"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="名称" prop="name">
      <el-input v-model="ruleForm.name"></el-input>
    </el-form-item>
    <el-form-item label="预期结果" prop="expect_result">
      <el-input v-model="ruleForm.expect_result" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
    </el-form-item>
    <el-form-item label="实际结果" prop="actual_result">
      <el-input v-model="ruleForm.actual_result" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
    </el-form-item>
    <el-form-item label="执行状态" prop="status">
      <el-select v-model="ruleForm.status" placeholder="请选择状态码">
        <el-option v-for="item in TEST_STATUS" :key="item.id" :label="item.label" :value="item.value"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="测试人员" prop="test_user">
      <el-select v-model="ruleForm.test_user" filterable placeholder="请选择用户">
        <el-option v-for="item in users" :key="item.id" :value="item.username"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="开发人员" prop="action_user">
      <el-select v-model="ruleForm.action_user" filterable placeholder="请选择用户">
        <el-option v-for="item in users" :key="item.id" :value="item.username"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="测试时间" prop="test_time">
      <el-date-picker
        v-model="ruleForm.test_time"
        type="date"
        value-format="yyyy-MM-dd"
        placeholder="选择日期时间">
      </el-date-picker>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm('ruleForm')">立即创建</el-button>
      <el-button @click="resetForm('ruleForm')">重置</el-button>
    </el-form-item>
  </el-form>
</template>
<script>
import { getUser } from 'api/user'
import { getProject } from '@/api/project'
export default {
  props: ['ruleForm'],
  data() {
    return {
      rules: {
        name: [
          { required: true, message: '请输入一个正确的内容', trigger: 'blur' }
        ]
      },
      projects: [],
      users: [],
      TEST_STATUS: [
        { 'label': 'Passed', value: '0' },
        { 'label': 'Failed', value: '1' },
        { 'label': 'Block', value: '2' },
        { 'label': 'N/A', value: '3' }
      ]
    }
  },
  created() {
    this.getUsers()
    this.getProjects()
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$emit('formdata', this.ruleForm)
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    getUsers() {
      const query = {
        groups__name: 'ITDept'
      }
      getUser(query).then(response => {
        this.users = response.data
      })
    },
    getProjects() {
      getProject().then(response => {
        this.projects = response.data
      })
    }
  }
}
</script>
