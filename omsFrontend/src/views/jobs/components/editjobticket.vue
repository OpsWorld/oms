<template>
  <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px">
    <el-form-item label="标题" prop="name">
      <el-input v-model="ruleForm.name" disabled></el-input>
    </el-form-item>
    <el-form-item label="项目和版本" prop="version">
      <el-input v-model="ruleForm.version" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
    </el-form-item>
    <el-form-item label="内容" prop="content">
      <el-input v-model="ruleForm.content" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
    </el-form-item>
    <el-form-item label="通知对象" prop="skype_to">
      <el-checkbox-group v-model="ruleForm.skype_to">
        <el-checkbox v-for="item in Object.keys(skype_tos)" :key="item" :label="skype_tos[item]">
          {{skype_tos[item]}}
        </el-checkbox>
      </el-checkbox-group>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm('ruleForm')">更新</el-button>
    </el-form-item>
  </el-form>
</template>
<script>
import { putDeployTicket, postDeployTicketEnclosur } from '@/api/job'
import { postUpload, postSendmessage } from 'api/tool'
import { getUser } from 'api/user'
import { getConversionTime } from '@/utils'

export default {

  data() {
    return {
      route_path: this.$route.path.split('/'),
      ruleForm: {
        name: '',
        version: '',
        content: '',
        skype_to: [],
        create_user: localStorage.getItem('username')
      },
      rules: {
        name: [
          { required: true, message: '请输入工单标题', trigger: 'blur' }
        ],
        version: [
          { required: true, message: '请输入工单内容', trigger: 'blur' }
        ],
        content: [
          { required: true, message: '请输入工单内容', trigger: 'blur' }
        ]
      },
      fileList: [],
      count: 0,
      enclosureForm: {
        ticket: '',
        create_user: localStorage.getItem('username'),
        file: ''
      }
    }
  },

  created() {
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.ruleForm.skype_to = this.ruleForm.skype_to.join()
          putDeployTicket(this.ruleForm).then(response => {
            this.$message({
              type: 'success',
              message: '恭喜你，新建成功'
            })
            for (var fileList of this.fileList) {
              const formData = new FormData()
              formData.append('username', this.enclosureForm.create_user)
              formData.append('file', fileList)
              formData.append('create_time', getConversionTime(fileList.uid))
              formData.append('type', fileList.type)
              formData.append('archive', this.route_path[1])
              postUpload(formData).then(res => {
                this.enclosureForm.file = res.data.filepath
                this.enclosureForm.ticket = response.data.id
                postDeployTicketEnclosur(this.enclosureForm)
              })
            }
            const pramas = {
              groups__name: 'OMS_Dev_Manager'
            }
            getUser(pramas).then(uu => {
              const users = uu.data
              for (const user of users) {
                const messageForm = {
                  action_user: user.username,
                  title: '【新上线申请】' + this.ruleForm.name,
                  message: `上线内容: ${this.ruleForm.content}`
                }
                postSendmessage(messageForm)
              }
              this.addForm = false
              this.fetchData()
            })
          })
        } else {
          console.log('error submit!!')
          return false
        }
      }
      )
    }

  }
}
</script>

<style lang='scss'>

</style>
