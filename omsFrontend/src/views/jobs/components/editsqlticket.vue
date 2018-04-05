<template>
  <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px">
    <el-form-item label="标题" prop="name">
      <el-input v-model="ruleForm.name"></el-input>
    </el-form-item>
    <el-form-item label="说明" prop="desc">
      <el-input v-model="ruleForm.desc"></el-input>
    </el-form-item>
    <el-form-item label="执行环境" prop="env">
      <el-checkbox-group v-model="ruleForm.env">
        <el-checkbox v-for="item in Object.keys(envs)" :key="item" :label="envs[item]">
          {{envs[item]}}
        </el-checkbox>
      </el-checkbox-group>
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
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        desc: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        env: [
          { required: true, type: 'array', message: '请输入正确的内容', trigger: 'blur' }
        ],
        content: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ]
      },
      envs: { 0: '测试', 1: '正式' }
    }
  },

  created() {
    this.ruleForm.env = this.ruleForm.env.split(',')
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.ruleForm.env = this.ruleForm.env.join()
          putSqlTicket(this.ruleForm.id, this.ruleForm).then(response => {
            this.$message({
              type: 'success',
              message: '恭喜你，更新成功'
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
    }

  }
}
</script>

<style lang='scss'>
</style>
