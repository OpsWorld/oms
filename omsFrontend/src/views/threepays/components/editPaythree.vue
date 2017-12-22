<template>
  <el-form :model="rowdata" :rules="rules" ref="ruleForm" label-width="100px">
    <el-form-item label="商户" prop="merchant">
      <el-select v-model="rowdata.merchant" placeholder="请选择商户">
        <el-option v-for="item in merchants" :key="item.id" :value="item.name"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="名称" prop="name">
      <el-input v-model="rowdata.name"></el-input>
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
    <el-form-item label="紧急度" prop="m_backurl">
      <el-rate
        v-model="rowdata.level"
        :colors="['#99A9BF', '#F7BA2A', '#ff1425']"
        show-text
        :texts="['E', 'D', 'C', 'B', 'A']">
      </el-rate>
      <a class="tips">Tip：星数代表问题紧急程度，星数越多，代表越紧急</a>
    </el-form-item>
    <el-form-item label="回调域名" prop="m_backurl">
      <el-input v-model="rowdata.m_backurl"></el-input>
    </el-form-item>
    <el-form-item label="转发域名" prop="m_backurl">
      <el-input v-model="rowdata.m_forwardurl"></el-input>
    </el-form-item>
    <el-form-item label="提交域名" prop="m_backurl">
      <el-input v-model="rowdata.m_submiturl"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm('ruleForm')">立即创建</el-button>
      <el-button @click="resetForm('ruleForm')">重置</el-button>
    </el-form-item>
  </el-form>
</template>
<script>
import { getMerchant } from 'api/threeticket'
export default {
  props: ['rowdata'],
  data() {
    return {
      rules: {
        merchant: [
          { required: true, message: '请选择一个平台', trigger: 'change' }
        ],
        name: [
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
        levle: [
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
      merchants: []
    }
  },
  created() {
    this.getMerchants()
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$emit('formdata', this.rowdata)
          this.rowdata = {
            merchant: '',
            name: '',
            m_id: '',
            m_md5key: '',
            m_public_key: '',
            m_private_key: '',
            p_public_key: '',
            levle: '',
            m_backurl: '',
            m_forwardurl: '',
            m_submiturl: ''
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
    getMerchants() {
      getMerchant().then(response => {
        this.platforms = response.data
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
