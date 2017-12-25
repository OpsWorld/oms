<template xmlns="http://www.w3.org/1999/html">
  <div class="components-container" style='height:100vh'>
    <el-card>
      <div class="workticket">
        <el-card>
          <div slot="header" class="clearfix">
            <a class="title">{{ticketData.title}}</a>
            <hr class="heng"/>

            <div class="appendInfo">
              <a class="ticketinfo create_user"><span class="han">
                                工单创建时间：</span>{{ticketData.create_time | parseDate}}</a>
              <a class="shu"></a>
              <a class="ticketinfo create_user"><span class="han">
                                工单发起人：</span>{{ticketData.create_user}}</a>
              <a class="shu"></a>
              <a class="ticketinfo action_user" v-if="ticketData.ticket_status!=0||ticketData.action_user">
                <span class="han">当前处理人：</span>{{ticketData.action_user}}</a>
              <a class="han" v-else><span class="han">当前处理人：</span> 未设置</a>
            </div>
            <div class="appendInfo">
              <span class="han">问题跟踪人：</span>
              <a style="margin-right: 5px" v-for="item in ticketData.follower" :key="item.id">
                {{item}}
              </a>
              <a class="han" v-if="showfollower">未设置</a>
              <a class="shu"></a>
              <span class="han">工单类型：</span>
              <a>{{ticketData.type}}</a>
              <a class="shu"></a>
              <span class="han">工单当前状态：</span>
              <el-tag>
                {{TICKET_STATUS[ticketData.ticket_status]}}
              </el-tag>
            </div>
            <div class="appendInfo" v-if="(workticketlist_btn_edit||role==='super')&&ticketData.ticket_status!=2">
              <span class="han">工单操作：</span>
              <el-button v-if="!showinput" type="success" size="small" @click="showinput=true">编辑</el-button>
              <el-button v-if="showinput" type="warning" size="small" @click="showinput=false">收起</el-button>
              <el-button type="primary" size="small" @click="showaction=true" v-if="showinput">选择指令</el-button>
            </div>
          </div>
          <vue-markdown :source="ticketData.content"></vue-markdown>
          <hr class="heng"/>

          <div v-if="showinput">
            <el-upload
              class="upload"
              ref="upload"
              :action="uploadurl"
              :on-success="handleSuccess"
              :show-file-list="false"
              :disabled="count>2?true:false">
              <el-button slot="trigger" size="mini" type="danger" plain icon="upload2" :disabled="count>2?true:false">
                上传附件
              </el-button>
              <div slot="tip" class="el-upload__tip">
                <p>上传文件不超过10m，<a style="color: red">最多只能上传3个文件</a></p>
              </div>
            </el-upload>
            <hr class="heng"/>
          </div>

          <div v-if='enclosureData.length>0' class="ticketenclosure">
            <ul>
              <li v-for="item in enclosureData" :key="item.id" v-if="item.file" style="list-style:none">
                <i class="fa fa-paperclip"></i>
                <a :href="apiurl + '/upload/' + item.file" :download="item.file">{{item.file.split('/')[1]}}</a>
                <el-button v-if="showinput" type="text" size="small" @click="deleteEnclosure(item.id)">删除</el-button>
              </li>
            </ul>
          </div>
        </el-card>
      </div>

      <div v-if="ticketData.ticket_status!=2&&showinput">
        <el-form :model="commentForm" ref="mailcontent" label-width="80px" class="demo-ruleForm">
          <hr class="heng"/>
          <el-form-item label="问题处理" prop="content">
            <mavon-editor style="z-index: 1" v-model="mailcontent" code_style="monokai" :toolbars="toolbars"
                          @imgAdd="imgAdd" ref="md"></mavon-editor>
          </el-form-item>

          <hr class="heng"/>
          <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
        </el-form>
      </div>

      <el-card class="ticketcomment" v-if="commentData.length>0">
        处理历史记录
        <div v-for="item in commentData" :key="item.id">
          <hr class="heng2"/>
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
      </el-card>
    </el-card>
    <el-tooltip placement="top" content="一路向西">
      <back-to-top transitionName="fade" :customStyle="BackToTopStyle" :visibilityHeight="300"
                   :backPosition="50"></back-to-top>
    </el-tooltip>

    <el-dialog
      title="指令"
      :visible.sync="showaction"
      width="30%">
      <div style="margin-left: 20px">
        <el-radio-group v-model="radio_status">
          <el-radio label="0">不操作</el-radio>
          <el-radio label="1">更改指派人</el-radio>
          <el-radio label="2">关闭工单</el-radio>
        </el-radio-group>
        <div v-if="radio_status==1">
          <el-select v-model="rowdata.action_user" placeholder="请选择指派人">
            <el-option v-for="item in users" :key="item.id" :value="item.username"></el-option>
          </el-select>
          <p style="color: red">点提交后生效</p>
        </div>
        <div v-if="radio_status==2">
          <p style="color: red">请在下方输入关闭原因并提交</p>
        </div>
      </div>
      <span slot="footer" class="dialog-footer">
    <el-button type="primary" @click="changeComment">确 定</el-button>
      </span>
    </el-dialog>
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
import { getCreatetime, getConversionTime } from '@/utils'

export default {
  components: {
    VueMarkdown, BackToTop
  },

  data() {
    return {
      route_path: this.$route.path.split('/'),
      ticketid: this.$route.params.ticketid,
      ticket_id: '',
      ticketData: {},
      commentData: {},
      enclosureData: {},
      apiurl: apiUrl,
      commentForm: {
        ticket: '',
        create_user: localStorage.getItem('username'),
        content: '【问题处理】',
        create_group: ''
      },
      enclosureForm: {
        ticket: '',
        create_user: localStorage.getItem('username'),
        file: '',
        create_group: ''
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
      users: [],
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
      uploadurl: uploadurl,
      TICKET_STATUS: {
        '0': '未接收',
        '1': '正在处理',
        '2': '已解决'
      },
      showfollower: true,
      showinput: false,
      showaction: false,
      radio_status: '0',
      mailmsg: '',
      mailcontent: ''
    }
  },

  computed: {
    ...mapGetters([
      'role',
      'elements'
    ])
  },

  created() {
    this.workticketlist_btn_edit = this.elements['编辑工单-编辑工单按钮']
    this.fetchData()
    this.CommentData()
    this.EnclosureData()
    this.getTicketUsers()
  },
  methods: {
    fetchData() {
      const parms = {
        ticketid: this.ticketid
      }
      getWorkticket(parms).then(response => {
        this.ticketData = response.data[0]
        this.ticket_id = this.ticketData.id
        if (this.ticketData.follower.length > 0) {
          this.showfollower = false
        }
      })
    },
    CommentData() {
      const parms = {
        ticket__ticketid: this.ticketid
      }
      getTicketcomment(parms).then(response => {
        this.commentData = response.data
        this.rowdata.action_user = this.commentData.length === 0 ? null : this.commentData[this.commentData.length - 1].create_user
      })
      this.commentForm.content = ''
    },
    EnclosureData() {
      const parms = {
        ticket__ticketid: this.ticketid
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
    changeComment() {
      this.showaction = false
    },
    submitForm(formName) {
      this.$confirm('你的操作即将提交，提交完成后会立即跳转到工单列表页面!', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(response => {
        this.commentForm.ticket = this.ticket_id
        if (this.radio_status === '1') {
          this.mailmsg = '【工单状态变化】工单被' + this.commentForm.create_user + '重新指派给' + this.rowdata.action_user
          this.commentForm.content = '【工单状态变化】工单被' + this.commentForm.create_user + '重新指派给' + this.rowdata.action_user + ',' + this.mailcontent
        } else if (this.radio_status === '2') {
          this.rowdata.action_user = this.commentForm.create_user
          this.rowdata.ticket_status = this.ticketData.ticket_status = this.radio_status
          this.mailmsg = '【工单状态变化】工单被' + this.commentForm.create_user + '关闭！'
          this.commentForm.content = '【工单状态变化】工单被' + this.commentForm.create_user + '关闭！' + this.mailcontent
        } else {
          this.rowdata.action_user = this.commentForm.create_user
          this.commentForm.content = '【问题处理】' + this.mailcontent
        }
        postTicketcomment(this.commentForm).then(response => {
          this.patchForm(this.rowdata)
          if (this.radio_status !== '0') {
            const create_time = getCreatetime()
            const mailForm = {
              to: this.ticketData.action_user,
              cc: this.ticketData.create_user + ',' + this.ticketData.follower.join(),
              sub: '【工单状态变化】' + this.ticketData.title,
              content: `
                    <html xmlns="http://www.w3.org/1999/xhtml">
                    <head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><title>工单通知邮件</title></head>
                    <body><div id="container">
                    <p>工单提交人： ${this.commentForm.create_user} </p>
                    <p>工单提交时间：${create_time} </p>
                    <p>点击工单地址: <a href='http://${window.location.href}'>http://${window.location.href}</a></p>
                    <p>工单详细内容：</p>
                    <p>${this.mailmsg}</p>
                    <p>【工单处理内容】${this.mailcontent}</p>
                    </div></body></html>`
            }
            postSendmail(mailForm)
          }
          this.$router.push('/worktickets/workticket')
        })
      }).catch(() => {
        this.$message({
          type: 'error',
          message: '已取消本次操作'
        })
      })
    },
    patchForm(rowdata) {
      patchWorkticket(this.ticket_id, rowdata)
    },
    handleSuccess(file, fileList) {
      const formData = new FormData()
      formData.append('username', this.enclosureForm.create_user)
      formData.append('file', fileList.raw)
      formData.append('create_time', getConversionTime(fileList.uid))
      formData.append('type', fileList.raw.type)
      formData.append('archive', this.route_path[1])
      postUpload(formData).then(response => {
        this.enclosureForm.file = response.data.filepath
        this.enclosureForm.ticket = this.ticket_id
        postTicketenclosure(this.enclosureForm)
        setTimeout(this.EnclosureData, 1000)
        if (response.statusText === 'Created') {
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
      formData.append('username', this.username)
      formData.append('file', file)
      formData.append('create_time', getConversionTime(file.lastModified))
      formData.append('type', file.type)
      formData.append('archive', this.route_path[1])
      postUpload(formData).then(response => {
        md.$imglst2Url([[pos, response.data.file]])
      })
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
    font-size: 28px;
    font-weight: 700;
    padding-left: 10px;
  }

  .appendInfo {
    padding: 5px;
    margin: 5px;
  }

  .han {
    margin-left: 5px;
  }

  .shu {
    margin: 0 5px;
    height: 100px;
    width: 1px;
    border-left: 1px rgba(52, 52, 52, 0.38) solid
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
    margin-top: 20px;
    background-color: rgba(48, 250, 81, 0.17);
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
          border-color: transparent rgba(48, 250, 81, 0.38) transparent transparent;
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
