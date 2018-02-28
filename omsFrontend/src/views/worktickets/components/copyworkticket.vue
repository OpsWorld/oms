<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px">
        <el-form-item label="转移">
          <el-radio v-model="copy" label="op">运维</el-radio>
          <el-radio v-model="copy" label="dev">研发</el-radio>
        </el-form-item>
        <el-form-item label="名称" prop="name">
          <el-input v-model="ruleForm.name" placeholder="请输入名称"></el-input>
        </el-form-item>
        <el-form-item label="类型" prop="type">
          <el-select v-model="ruleForm.type" placeholder="请选择类型">
            <el-option v-for="item in types" :key="item.id" :value="item.name"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <mavon-editor style="z-index: 1" v-model="ruleForm.content" code_style="monokai"
                        :toolbars="toolbars" @imgAdd="imgAdd" ref="md"></mavon-editor>
          <a class="tips"> Tip：截图可以直接 Ctrl + v 粘贴到内容里面</a>
        </el-form-item>
        <el-form-item label="附件">
          <el-upload
            ref="upload"
            :action="uploadurl"
            :show-file-list="false"
            :disabled="count>4"
            :before-upload="beforeAvatarUpload">
            <el-button slot="trigger" size="mini" type="success" plain :disabled="count>4">
              上传
            </el-button>
            <div slot="tip" class="el-upload__tip">
              <p><a style="color: red">最多只能上传5个文件</a></p>
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
          <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>
<script>
import {
  getWorkticket,
  putWorkticket,
  getTickettype,
  postTicketenclosure,
  getTicketenclosure,
  deleteTicketenclosure
} from 'api/workticket'
import { postDemandManager, postDemandEnclosure } from '@/api/project'
import { postopsDemandManager, postopsDemandEnclosure } from '@/api/optask'
import { postUpload, postSendmessage } from 'api/tool'
import { apiUrl, uploadurl } from '@/config'
import { getUser } from 'api/user'
import { getConversionTime } from '@/utils'

export default {
  components: {},

  data() {
    return {
      route_path: this.$route.path.split('/'),
      pid: this.$route.params.pid,
      ruleForm: {},
      rules: {
        name: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        content: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        type: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ]
      },
      copy: 'op',
      users: [],
      toolbars: {
        preview: true, // 预览
        bold: true, // 粗体
        italic: true, // 斜体
        header: true, // 标题
        underline: true, // 下划线
        strikethrough: true, // 中划线
        ol: true, // 有序列表
        help: true
      },
      apiurl: apiUrl,
      uploadurl: uploadurl,
      types: [],
      img_file: {},
      count: 0,
      enclosureData: [],
      enclosureForm: {
        project: '',
        create_user: localStorage.getItem('username'),
        file: ''
      }
    }
  },

  created() {
    this.fetchData()
    this.getTypes()
    this.fetchEnclosureData()
  },
  methods: {
    fetchData() {
      const parms = {
        pid: this.pid
      }
      getWorkticket(parms).then(response => {
        this.ruleForm = response.data[0]
      })
    },
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.ruleForm.status = 1
          putWorkticket(this.ruleForm.id, this.ruleForm).then(response => {
            this.copyWorkticket(response.data)
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
    getTypes() {
      getTickettype().then(response => {
        this.types = response.data
      })
    },
    imgAdd(pos, file) {
      var md = this.$refs.md
      const formData = new FormData()
      formData.append('username', localStorage.getItem('username'))
      formData.append('file', file)
      formData.append('create_time', getConversionTime(file.lastModified))
      formData.append('type', file.type)
      formData.append('archive', this.route_path[1])
      postUpload(formData).then(response => {
        md.$imglst2Url([[pos, response.data.file]])
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
        postTicketenclosure(this.enclosureForm)
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
        ticket__pid: this.pid
      }
      getTicketenclosure(parms).then(response => {
        this.enclosureData = response.data
      })
    },
    deleteEnclosure(id) {
      deleteTicketenclosure(id)
      this.fetchEnclosureData()
    },
    copyWorkticket(ticketData) {
      const DemandForm = {
        pid: ticketData.pid,
        name: ticketData.name,
        content: ticketData.content,
        type: '来自工单',
        create_user: ticketData.create_user,
        create_time: ticketData.create_time
      }
      if (this.copy === 'op') {
        postopsDemandManager(DemandForm).then(response => {
          this.$message({
            type: 'success',
            message: '恭喜你，转移成功'
          })
          if (this.enclosureData.length > 0) {
            for (const item of this.enclosureData) {
              const Demandenclosure = {
                project: response.data.id,
                file: item.file,
                create_user: item.create_user,
                create_time: item.create_time
              }
              postopsDemandEnclosure(Demandenclosure)
            }
          }
          const pramas = {
            groups__name: 'OMS_Dev_Manager'
          }
          getUser(pramas).then(response => {
            const users = response.data
            for (const user of users) {
              const messageForm = {
                action_user: user,
                title: '【新需求】' + DemandForm.name,
                message: `操作人: ${DemandForm.create_user}`
              }
              postSendmessage(messageForm)
            }
          })
          this.$router.push('/opstasks/opsdemands')
        }).catch(error => {
          const errordata = Object.values(error.response.data)[0]
          this.$message.error(errordata[0])
          console.log(errordata)
        })
      } else {
        postDemandManager(DemandForm).then(response => {
          this.$message({
            type: 'success',
            message: '恭喜你，转移成功'
          })
          if (this.enclosureData.length > 0) {
            for (const item of this.enclosureData) {
              const Demandenclosure = {
                project: response.data.id,
                file: item.file,
                create_user: item.create_user,
                create_time: item.create_time
              }
              postDemandEnclosure(Demandenclosure)
            }
          }
          const pramas = {
            groups__name: 'OMS_Dev_Manager'
          }
          getUser(pramas).then(response => {
            const users = response.data
            for (const user of users) {
              const messageForm = {
                action_user: user,
                title: '【新需求】' + DemandForm.name,
                message: `操作人: ${DemandForm.create_user}`
              }
              postSendmessage(messageForm)
            }
          })
          this.$router.push('/projects/demands')
        }).catch(error => {
          const errordata = Object.values(error.response.data)[0]
          this.$message.error(errordata[0])
          console.log(errordata)
        })
      }
    }
  }
}
</script>

<style lang='scss'>
</style>
