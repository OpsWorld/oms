<template>
  <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px">
    <el-form-item label="商户" prop="platform">
      <el-input v-model="rowdata.name" disabled></el-input>
    </el-form-item>
    <el-form-item label="名称" prop="name">
      <el-select v-model="ruleForm.name" filterable placeholder="请选择通道名">
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
    <el-form-item>
      <el-button type="primary" @click="submitForm('ruleForm')">立即创建</el-button>
      <el-button @click="resetForm('ruleForm')">重置</el-button>
    </el-form-item>
  </el-form>
</template>
<script>
import { getMerchant, postPayChannel, getPayChannelName } from 'api/threeticket'
export default {
  props: ['rowdata', 'state'],
  data() {
    return {
      ruleForm: {
        merchant: '',
        name: '',
        m_md5key: '',
        m_public_key: '',
        m_private_key: '',
        p_public_key: '',
        level: 0,
        m_backurl: '',
        m_forwardurl: '',
        m_submiturl: ''
      },
      rules: {
        merchant: [
          { required: true, message: '请选择一个平台', trigger: 'change' }
        ],
        name: [
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
        ]
      },
      merchants: [],
      paychannelnames: []
    }
  },
  created() {
    //      this.getMerchants()
    this.getPayChannelNames()
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.ruleForm.merchant = this.rowdata.id
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
    getMerchants() {
      getMerchant().then(response => {
        this.merchants = response.data
      })
    },
    getPayChannelNames() {
      getPayChannelName().then(response => {
        this.paychannelnames = response.data
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
