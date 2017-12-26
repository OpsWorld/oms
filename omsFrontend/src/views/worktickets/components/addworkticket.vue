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
          <a class="tips"> Tip：截图可以直接 Ctrl + v 粘贴到工单内容里面</a>
        </el-form-item>
        <el-form-item label="工单等级" prop="level">
          <el-rate
            v-model="ruleForm.level"
            :colors="['#99A9BF', '#F7BA2A', '#ff1425']"
            show-text
            :texts="['E', 'D', 'C', 'B', 'A']">
          </el-rate>
          <a class="tips">Tip：星数代表问题紧急程度，星数越多，代表越紧急</a>
        </el-form-item>
        <el-form-item>
          <hr class="heng"/>
          <el-upload
            class="upload-demo"
            ref="upload"
            :action="uploadurl"
            :on-success="handleSuccess"
            :on-remove="handleRemove"
            :file-list="fileList">
            <el-button slot="trigger" size="small" type="primary" :disabled="count>2?true:false">
              上传文件
            </el-button>
            (可以不用上传)
            <div slot="tip" class="el-upload__tip">
              <p>上传文件不超过10m，<a style="color: red">最多只能上传3个文件</a></p>
            </div>
          </el-upload>
          <hr class="heng"/>
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
import { postUpload, postSendmail, postSendmessage } from 'api/tool'
import { getUser } from 'api/user'
import { uploadurl } from '@/config'
import { mapGetters } from 'vuex'
import { getCreatetime, getConversionTime } from '@/utils'

export default {
  components: {},

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
      enclosureFile: [],
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
          this.ruleForm.ticketid = getConversionTime()
          postWorkticket(this.ruleForm).then(response => {
            if (response.statusText === '"Created"') {
              this.$message({
                type: 'success',
                message: '恭喜你，新建成功'
              })
            }
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
                postTicketenclosure(this.enclosureForm)
              })
            }
            const create_time = getCreatetime()
            const mailForm = {
              to: this.ruleForm.action_user,
              cc: this.ruleForm.follower.join(),
              sub: '【新工单】' + this.ruleForm.title,
              content: `
                    <html xmlns="http://www.w3.org/1999/xhtml">
                    <head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><title>工单通知邮件</title></head>
                    <body><div id="container">
                    <p>工单提交人： ${this.ruleForm.create_user}</p>
                    <p>工单提交时间：${create_time} </p>
                    <p>点击工单地址: <a href='http://${window.location.host}/#/worktickets/editworkticket/${this.ruleForm.ticketid}'>
                    http://${window.location.host}/#/worktickets/editworkticket/${this.ruleForm.ticketid}</a></p>
                    <p>工单详细内容：</p>
                    <p>${this.ruleForm.content}</p>
                    </div></body></html>`
            }
            postSendmail(mailForm)
            const messageForm = {
              user: this.ruleForm.action_user,
              title: '您有新的工单',
              message: `工单地址: http://${window.location.host}/#/worktickets/editworkticket/${this.ruleForm.ticketid}`
            }
            postSendmessage(messageForm)
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
      this.fileList.push(fileList.raw)
      this.count += 1
    },
    handleRemove(file, fileList) {
      this.fileList.remove(file)
      this.count -= 1
    },
    imgAdd(pos, file) {
      var md = this.$refs.md
      const formData = new FormData()
      formData.append('username', this.enclosureForm.create_user)
      formData.append('file', file)
      formData.append('create_time', getConversionTime(file.lastModified))
      formData.append('type', file.type)
      formData.append('archive', this.route_path[1])
      postUpload(formData).then(response => {
        md.$imglst2Url([[pos, response.data.file]])
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

  .addticket {
    margin: 50px;
    width: 80%;
  }

  .tips {
    color: rgba(128, 128, 128, 0.82);
  }
</style>
