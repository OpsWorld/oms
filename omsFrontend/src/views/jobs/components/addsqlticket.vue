<template>
  <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px">
    <el-form-item label="标题" prop="name">
      <el-input v-model="ruleForm.name"></el-input>
    </el-form-item>
    <el-form-item label="说明" prop="desc">
      <el-input v-model="ruleForm.desc"></el-input>
    </el-form-item>
    <el-form-item label="执行环境" prop="env">
      <el-checkbox-group v-model="ruleForm.env">
        <el-checkbox v-for="item in Object.keys(envs)" :key="item" :label="envs[item]">
          {{envs[item]}}
        </el-checkbox>
      </el-checkbox-group>
    </el-form-item>
    <el-form-item label="SQL" prop="content">
      <el-input
        type="textarea"
        :autosize="{ minRows: 10, maxRows: 32}"
        placeholder="请输入sql"
        v-model="ruleForm.content">
      </el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm('ruleForm')">立即创建</el-button>
    </el-form-item>
  </el-form>

</template>

<script>
import { postSqlTicket } from '@/api/job'
import { postSendmessage } from 'api/tool'

export default {
  data() {
    return {
      route_path: this.$route.path.split('/'),
      ruleForm: {
        name: '',
        desc: '',
        content: '',
        create_user: localStorage.getItem('username'),
        action_user: '',
        env: []
      },
      rules: {
        name: [
          { required: true, message: '请输入工单标题', trigger: 'blur' }
        ],
        desc: [
          { required: true, message: '请输入工单内容', trigger: 'blur' }
        ],
        env: [
          { required: true, type: 'array', message: '请输入工单内容', trigger: 'blur' }
        ],
        content: [
          { required: true, message: '请输入工单内容', trigger: 'blur' }
        ]
      },
      envs: { 0: '测试', 1: '正式' }
    }
  },

  created() {
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.ruleForm.env = this.ruleForm.env.join()
          postSqlTicket(this.ruleForm).then(response => {
            this.$message({
              type: 'success',
              message: '恭喜你，新建成功'
            })
            const messageForm = {
              action_user: 'itsupport',
              title: '【sql执行申请】' + this.ruleForm.name,
              message: this.ruleForm.desc
            }
            postSendmessage(messageForm)
            this.$emit('DialogStatus', false)
          }).catch(error => {
            this.$message.error('新建失败')
            console.log(error)
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    }
  }
}
</script>

<style lang='scss'>
</style>
