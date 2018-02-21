<template>
  <el-form :model="rowdata" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
    <el-form-item label="用户组" prop="usergroups">
      <el-input v-model="rowdata.usergroups" disabled></el-input>
    </el-form-item>
    <el-form-item label="选择文档" prop="hosts">
      <sesect-datas :selectdata="rowdata.objs" @getDatas="getWikis"></sesect-datas>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm('ruleForm')">立即更新</el-button>
    </el-form-item>
  </el-form>
</template>
<script>
import sesectDatas from './wikitransfer.vue'
import { putWikiPerm } from '@/api/perm'

export default {
  components: { sesectDatas },

  props: ['rowdata'],
  data() {
    return {
      rules: {
        usergroups: [
          { required: true, message: '请输入一个正确的内容', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          putWikiPerm(this.rowdata.id, this.rowdata).then(response => {
            this.$message({
              message: '恭喜你，更新成功',
              type: 'success'
            })
            this.$emit('DialogStatus', false)
          }).catch(error => {
            this.$message.error('更新失败')
            console.log(error)
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    getWikis(data) {
      this.rowdata.objs = data
    }
  }
}
</script>
