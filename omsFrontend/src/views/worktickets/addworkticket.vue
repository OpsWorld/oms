<template xmlns="http://www.w3.org/1999/html">
  <div class="components-container" style='height:100vh'>
    <el-card>
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
        <el-form-item label="标题" prop="title">
          <el-input v-model="ruleForm.title" placeholder="请输入标题"></el-input>
        </el-form-item>
        <el-form-item label="指派人" prop="action_user">
          <el-select v-model="ruleForm.action_user" filterable placeholder="请选择指派人">
            <el-option v-for="item in users" :key="item.id" :value="item.username"></el-option>
          </el-select>
          <a class="tips"> Tip：当前工单处理人，默认是指派给ITSupport群组</a>
        </el-form-item>
        <el-form-item label="跟踪者" prop="follower">
          <el-select v-model="ruleForm.follower" filterable multiple placeholder="请选择跟踪者">
            <el-option v-for="item in users" :key="item.id" :value="item.username"></el-option>
          </el-select>
          <a class="tips"> Tip：工单状态发生变更时，邮件抄送给跟踪者</a>
        </el-form-item>
        <el-form-item label="工单类型" prop="type">
          <el-select v-model="ruleForm.type" placeholder="请选择工单类型">
            <el-option v-for="item in types" :key="item.id" :value="item.name"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="工单内容" prop="content">
          <mavon-editor style="z-index: 1" v-model="ruleForm.content" code_style="monokai"
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
              :disabled="count>2?true:false">
              <el-button slot="trigger" size="small" type="primary" :disabled="count>0?true:false">
                上传文件
              </el-button>
              (可以不用上传)
              <div slot="tip" class="el-upload__tip">
                <p>上传文件不超过10m，<a style="color: red">最多只能上传3个文件</a></p>
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
import { postWorkticket, postTicketenclosure, getTickettype } from 'api/workticket'
import ElButton from '../../../node_modules/element-ui/packages/button/src/button'
import { postUpload, postSendmail } from 'api/tool'
import { getUser } from 'api/user'
import { uploadurl } from '@/config'
import { mapGetters } from 'vuex'
import getTime from '@/utils/conversionTime'

export default {
  components: { ElButton },

  data() {
    return {
      route_path: this.$route.path.split('/'),
      ruleForm: {
        title: '',
        type: '',
        content: '',
        create_user: localStorage.getItem('username'),
        level: 2,
        action_user: 'itsupport',
        follower: '',
        create_group: '',
        ticketid: ''
      },
      rules: {
        title: [
          { required: true, message: '请输入工单标题', trigger: 'blur' }
        ],
        content: [
          { required: true, message: '请输入工单内容', trigger: 'blur' }
        ],
        type: [
          { required: true, message: '请选择工单类型', trigger: 'blur' }
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
        create_user: localStorage.getItem('username'),
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
      uploadurl: uploadurl,
      types: []
    }
  },

  computed: {
    ...mapGetters([
      'username'
    ])
  },
  created() {
    this.getTicketUsers()
    this.getTicketType()
  },
  methods: {
    postForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.ruleForm.ticketid = getTime()
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
              content: window.location.host + '/#/worktickets/editworkticket/' + this.ruleForm.ticketid
            }
            postSendmail(mailForm)
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

    getTicketType() {
      getTickettype().then(response => {
        this.types = response.data
      })
    },
    handleSuccess(file, fileList) {
      const formData = new FormData()
      formData.append('username', this.enclosureForm.create_user)
      formData.append('file', fileList.raw)
      formData.append('create_time', getTime(fileList.uid))
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
    imgAdd(pos, file) {
      var md = this.$refs.md
      const formData = new FormData()
      formData.append('username', this.enclosureForm.create_user)
      formData.append('file', file)
      formData.append('create_time', getTime(file.lastModified))
      formData.append('type', file.type)
      formData.append('archive', this.route_path[1])
      postUpload(formData).then(response => {
        md.$imglst2Url([[pos, response.data.file]])
      })
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

  .tips {
    color: rgba(128, 128, 128, 0.65);
  }
</style>
