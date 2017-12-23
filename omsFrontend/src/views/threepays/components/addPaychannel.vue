<template>
  <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px">
    <el-form-item label="平台/商户" prop="platform">
      <el-cascader
        :options="platforms"
        :props="props"
        @change="selectPlatmerchant"
      ></el-cascader>
    </el-form-item>
    <el-form-item label="名称" prop="name">
      <el-select v-model="ruleForm.type" filterable placeholder="请选择通道名">
        <el-option v-for="item in paychannelnames" :key="item.id" :value="item.name"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="MD5KEY" prop="m_md5key">
      <el-input v-model="ruleForm.m_md5key"></el-input>
    </el-form-item>
    <el-form-item label="商户公钥" prop="m_public_key">
      <el-input v-model="ruleForm.m_public_key"></el-input>
    </el-form-item>
    <el-form-item label="商户私钥" prop="m_private_key">
      <el-input v-model="ruleForm.m_private_key"></el-input>
    </el-form-item>
    <el-form-item label="平台公钥" prop="p_public_key">
      <el-input v-model="ruleForm.p_public_key"></el-input>
    </el-form-item>
    <el-form-item label="紧急度" prop="m_backurl">
      <el-rate
        v-model="ruleForm.level"
        :colors="['#99A9BF', '#F7BA2A', '#ff1425']"
        show-text
        :texts="['E', 'D', 'C', 'B', 'A']">
      </el-rate>
      <a class="tips">Tip：星数代表问题紧急程度，星数越多，代表越紧急</a>
    </el-form-item>
    <el-form-item label="回调域名" prop="m_backurl">
      <el-input v-model="ruleForm.m_backurl"></el-input>
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
      <el-button type="primary" @click="submitForm('ruleForm')">立即创建</el-button>
      <el-button @click="resetForm('ruleForm')">重置</el-button>
    </el-form-item>
  </el-form>
</template>
<script>
import { getPlatform, getMerchant, postPayChannel, getPayChannelName } from 'api/threeticket'
import { getUser } from 'api/user'
export default {
  data() {
    return {
      ruleForm: {
        platform: '',
        merchant: '',
        type: '',
        m_md5key: '',
        m_public_key: '',
        m_private_key: '',
        p_public_key: '',
        level: 0,
        m_backurl: '',
        m_forwardurl: '',
        m_submiturl: '',
        action_user: ''
      },
      rules: {
        type: [
          { required: true, message: '请输入正确的内容', trigger: 'change' }
        ],
        m_id: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        m_md5key: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        m_public_key: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        m_private_key: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        p_public_key: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        level: [
          { required: true, type: 'number', message: '请输入正确的内容', trigger: 'blur' }
        ],
        m_backurl: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        m_forwardurl: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        m_submiturl: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
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
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          postPayChannel(this.ruleForm).then(response => {
            this.$emit('formdata', response.data)
            this.$refs[formName].resetFields()
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
        // 对象map用法
        this.platforms.map(function(data) {
          const parmas = {
            platform__name: data.name
          }
          getMerchant(parmas).then(response => {
            data['merchants'] = response.data
          })
        })
      })
    },
    getPayChannelNames() {
      getPayChannelName().then(response => {
        this.paychannelnames = response.data
      })
    },
    selectPlatmerchant(data) {
      this.ruleForm.platform = data[0]
      this.ruleForm.merchant = data[1]
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
