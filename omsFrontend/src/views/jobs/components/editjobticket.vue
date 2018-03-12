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
    <el-form-item label="附件">
      <el-upload
        ref="upload"
        :action="uploadurl"
        :show-file-list="false"
        :disabled="count>2"
        :before-upload="beforeAvatarUpload">
        <el-button slot="trigger" size="mini" type="success" plain :disabled="count>4">
          上传
        </el-button>
        <div slot="tip" class="el-upload__tip">
          <p><a style="color: red">最多只能上传3个文件</a></p>
        </div>
      </el-upload>
      <hr class="heng"/>
      <div v-if='enclosureData.length>0' class="ticketenclosure">
        <ul>
          <li v-for="item in enclosureData" :key="item.id" v-if="item.file" style="list-style:none">
            <i class="fa fa-paperclip"></i>
            <a :href="apiurl + '/upload/' + item.file" :download="item.file">{{item.file.split('/')[1]}}</a>
            <el-tooltip class="item" effect="dark" content="删除附件" placement="right">
              <el-button type="text" icon="el-icon-delete" @click="deleteEnclosure(item.id)"></el-button>
            </el-tooltip>
          </li>
        </ul>
      </div>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm('ruleForm')">更新</el-button>
    </el-form-item>
  </el-form>
</template>
<script>
import {
  getDeployTicket,
  putDeployTicket,
  getDeployTicketEnclosur,
  postDeployTicketEnclosur,
  deleteDeployTicketEnclosur
} from '@/api/job'
import { postUpload } from 'api/tool'
import { apiUrl, uploadurl } from '@/config'
import { getConversionTime } from '@/utils'

export default {
  props: ['ruleForm'],
  data() {
    return {
      route_path: this.$route.path.split('/'),
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
      },
      apiurl: apiUrl,
      uploadurl: uploadurl,
      enclosureData: []
    }
  },

  created() {
    this.fetchEnclosureData()
  },
  methods: {
    submitForm() {
      const query = null
      getDeployTicket(query, this.ruleForm.id).then(res => {
        if (res.data.status === 0) {
          putDeployTicket(this.ruleForm.id, this.ruleForm).then(response => {
            this.$message({
              type: 'success',
              message: '恭喜你，更新成功'
            })
            this.$emit('DialogStatus', false)
          })
        } else {
          this.$message.error('上线工单状态已被改变')
        }
      })
    },
    beforeAvatarUpload(file) {
      const formData = new FormData()
      formData.append('username', this.enclosureForm.create_user)
      formData.append('file', file)
      formData.append('create_time', getConversionTime())
      formData.append('type', file.type)
      formData.append('archive', this.route_path[1])
      postUpload(formData).then(response => {
        this.enclosureForm.file = response.data.filepath
        this.enclosureForm.ticket = this.ruleForm.id
        postDeployTicketEnclosur(this.enclosureForm)
        if (response.statusText === 'Created') {
          this.$message({
            type: 'success',
            message: '恭喜你，上传成功'
          })
        }
        this.fetchEnclosureData()
      }).catch(error => {
        this.$message.error('上传失败')
        this.$refs.upload.clearFiles()
        console.log(error)
      })
      return true
    },
    fetchEnclosureData() {
      const parms = {
        ticket__id: this.ruleForm.id
      }
      getDeployTicketEnclosur(parms).then(response => {
        this.enclosureData = response.data
        this.count = response.data.length
      })
    },
    deleteEnclosure(id) {
      deleteDeployTicketEnclosur(id).then(() => {
        this.fetchEnclosureData()
      })
    }
  }
}
</script>

<style lang='scss'>

</style>
