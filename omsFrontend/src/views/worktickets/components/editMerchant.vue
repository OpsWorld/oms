<template>
  <el-form :model="rowdata" :rules="rules" ref="ruleForm" label-width="100px">
    <el-form-item label="platform" prop="platform">
      <el-select v-model="rowdata.platform" placeholder="请选择平台">
        <el-option v-for="item in platforms" :key="item.id" :value="item.name"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="名称" prop="name">
      <el-input v-model="rowdata.name"></el-input>
    </el-form-item>
    <el-form-item label="回调域名" prop="m_backurl">
      <el-input v-model="rowdata.m_backurl"></el-input>
    </el-form-item>
    <el-form-item label="商户id" prop="m_id">
      <el-input v-model="rowdata.m_id"></el-input>
    </el-form-item>
    <el-form-item label="开通通道" prop="m_channel">
      <el-checkbox-group v-model="rowdata.m_channel">
        <el-checkbox v-for="item in paychannels" :key="item.id" :label="item.name"></el-checkbox>
      </el-checkbox-group>
    </el-form-item>
    <el-form-item label="MD5KEY" prop="m_md5key">
      <el-input v-model="rowdata.m_md5key"></el-input>
    </el-form-item>
    <el-form-item label="商户公钥" prop="m_public_key">
      <el-input v-model="rowdata.m_public_key"></el-input>
    </el-form-item>
    <el-form-item label="商户私钥" prop="m_private_key">
      <el-input v-model="rowdata.m_private_key"></el-input>
    </el-form-item>
    <el-form-item label="平台公钥" prop="p_public_key">
      <el-input v-model="rowdata.p_public_key"></el-input>
    </el-form-item>
    <el-form-item label="业务经理" prop="three">
      <el-input v-model="rowdata.three"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm('ruleForm')">立即更新</el-button>
    </el-form-item>
  </el-form>
</template>
<script>
import { getPlatform, getPayChannel } from 'api/threeticket'
export default {
  props: ['rowdata'],
  data() {
    return {
      rules: {
        platform: [
          { required: true, message: '请选择一个平台', trigger: 'change' }
        ],
        name: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        m_backurl: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
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
    this.getPayChannels()
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$emit('formdata', this.rowdata)
          this.ruleForm = {
            platform: '',
            name: '',
            m_backurl: '',
            m_id: '',
            m_channel: [],
            m_md5key: '',
            m_public_key: '',
            m_private_key: '',
            p_public_key: '',
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
    },
    getPayChannels() {
      getPayChannel().then(response => {
        this.paychannels = response.data
      })
    }
  }
}
</script>
