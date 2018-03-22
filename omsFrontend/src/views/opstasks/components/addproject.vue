<template>
  <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px">
    <el-form-item label="名称" prop="name">
      <el-input v-model="ruleForm.name" placeholder="请输入名称"></el-input>
    </el-form-item>
    <el-form-item label="指派人" prop="action_user">
      <el-select v-model="ruleForm.action_user" filterable placeholder="请选择指派人">
        <el-option v-for="item in users" :key="item.id" :value="item.username"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="内容" prop="content">
      <el-input v-model="ruleForm.content" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
    </el-form-item>
    <el-form-item label="时间" prop="time">
      <el-date-picker
        v-model="ruleForm.time"
        type="daterange"
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        value-format="yyyy-MM-dd">
      </el-date-picker>
    </el-form-item>
    <el-form-item label="发送通知" prop="sendnotice">
      <el-checkbox v-model="sendnotice">发送通知</el-checkbox>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="postForm('ruleForm')">提交</el-button>
      <el-button type="danger" @click="resetForm('ruleForm')">清空</el-button>
    </el-form-item>
  </el-form>
</template>
<script>
import { postProject } from '@/api/optask'
import { postSendmessage } from 'api/tool'
import { getUser } from 'api/user'
import { getConversionTime } from '@/utils'

export default {
  components: {},
  props: ['demand'],
  data() {
    return {
      route_path: this.$route.path.split('/'),
      ruleForm: {
        name: '',
        content: '',
        create_user: localStorage.getItem('username'),
        level: 1,
        complete: 0,
        action_user: '',
        pid: '',
        is_public: true,
        time: []
      },
      rules: {
        name: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        action_user: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        content: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        time: [
          { required: true, type: 'array', message: '请输入正确的内容', trigger: 'blur' }
        ]
      },
      users: [],
      sendnotice: false
    }
  },

  created() {
    this.getUsers()
  },
  methods: {
    postForm(formName) {
      this.ruleForm.demand = this.demand
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.ruleForm.start_time = this.ruleForm.time[0]
          this.ruleForm.end_time = this.ruleForm.time[1]
          this.ruleForm.pid = 'pps' + getConversionTime()
          postProject(this.ruleForm).then(response => {
            if (response.statusText === '"Created"') {
              this.$message({
                type: 'success',
                message: '恭喜你，新建成功'
              })
            }
            if (this.sendnotice) {
              const messageForm = {
                action_user: this.ruleForm.action_user,
                title: `【${this.ruleForm.type}】${this.ruleForm.title}`,
                message: `提交人: ${this.ruleForm.create_user}\n指派人: ${this.ruleForm.action_user}`
              }
              postSendmessage(messageForm)
            }
            this.$emit('DialogStatus', false)
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
    getUsers() {
      const query = {
        groups__name: 'ITDept'
      }
      getUser(query).then(response => {
        this.users = response.data
      })
    }
  }
}
</script>

<style lang='scss'>

</style>
