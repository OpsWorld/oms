<template>
  <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
    <el-form-item label="用户组" prop="usergroups">
      <el-select v-model="ruleForm.usergroups" placeholder="请选择用户组">
        <el-option v-for="item in groups" :key="item.name" :value="item.name"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="选择主机" prop="hosts">
      <sesect-hosts :selecthost="ruleForm.objs" @gethosts="getHosts"></sesect-hosts>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm('ruleForm')">立即创建</el-button>
      <el-button @click="resetForm('ruleForm')">重置</el-button>
    </el-form-item>
  </el-form>
</template>
<script>
import sesectHosts from 'views/components/hosttransfer.vue'
import { getGroup } from 'api/user'
import { postHostPerm } from '@/api/perm'

export default {
  components: { sesectHosts },

  data() {
    return {
      ruleForm: {
        usergroups: '',
        objs: []
      },
      rules: {
        usergroups: [
          { required: true, message: '请输入一个正确的内容', trigger: 'blur' }
        ]
      },
      groups: []
    }
  },
  created() {
    this.getGroups()
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          postHostPerm(this.ruleForm).then(response => {
            this.$message({
              message: '恭喜你，添加成功',
              type: 'success'
            })
            this.ruleForm = {
              usergroups: '',
              objs: []
            }
            this.$emit('DialogStatus', false)
          }).catch(error => {
            this.$message.error('添加失败')
            console.log(error)
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    getHosts(data) {
      this.ruleForm.objs = data
    },
    getGroups() {
      getGroup().then(response => {
        this.groups = response.data
      })
    }
  }
}
</script>
