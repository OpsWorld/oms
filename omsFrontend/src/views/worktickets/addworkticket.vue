<template xmlns="http://www.w3.org/1999/html">
  <div class="components-container" style='height:100vh'>
    <el-card>
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
        <el-form-item label="标题" prop="title">
          <el-input v-model="ruleForm.title" placeholder="请输入标题"></el-input>
        </el-form-item>
        <el-form-item label="指派人" prop="action_user">
          <el-select v-model="ruleForm.action_user" placeholder="请选择指派人">
            <el-option v-for="item in users" :key="item.id" :value="item.username"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="跟踪者" prop="follower">
          <el-select v-model="ruleForm.follower" filterable multiple placeholder="请选择跟踪者">
            <el-option v-for="item in users" :key="item.id" :value="item.username"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="工单内容" prop="content">
          <mavon-editor style="z-index: 1" default_open='edit' v-model="ruleForm.content" code_style="monokai"
                        :toolbars="toolbars" @imgAdd="imgAdd" ref="md"></mavon-editor>
        </el-form-item>
        <el-form-item label="工单等级" prop="level">
          <el-rate
            v-model="ruleForm.level"
            :colors="['#99A9BF', '#F7BA2A', '#ff1425']"
            show-text
            :texts="['E', 'D', 'C', 'B', 'A']">
          </el-rate>
          <div>
            <hr class="heng"/>
            <el-upload
              class="upload-demo"
              ref="upload"
              :action="uploadurl"
              :on-success="handleSuccess"
              :file-list="fileList"
              :disabled="count>0?true:false">
              <el-button slot="trigger" size="small" type="primary" :disabled="count>0?true:false">
                上传文件
              </el-button>
              (可以不用上传)
              <div slot="tip" class="el-upload__tip">
                <p>上传文件不超过500kb，<a style="color: red">添加工单页面只能上传1个文件</a></p>
              </div>
            </el-upload>
            <hr class="heng"/>
          </div>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="postForm('ruleForm')">提交</el-button>
          <el-button type="danger" @click="resetForm('ruleForm')">清空</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>
<script>
import { postWorkticket, postTicketenclosure } from 'api/workticket'
import ElButton from '../../../node_modules/element-ui/packages/button/src/button'
import { postUpload, postSendmail } from 'api/tool'
import { getUser } from 'api/user'
import { uploadurl } from '@/config'
import { mapGetters } from 'vuex'

export default {
  components: { ElButton },

  data() {
    return {
      route_path: this.$route.path.split('/'),
      ruleForm: {
        title: '',
        type: '',
        content: '',
        create_user: sessionStorage.getItem('username'),
        level: 2,
        action_user: '',
        follower: '',
        create_group: ''
      },
      rules: {
        title: [
          { required: true, message: '请输入工单标题', trigger: 'blur' }
        ],
        action_user: [
          { required: true, message: '请选择指派者', trigger: 'change' }
        ],
        follower: [
          { required: true, type: 'array', message: '请选择工单跟踪者', trigger: 'change' }
        ],
        content: [
          { required: true, message: '请输入工单内容', trigger: 'blur' }
        ],
        level: [
          { required: true, type: 'number', message: '请确认工单等级', trigger: 'blur' }
        ]
      },
      users: [],
      fileList: [],
      count: 0,
      enclosureFile: null,
      enclosureForm: {
        ticket: '',
        create_user: sessionStorage.getItem('username'),
        file: '',
        create_group: ''
      },
      toolbars: {
        preview: true, // 预览
        bold: true, // 粗体
        italic: true, // 斜体
        header: true, // 标题
        underline: true, // 下划线
        strikethrough: true, // 中划线
        ol: true, // 有序列表
        fullscreen: true, // 全屏编辑
        help: true
      },
      img_file: {},
      formDataList: [],
      to_list: '',
      cc_list: '',
      uploadurl: uploadurl
    }
  },

  computed: {
    ...mapGetters([
      'username'
    ])
  },
  created() {
    this.getTicketUsers()
  },
  methods: {
    postForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          console.log(this.ruleForm)
          postWorkticket(this.ruleForm).then(response => {
            if (response.statusText === 'ok') {
              this.$message({
                type: 'success',
                message: '恭喜你，新建成功'
              })
            }
            if (this.enclosureFile) {
              this.enclosureForm.file = this.enclosureFile
              this.enclosureForm.ticket = response.data.id
              postTicketenclosure(this.enclosureForm)
            }
            const mailForm = {
              to: this.ruleForm.action_user,
              cc: this.ruleForm.follower.join(),
              sub: '【新工单】' + this.ruleForm.title,
              content: window.location.href
            }
            postSendmail(mailForm).then(response => {
              this.$message({
                type: 'success',
                message: '通知邮件发送成功'
              })
            }).catch(error => {
              this.$message.error('通知邮件发送失败')
              console.log(error)
            })
            this.$router.push('/worktickets/workticket')
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
    getTicketUsers() {
      getUser().then(response => {
        this.users = response.data
      })
    },
    handleSuccess(file, fileList) {
      const formData = new FormData()
      formData.append('username', this.enclosureForm.create_user)
      formData.append('file', fileList.raw)
      formData.append('create_time', this.afterFileUpload(fileList))
      formData.append('type', fileList.type)
      formData.append('archive', this.route_path[1])
      postUpload(formData).then(response => {
        this.enclosureFile = response.data.filepath
        if (response.statusText === 'ok') {
          this.count += 1
          this.$message({
            type: 'success',
            message: '恭喜你，上传成功'
          })
        }
      }).catch(error => {
        this.$message.error('上传失败')
        this.$refs.upload.clearFiles()
        console.log(error)
      })
    },
    afterFileUpload(fileList) {
      const date = new Date(fileList.uid)
      const Y = date.getFullYear().toString()
      const M = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1)
      const D = date.getDate()
      const h = date.getHours()
      const m = date.getMinutes()
      const s = date.getSeconds()
      const ctime = Y + M + D + h + m + s
      return ctime
    },
    imgAdd(pos, file) {
      var md = this.$refs.md
      const formData = new FormData()
      formData.append('username', this.enclosureForm.create_user)
      formData.append('file', file)
      formData.append('create_time', this.afterUpload(file))
      formData.append('type', file.type)
      formData.append('archive', this.route_path[1])
      postUpload(formData).then(response => {
        md.$imglst2Url([[pos, response.data.file]])
      })
    },
    afterUpload(file) {
      const date = new Date(file.lastModified)
      const Y = date.getFullYear().toString()
      const M = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1)
      const D = date.getDate()
      const h = date.getHours()
      const m = date.getMinutes()
      const s = date.getSeconds()
      const ctime = Y + M + D + h + m + s
      return ctime
    }
    //    wsInit() {
    //      const self = this
    //      self.ws = new WebSocket(ws_url + self.ws_stream)
    //      if (self.ws.readyState === WebSocket.OPEN) self.ws.onopen()
    //      self.ws.onmessage = (e) => {
    //        this.$message({
    //          type: e.code,
    //          message: e.msg
    //        })
    //        // self.results.push(e.data);
    //      }
    //    }
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

  .addticket {
    margin: 50px;
    width: 80%;
  }
</style>
