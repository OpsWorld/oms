<template>
  <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px">
    <el-form-item label="平台" prop="platform">
      <el-select v-model="ruleForm.platform" filterable placeholder="请选择平台" @change="getMerchants">
        <el-option v-for="item in platforms" :key="item.id" :value="item.name"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="商户" prop="merchant">
      <el-select v-model="ruleForm.merchant" filterable placeholder="请选择商户">
        <el-option v-for="item in merchants" :key="item.id" :value="item.name"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="类型" prop="type">
      <el-select v-model="ruleForm.type" filterable placeholder="请选择通道类型" @change="getPayChannelComplete">
        <el-option v-for="item in paychannelnames" :key="item.id" :value="item.name"></el-option>
      </el-select>
      <a v-if="showtip" style="color: #ff2e61">{{showtiptext}}</a>
    </el-form-item>
    <el-form-item label="费率" prop="rate">
      <el-input v-model="ruleForm.rate"></el-input>
    </el-form-item>
    <el-form-item label="key信息" prop="keyinfo">
      <el-input v-model="ruleForm.keyinfo" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
    </el-form-item>
    <el-form-item label="转发域名" prop="m_forwardurl">
      <el-input v-model="ruleForm.m_forwardurl"></el-input>
    </el-form-item>
    <el-form-item label="提交域名" prop="m_submiturl">
      <el-input v-model="ruleForm.m_submiturl"></el-input>
    </el-form-item>
    <el-form-item label="通知人" prop="action_user">
      <el-select v-model="ruleForm.action_user" filterable placeholder="请选择通知人">
        <el-option v-for="item in users" :key="item.id" :value="item.username"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm('ruleForm')" :disabled="showtip">立即创建</el-button>
      <el-button @click="resetForm('ruleForm')">重置</el-button>
    </el-form-item>
  </el-form>
</template>
<script>
import { getPlatform, getMerchant, postPayChannel, getPayChannelName, getPlatformPayChannel } from 'api/threeticket'
import { postSendmessage } from 'api/tool'
import { getUser } from 'api/user'

export default {
  data() {
    return {
      ruleForm: {
        platform: '',
        merchant: '',
        type: '',
        rate: '',
        keyinfo: '',
        m_forwardurl: '',
        m_submiturl: '',
        create_user: localStorage.getItem('username'),
        action_user: 'itsupport'
      },
      rules: {
        platform: [
          { required: true, message: '请输入正确的内容', trigger: 'change' }
        ],
        merchant: [
          { required: true, message: '请输入正确的内容', trigger: 'change' }
        ],
        type: [
          { required: true, message: '请输入正确的内容', trigger: 'change' }
        ],
        m_id: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        action_user: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ]
      },
      platforms: [],
      merchants: [],
      paychannelnames: [],
      users: [],
      showtip: false,
      showtiptext: ''
    }
  },
  created() {
    this.getPlatforms()
    this.getPayChannelNames()
    this.getTicketUsers()
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          postPayChannel(this.ruleForm).then(response => {
            const messageForm = {
              action_user: this.ruleForm.action_user,
              title: '【添加新支付通道】',
              message: `提交人: ${this.ruleForm.create_user}\n处理人: ${this.ruleForm.action_user}\n平台: ${this.ruleForm.platform}     商户: ${this.ruleForm.merchant}     通道: ${this.ruleForm.type}`
            }
            postSendmessage(messageForm)
            this.$emit('formdata', response.data)
            this.$refs[formName].resetFields()
          }).catch(error => {
            this.$message.error('检查此平台此商户下面通道是否已经存在')
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
    getPlatforms() {
      getPlatform().then(response => {
        this.platforms = response.data
      })
    },
    getMerchants() {
      const parmas = {
        platform__name: this.ruleForm.platform
      }
      getMerchant(parmas).then(response => {
        this.merchants = response.data
      })
    },
    getPayChannelNames() {
      getPayChannelName().then(response => {
        this.paychannelnames = response.data
      })
    },
    getTicketUsers() {
      getUser().then(response => {
        this.users = response.data
      })
    },
    getPayChannelComplete() {
      const query = {
        platform__name: this.ruleForm.platform,
        type__name: this.ruleForm.type
      }
      getPlatformPayChannel(query).then(response => {
        if (response.data.length > 0) {
          this.showtip = true
          const complete = response.data[0].complete
          if (complete === 0) {
            this.showtiptext = 'Tip：该通道已添加，但未开始对接'
          } else if (complete === 100) {
            this.showtiptext = 'Tip：该通道已添加，并已对接完成'
          } else {
            this.showtiptext = 'Tip：该通道已添加，正在对接中，对接进度为' + complete + '%'
          }
        } else {
          this.showtip = false
        }
      })
    }
  }
}
</script>
