<template>
  <el-form :model="rowdata" :rules="rules" ref="ruleForm" label-width="100px">
    <el-form-item label="平台" prop="platform">
      <el-select v-model="rowdata.platform" filterable placeholder="请选择平台" @change="getMerchants">
        <el-option v-for="item in platforms" :key="item.id" :value="item.name"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="商户" prop="merchant">
      <el-select v-model="rowdata.merchant" filterable placeholder="请选择商户">
        <el-option v-for="item in merchants" :key="item.id" :value="item.name"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="类型" prop="type">
      <el-select v-model="rowdata.type" filterable placeholder="请选择类型">
        <el-option v-for="item in paychannelnames" :key="item.id" :value="item.name"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="key信息" prop="keyinfo">
      <el-input v-model="rowdata.keyinfo" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
    </el-form-item>
    <el-form-item label="紧急度" prop="m_backurl">
      <el-rate
        v-model="rowdata.level"
        :colors="['#99A9BF', '#F7BA2A', '#ff1425']"
        show-text
        :texts="['E', 'D', 'C', 'B', 'A']">
      </el-rate>
      <a class="tips">Tip：星数代表问题紧急程度，星数越多，代表越紧急</a>
    </el-form-item>
    <el-form-item label="转发域名" prop="m_forwardurl">
      <el-input v-model="rowdata.m_forwardurl"></el-input>
    </el-form-item>
    <el-form-item label="提交域名" prop="m_submiturl">
      <el-input v-model="rowdata.m_submiturl"></el-input>
    </el-form-item>
    <el-form-item label="通知人" prop="action_user">
      <el-select v-model="rowdata.action_user" filterable placeholder="请选择通知人">
        <el-option v-for="item in users" :key="item.id" :value="item.username"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm('ruleForm')">更新</el-button>
    </el-form-item>
  </el-form>
</template>
<script>
import { getPlatform, getMerchant, putPayChannel, getPayChannelName } from 'api/threeticket'
import { getUser } from 'api/user'
import { postSendmessage } from 'api/tool'

export default {
  props: ['rowdata'],
  data() {
    return {
      create_user: localStorage.getItem('username'),
      rules: {
        type: [
          { required: true, message: '请输入正确的内容', trigger: 'change' }
        ],
        m_id: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        keyinfo: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        level: [
          { required: true, type: 'number', message: '请输入正确的内容', trigger: 'blur' }
        ],
        action_user: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ]
      },
      platforms: [],
      merchants: [],
      paychannelnames: [],
      props: {
        label: 'name',
        value: 'name',
        children: 'merchants'
      },
      users: []
    }
  },
  created() {
    this.getPlatforms()
    this.getPayChannelNames()
    this.getTicketUsers()
    this.getMerchants()
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          putPayChannel(this.rowdata.id, this.rowdata).then(response => {
            const messageForm = {
              action_user: this.rowdata.action_user,
              title: '【支付通道修改】',
              message: `修改人: ${this.create_user}\n处理人: ${this.rowdata.action_user}\n平台: ${this.rowdata.platform}     商户: ${this.rowdata.merchant}     通道: ${this.rowdata.type}`
            }
            postSendmessage(messageForm)
            this.$emit('formdata', response.data)
            this.$refs[formName].resetFields()
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    getPlatforms() {
      getPlatform().then(response => {
        this.platforms = response.data
      })
    },
    getMerchants() {
      const parmas = {
        platform__name: this.rowdata.platform
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
    }
  }
}
</script>

<style lang='scss'>
  .heng {
    margin: 20px 0;
    height: 1px;
    border: 0px;
    background-color: rgba(174, 127, 255, 0.38);
    color: #29e11c;
  }

  .tips {
    color: rgba(128, 128, 128, 0.82);
  }
</style>
