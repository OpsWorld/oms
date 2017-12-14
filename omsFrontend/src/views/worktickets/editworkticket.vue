<template xmlns="http://www.w3.org/1999/html">
  <div class="components-container" style='height:100vh'>
    <el-card>
      <div class="workticket">
        <el-card>
          <div slot="header" class="clearfix">
            <a class="title">{{ticketData.title}}</a>
            <div class="appendInfo">
              <a class="ticketinfo create_user"><span class="han">
                                工单创建时间：</span>{{ticketData.create_time | parseDate}}</a>
              <a class="ticketinfo create_user"><span class="han">
                                工单发起人：</span>{{ticketData.create_user}}</a>
              <a class="ticketinfo action_user"><span class="han">
                                当前处理人：</span>{{ticketData.action_user}}</a>
            </div>
            <div class="appendInfo">
              <span class="han">问题跟踪人：</span>
              <el-tag type="warning" style="margin-right: 5px" v-for="item in ticketData.follower"
                      :key="item.id">
                {{item}}
              </el-tag>
            </div>
          </div>
          <vue-markdown :source="ticketData.content"></vue-markdown>
        </el-card>
      </div>

      <div v-if="ticketData.ticket_status!=2">
        <el-form :model="commentForm"
                 :rules="rules" ref="ruleForm"
                 label-width="80px" class="demo-ruleForm">
          <hr class="heng"/>
          <el-form-item label="问题处理" prop="content">
            <mavon-editor style="z-index: 1" :default_open="ticketData.ticket_status==1?'edit':'preview'"
                          v-model="commentForm.content"
                          code_style="monokai" :toolbars="toolbars" @imgAdd="imgAdd"
                          ref="md"></mavon-editor>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm('ruleForm')" style="float: right">提交
            </el-button>
          </el-form-item>
          <hr class="heng"/>
        </el-form>
        <el-upload
          class="upload-demo"
          ref="upload"
          :action="uploadurl"
          :on-success="handleSuccess"
          :show-file-list="false"
          :disabled="count>2?true:false">
          <el-button slot="trigger" size="small" type="primary" icon="upload2" :disabled="count>2?true:false">
            上传文件
          </el-button>
          <div slot="tip" class="el-upload__tip">
            <p>上传文件不超过500kb，<a style="color: red">最多只能上传3个文件</a></p>
          </div>
        </el-upload>
        <hr class="heng"/>
      </div>
      <div v-if='enclosureData.length>0' class="ticketenclosure">
        <ul>
          <li v-for="item in enclosureData" :key="item.id" v-if="item.file">
            <a :href="apiurl + '/upload/' +item.file" download="item.id">{{item.file}}</a>
            <el-button type="text" size="small" @click="deleteEnclosure(item.id)">删除</el-button>
          </li>
        </ul>
      </div>
      <div class="ticketcomment" v-for="item in commentData" :key="item.id">
        处理过程：
        <hr class="heng"/>
        <el-row>
          <el-col :span="1">
            <el-button type="primary" plain class="commentuser">{{item.create_user}}</el-button>
          </el-col>
          <el-col :span="14">
            <div class="dialog-box">
              <span class="bot"></span>
              <span class="top"></span>
              <div class="comment">
                <vue-markdown :source="item.content"></vue-markdown>
                <p class="commenttime">处理时间：{{item.create_time | parseDate}}</p>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
      <div v-if="ticketData.ticket_status!=2">
        <hr class="heng"/>
        工单操作：
        <!--<el-button type="success" @click="changeTicketStatus(1)"-->
        <!--:disabled="ticketData.ticket_status==0?false:true">接收-->
        <!--</el-button>-->
        <el-button type="danger" @click="changeTicketStatus(2)"
                   :disabled="ticketData.ticket_status!=2?false:true">关闭
        </el-button>
        <el-button type="warning" plain @click="change_action=!change_action" v-if="ticketData.ticket_status!=2">更改指派者
        </el-button>
        <div v-if="change_action==true" style="display:inline;">
          <el-select v-model="rowdata.action_user" placeholder="请选择指派人">
            <el-option v-for="item in users" :key="item.id" :value="item.username"></el-option>
          </el-select>
          <el-button type="primary" plain @click="changeActionForm">提交</el-button>
        </div>
      </div>
    </el-card>
    <el-tooltip placement="top" content="一路向西">
      <back-to-top transitionName="fade" :customStyle="BackToTopStyle" :visibilityHeight="300"
                   :backPosition="50"></back-to-top>
    </el-tooltip>
  </div>
</template>
<script>
import {
  getWorkticket,
  patchWorkticket,
  getTicketcomment,
  postTicketcomment,
  postTicketenclosure,
  getTicketenclosure,
  deleteTicketenclosure
} from 'api/workticket'
import { postUpload, postSendmail } from 'api/tool'
import { apiUrl } from '@/config'
import VueMarkdown from 'vue-markdown' // 前端显示
import { getUser } from 'api/user'
import { uploadurl } from '@/config'
import BackToTop from '@/components/BackToTop'
import { mapGetters } from 'vuex'

export default {
  components: { VueMarkdown, BackToTop },

  data() {
    return {
      route_path: this.$route.path.split('/'),
      ticket_id: '',
      ticketData: {},
      ticket__title: '',
      commentData: {},
      enclosureData: {},
      apiurl: apiUrl,
      commentForm: {
        ticket: '',
        create_user: sessionStorage.getItem('username'),
        content: '',
        create_group: ''
      },
      enclosureForm: {
        ticket: '',
        create_user: sessionStorage.getItem('username'),
        file: '',
        create_group: ''
      },
      rules: {
        content: [
          { required: true, message: '赏几个字吧', trigger: 'blur' }
        ]
      },
      rowdata: {
        ticket_status: 1,
        action_user: ''
      },
      count: 0,
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
      users: [],
      change_action: false,
      to_list: '',
      BackToTopStyle: {
        right: '50px',
        bottom: '50px',
        width: '40px',
        height: '40px',
        'border-radius': '4px',
        'line-height': '45px', // 请保持与高度一致以垂直居中
        background: '#a2fdff'// 按钮的背景颜色
      },
      workticketlist_btn_edit: false,
      uploadurl: uploadurl
    }
  },

  computed: {
    ...mapGetters([
      'role',
      'elements'
    ])
  },

  created() {
    this.ticket_id = this.route_path[this.route_path.length - 1]
    this.workticketlist_btn_edit = this.elements['编辑工单-编辑工单按钮']
    this.fetchData()
    this.CommentData()
    this.EnclosureData()
    this.getTicketUsers()
  },
  methods: {
    fetchData() {
      getWorkticket(this.ticket_id).then(response => {
        this.ticketData = response.data
      })
    },
    CommentData() {
      const parms = {
        ticket__id: this.ticket_id
      }
      getTicketcomment(parms).then(response => {
        this.commentData = response.data
        this.rowdata.action_user = this.commentData.length === 0 ? null : this.commentData[this.commentData.length - 1].create_user
      })
      this.commentForm.content = ''
    },
    EnclosureData() {
      const parms = {
        ticket__id: this.ticket_id
      }
      getTicketenclosure(parms).then(response => {
        this.enclosureData = response.data
        this.count = response.data.length
      })
    },
    deleteEnclosure(id) {
      deleteTicketenclosure(id)
      setTimeout(this.EnclosureData, 1000)
    },
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.commentForm.ticket = this.ticket_id
          if (this.commentForm.create_user === this.ticketData.create_user) {
            this.rowdata.action_user = this.ticketData.action_user
          }
          postTicketcomment(this.commentForm)
          this.patchForm(this.rowdata)
        } else {
          console.log('error submit!!')
          return false
        }
        setTimeout(this.CommentData, 1000)
      })
    },
    patchForm(rowdata) {
      patchWorkticket(this.ticket_id, rowdata)
    },
    changeTicketStatus(status) {
      this.rowdata.ticket_status = this.ticketData.ticket_status = status
      patchWorkticket(this.ticket_id, this.rowdata)
    },
    changeActionForm() {
      patchWorkticket(this.ticket_id, this.rowdata)
      this.change_action = false
      this.ticketData.action_user = this.rowdata.action_user
      const mailForm = {
        to: this.ticketData.action_user,
        cc: this.ticketData.create_user,
        sub: '【' + this.ticketData.title + '】指派人被改变',
        content: '<html><a href="' + this.$route.fullPath + '">点我查看工单</a></html>'
      }
      postSendmail(mailForm)
    },
    handleSuccess(file, fileList) {
      const formData = new FormData()
      formData.append('username', this.enclosureForm.create_user)
      formData.append('file', fileList.raw)
      formData.append('create_time', this.afterFileUpload(fileList))
      formData.append('type', fileList.type)
      formData.append('archive', this.route_path[1])
      postUpload(formData).then(response => {
        this.enclosureForm.file = response.data.filepath
        this.enclosureForm.ticket = this.ticket_id
        postTicketenclosure(this.enclosureForm)
        setTimeout(this.EnclosureData, 1000)
        if (response.statusText === 'ok') {
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
      formData.append('username', this.username)
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
    },
    getTicketUsers() {
      getUser().then(response => {
        this.users = response.data
      })
    }
  }
}
</script>

<style lang='scss'>
  .editticket {
    margin: 50px;
    width: 80%;
  }

  .title {
    color: #f10df5;
    font-size: 30px;
    padding-left: 10px;
  }

  .appendInfo {
    padding: 5px;
  }

  .han {
    color: rgba(43, 200, 13, 0.6);
    font-size: 16px;
    margin-left: 5px;
  }

  .content {
    margin: 20px 5px;
  }

  .heng {
    margin: 20px 0;
    height: 1px;
    border: 0px;
    background-color: rgba(174, 127, 255, 0.38);
    color: #29e11c;
  }

  .ticketcomment {
    .commentuser {
    }
    .dialog-box {
      position: relative;
      left: 100px;
      margin-left: -20px;
      span {
        width: 0;
        height: 0;
        font-size: 0;
        overflow: hidden;
        position: absolute;
        &.bot {
          border-width: 16px;
          border-style: solid dashed dashed;
          border-color: transparent #4cff1e transparent transparent;
          top: 10px;
          left: -30px;
        }
        &.top {
          border-width: 18px;
          border-style: solid dashed dashed;
          border-color: transparent #fff transparent transparent;
          top: 10px;
          left: -30px;

        }
      }
      .comment {
        border: solid 1px rgba(255, 164, 186, 0.62);
        padding: 6px;
        margin-bottom: 10px;
        min-height: 50px;
        max-width: 600px;
        width: 50rem;
        .commenttime {
          float: right;
        }
      }
    }

  }
</style>
