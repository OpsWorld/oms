<template>
  <el-form :model="rowdata" :rules="rules" ref="ruleForm" label-width="100px">
    <el-form-item label="主机名" prop="hostname">
      <el-input v-model="rowdata.hostname"></el-input>
    </el-form-item>
    <el-form-item label="资产编号" prop="an">
      <el-input v-model="rowdata.an"></el-input>
    </el-form-item>
    <el-form-item label="序列号" prop="sn">
      <el-input v-model="rowdata.sn"></el-input>
    </el-form-item>
    <el-form-item label="主机ip" prop="ip">
      <el-input v-model="rowdata.ip"></el-input>
    </el-form-item>
    <el-form-item label="网关" prop="gateway">
      <el-input v-model="rowdata.gateway"></el-input>
    </el-form-item>
    <el-form-item label="外网" prop="have_net">
      <el-switch
        v-model="rowdata.have_net"
        active-color="#13ce66"
        inactive-color="#ff4949">
      </el-switch>
    </el-form-item>
    <el-form-item label="机房" prop="idc">
      <el-select v-model="rowdata.idc" placeholder="请选择机房">
        <el-option v-for="item in idcs" :key="item.name" :value="item.name"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="设备类型" prop="asset_type">
      <el-select v-model="rowdata.asset_type" placeholder="请选择设备类型">
        <el-option v-for="item in ASSET_TYPE" :key="item.key" :label="item.name" :value="item.key"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="主机状态" prop="status">
      <el-select v-model="rowdata.status" placeholder="请选择主机状态">
        <el-option v-for="item in ASSET_STATUS" :key="item.key" :label="item.name" :value="item.key"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="系统" prop="os">
      <el-input v-model="rowdata.os"></el-input>
    </el-form-item>
    <el-form-item label="cpu信息" prop="cpu">
      <el-input v-model="rowdata.cpu"></el-input>
    </el-form-item>
    <el-form-item label="内存信息" prop="memory">
      <el-input v-model="rowdata.memory"></el-input>
    </el-form-item>
    <el-form-item label="磁盘信息" prop="disk">
      <el-input v-model="rowdata.disk"></el-input>
    </el-form-item>
    <el-form-item label="描述" prop="desc">
      <el-input v-model="rowdata.desc" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm('ruleForm')">立即更新</el-button>
    </el-form-item>
  </el-form>
</template>
<script>
import { getIdc } from '@/api/host'

export default {
  props: ['rowdata'],
  data() {
    return {
      rules: {
        hostname: [
          { required: true, message: '请输入一个正确的内容', trigger: 'blur' }
        ],
        ip: [
          { required: true, message: '请输入一个正确的内容', trigger: 'blur' }
        ],
        idc: [
          { required: true, message: '请输入一个正确的内容', trigger: 'change' }
        ],
        asset_type: [
          { required: true, message: '请输入一个正确的内容', trigger: 'blur' }
        ],
        status: [
          { required: true, message: '请输入一个正确的内容', trigger: 'blur' }
        ]
      },
      ASSET_STATUS: [
        { key: 'used', name: '使用中' },
        { key: 'noused', name: '未使用' },
        { key: 'broken', name: '故障' },
        { key: 'trash', name: '废弃' }
      ],
      ASSET_TYPE: [
        { key: 'physical', name: '物理机' },
        { key: 'virtual', name: '虚拟机' },
        { key: 'container', name: '容器' },
        { key: 'network', name: '网络设备' },
        { key: 'other', name: '其他设备' }
      ],
      idcs: []
    }
  },
  created() {
    this.getIdcs()
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$emit('formdata', this.rowdata)
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    getIdcs() {
      getIdc().then(response => {
        this.idcs = response.data
      })
    }
  }
}
</script>
