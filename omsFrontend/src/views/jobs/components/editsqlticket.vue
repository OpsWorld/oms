<template>
  <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px">
    <el-form-item label="标题" prop="name">
      <el-input v-model="ruleForm.name"></el-input>
    </el-form-item>
    <el-form-item label="说明" prop="desc">
      <el-input v-model="ruleForm.desc"></el-input>
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
      <el-button type="primary" @click="submitForm('ruleForm')">立即更新</el-button>
    </el-form-item>
  </el-form>

</template>

<script>
import { putSqlTicket } from '@/api/job'

export default {
  props: ['ruleForm'],
  data() {
    return {
      route_path: this.$route.path.split('/'),
      rules: {
        name: [
          { required: true, message: '请输入工单标题', trigger: 'blur' }
        ],
        desc: [
          { required: true, message: '请输入工单内容', trigger: 'blur' }
        ],
        content: [
          { required: true, message: '请输入工单内容', trigger: 'blur' }
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
          putSqlTicket(this.ruleForm.id, this.ruleForm).then(response => {
            this.$message({
              type: 'success',
              message: '恭喜你，新建成功'
            })
          }).catch(error => {
            this.$message.error('新建失败')
            console.log(error)
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
      this.$emit('DialogStatus', false)
    }

  }
}
</script>

<style lang='scss'>
</style>
