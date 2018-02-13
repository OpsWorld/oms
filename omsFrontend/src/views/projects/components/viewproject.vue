<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <div class="workticket">
        <el-card>
          <div slot="header" class="clearfix">
            <a class="title">{{ticketData.title}}</a>
            <hr class="heng"/>

            <div class="appendInfo">
              <a class="ticketinfo create_user"><span class="han">
                                创建时间：</span>{{ticketData.create_time | parseDate}}</a>
              <a class="ticketinfo create_user"><span class="han">
                              <a class="shu"></a>
                                发起人：</span>{{ticketData.create_user}}</a>
              <a class="ticketinfo action_user">
                <span class="han"><a class="shu"></a>指派人：</span>
                <el-tag v-for="item in ticketData.action_user" :key="item.id" style="margin-right: 3px">{{item}}
                </el-tag>
              </a>
              <a class="shu"></a>
              <span class="han">类型：</span>
              <a>{{ticketData.type}}</a>
              <a class="shu"></a>
              <span class="han">当前状态：</span>
              <el-tag :type="STATUS_TYPE[ticketData.status]">
                {{STATUS_TEXT[ticketData.status]}}
              </el-tag>
            </div>
            <div class="appendInfo" v-if="(workticketlist_btn_edit||role==='super')&&ticketData.ticket_status!=2">
              <span class="han">操作：</span>
              <el-button v-if="!showinput" type="success" size="small" @click="showinput=true">编辑</el-button>
              <el-button v-if="showinput" type="warning" size="small" @click="showinput=false">收起</el-button>
              <div v-if="showinput" class="action">
                <el-radio-group v-model="radio_status">
                  <el-radio label="0">不操作</el-radio>
                  <el-radio label="2">关闭任务</el-radio>
                  <el-radio label="1">更改指派人</el-radio>
                </el-radio-group>
                <div class="action" v-if="radio_status==1">
                  <el-select v-model="rowdata.action_user" filterable placeholder="请选择指派人">
                    <el-option v-for="item in users" :key="item.id" :value="item.username"></el-option>
                  </el-select>
                </div>
                <a class="tips" style="display: block;margin: 5px 160px -20px"> Tip：请在下方回复内容并提交</a>
              </div>

            </div>
          </div>
          <vue-markdown :source="ticketData.content"></vue-markdown>
        </el-card>
      </div>

      <div v-if="ticketData.ticket_status!=2&&showinput">
        <el-form :model="commentForm" ref="mailcontent" label-width="80px" class="demo-ruleForm">
          <hr class="heng"/>
          <el-form-item label="问题处理" prop="content">
            <mavon-editor style="z-index: 1" v-model="mailcontent" code_style="monokai" :toolbars="toolbars"
                          @imgAdd="imgAdd" ref="md"></mavon-editor>
            <a class="tips"> Tip：截图可以直接 Ctrl + v 粘贴到问题处理里面</a>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
          </el-form-item>
        </el-form>
      </div>

      <el-card class="ticketcomment" v-if="commentData.length>0">
        处理历史记录
        <div v-for="item in commentData" :key="item.id">
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
      </el-card>
    </el-card>
    <el-tooltip placement="top" content="一路向西">
      <back-to-top transitionName="fade" :customStyle="BackToTopStyle" :visibilityHeight="300"
                   :backPosition="50"></back-to-top>
    </el-tooltip>
  </div>
</template>
<script>
import { getProject, patchProject, getProjectComment, postProjectComment } from '@/api/project'
import { postUpload } from 'api/tool'
import { apiUrl, uploadurl } from '@/config'
import VueMarkdown from 'vue-markdown' // 前端解析markdown
import { getUser } from 'api/user'
import BackToTop from '@/components/BackToTop'
import { mapGetters } from 'vuex'
import { getConversionTime } from '@/utils'

export default {
  components: {
    VueMarkdown, BackToTop
  },

  data() {
    return {
      route_path: this.$route.path.split('/'),
      pid: this.$route.params.id,
      ticket_id: '',
      ticketData: {},
      commentData: {},
      enclosureData: {},
      apiurl: apiUrl,
      commentForm: {
        ticket: '',
        create_user: localStorage.getItem('username'),
        content: '【问题处理】'
      },
      enclosureForm: {
        ticket: '',
        create_user: localStorage.getItem('username'),
        file: ''
      },
      rowdata: {
        ticket_status: 1,
        action_user: '',
        edit_user: ''
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
      STATUS_TEXT: { '0': '未指派', '1': '已指派', '2': '处理中', '3': '待审核', '4': '已完成' },
      STATUS_TYPE: { '0': 'danger', '1': 'primary', '2': 'success', '3': 'warning', '4': 'info' },
      showinput: false,
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
    this.getTicketUsers()
  },
  methods: {
    fetchData() {
      const query = null
      getProject(query, this.pid).then(response => {
        this.ticketData = response.data
        this.rowdata.action_user = this.ticketData.action_user
      })
    },
    CommentData() {
      const parms = {
        ticket__ticketid: this.pid
      }
      getProjectComment(parms).then(response => {
        this.commentData = response.data
      })
      this.commentForm.content = ''
    },
    submitForm(formName) {
      postProjectComment(this.commentForm).then(response => {
        this.patchForm(this.rowdata)
      }).catch(() => {
        this.$message({
          type: 'error',
          message: '提交有误'
        })
      })
    },
    patchForm(rowdata) {
      patchProject(this.pid, rowdata)
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

  .action {
    display: inline;
    margin-left: 20px;
  }

  .han {
    margin-left: 5px;
  }

  .content {
    margin: 20px 5px;
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
