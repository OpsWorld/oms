<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <el-row :gutter="20">
        <el-col :span="18">

          <el-card>
            <div slot="header" class="clearfix">
              <a class="title">{{ticketData.name}}</a>
              <hr class="heng"/>

              <div class="appendInfo">
                <a class="ticketinfo create_user"><span class="han">
                                创建时间：</span>{{ticketData.create_time | parseDate}}</a>
                <a class="ticketinfo create_user"><span class="han">
                              <a class="shu"></a>
                                发起人：</span>{{ticketData.create_user}}</a>
                <a class="ticketinfo action_user">
                  <span class="han"><a class="shu"></a>指派人：</span>
                  <el-tag size="mini" v-for="item in ticketData.action_user" :key="item.id" style="margin-right: 3px">{{item}}
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
                  </el-radio-group>
                  <a class="tips" style="display: block;margin: 5px 160px -20px"> Tip：请在下方回复内容并提交</a>
                </div>

              </div>
            </div>
            <vue-markdown :source="ticketData.content"></vue-markdown>
          </el-card>

          <div v-if="ticketData.ticket_status!=2&&showinput">
            <el-form :model="commentForm" ref="content" label-width="80px" class="demo-ruleForm">
              <hr class="heng"/>
              <el-form-item label="问题处理" prop="content">
                <mavon-editor style="z-index: 1" v-model="commentForm.content" code_style="monokai" :toolbars="toolbars"
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

        </el-col>
        <el-col :span="6">

          <el-card>
            <div slot="header" class="clearfix">
              <a class="right-title">测试用例</a>
              <el-button class="card-head-btn" type="text" icon="el-icon-plus" @click="addTestFrom=true"></el-button>
            </div>
            <el-table :data="testData" stripe @row-click="clicktestTable" style="width: 100%">
              <el-table-column prop="id" label="Id" width="60">
                <template slot-scope="scope">
                  <div slot="reference">
                    <i class="fa fa-hashtag"></i>{{scope.row.id}}
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="name" label="名称">
                <template slot-scope="scope">
                  <div slot="reference">
                    <el-button type="text" @click="showTest(scope.row)">{{scope.row.name}}</el-button>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="action_user" label="开发" width="100"></el-table-column>
            </el-table>
          </el-card>

          <el-card>
            <div slot="header" class="clearfix">
              <a class="right-title">关联bug</a>
              <el-button class="card-head-btn" type="text" icon="el-icon-plus" @click="addBugFrom=true"></el-button>
            </div>
            <el-table :data="bugData" stripe style="width: 100%">
              <el-table-column prop="id" label="Id" width="60">
                <template slot-scope="scope">
                  <div slot="reference">
                    <i class="fa fa-hashtag"></i>{{scope.row.id}}
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="name" label="名称">
                <template slot-scope="scope">
                  <div slot="reference">
                    <el-button type="text" @click="showBug(scope.row)">{{scope.row.name}}</el-button>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="action_user" label="开发" width="100"></el-table-column>
            </el-table>
          </el-card>

        </el-col>
      </el-row>
    </el-card>
    <el-tooltip placement="top" content="一路向西">
      <back-to-top transitionName="fade" :customStyle="BackToTopStyle" :visibilityHeight="300"
                   :backPosition="50"></back-to-top>
    </el-tooltip>

    <el-dialog :visible.sync="addBugFrom">
      <add-bug :pid="ticketData.pid" @DialogStatus="getDialogStatus"></add-bug>
    </el-dialog>

    <el-dialog :visible.sync="addTestFrom">
      <add-test :pid="ticketData.pid" @DialogStatus="getDialogStatus"></add-test>
    </el-dialog>

    <el-dialog :visible.sync="showBugForm">
      <div>bug详情</div>
    </el-dialog>

    <el-dialog :visible.sync="showTestForm">
      <div>test详情</div>
    </el-dialog>
  </div>
</template>
<script>
import {
  getProject,
  patchProject,
  getProjectComment,
  postProjectComment,
  getBugManager,
  getTestManager
} from '@/api/project'
import { postUpload } from 'api/tool'
import { apiUrl, uploadurl } from '@/config'
import VueMarkdown from 'vue-markdown' // 前端解析markdown
import { getUser } from 'api/user'
import BackToTop from '@/components/BackToTop'
import { mapGetters } from 'vuex'
import { getConversionTime } from '@/utils'
import addBug from './addbug.vue'
import addTest from './addtest.vue'

export default {
  components: {
    VueMarkdown, BackToTop, addBug, addTest
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
        project: '',
        create_user: localStorage.getItem('username'),
        content: ''
      },
      enclosureForm: {
        ticket: '',
        create_user: localStorage.getItem('username'),
        file: ''
      },
      rowdata: {
        status: 1,
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
      STATUS_TEXT: { '0': '未指派', '1': '已指派', '2': '处理中', '3': '待审核', '4': '已完成' },
      STATUS_TYPE: { '0': 'danger', '1': 'primary', '2': 'success', '3': 'warning', '4': 'info' },
      showinput: false,
      radio_status: '0',
      addBugFrom: false,
      addTestFrom: false,
      bugData: [],
      testData: [],
      bugquery: {
        project__id: '',
        test_id: '',
        id: ''
      },
      testquery: {
        project__id: '',
        id: ''
      },
      commentquery: {
        project__id: ''
      },
      showBugForm: false,
      showTestForm: false
    }
  },

  computed: {
    ...mapGetters([
      'role',
      'elements'
    ])
  },

  created() {
    this.bugquery.project__id = this.testquery.project__id = this.commentquery.project__id = this.commentForm.project = this.pid
    this.workticketlist_btn_edit = this.elements['编辑工单-编辑工单按钮']
    this.fetchData()
    this.fetchBugData()
    this.fetchTestData()
    this.CommentData()
    this.getTicketUsers()
  },
  methods: {
    fetchData() {
      const query = null
      getProject(query, this.pid).then(response => {
        this.ticketData = response.data
      })
    },
    getDialogStatus(data) {
      this.addBugFrom = data
      this.addTestFrom = data
      this.fetchBugData()
      this.fetchTestData()
    },
    CommentData() {
      getProjectComment(this.commentquery).then(response => {
        this.commentData = response.data
      })
      this.commentForm.content = ''
    },
    fetchBugData() {
      getBugManager(this.bugquery).then(response => {
        this.bugData = response.data
      })
    },
    fetchTestData() {
      getTestManager(this.testquery).then(response => {
        this.testData = response.data
      })
    },
    submitForm(formName) {
      console.log(this.commentForm)
      postProjectComment(this.commentForm).then(response => {
        this.CommentData()
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
    },
    showBug(row) {
      this.showBugForm = true
    },
    showTest(row) {
      this.showTestForm = true
    },
    clicktestTable(row) {
      this.bugquery.test_id = row.id
      this.fetchBugData()
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

  .right-title {
    font-size: 20px;
    font-weight: 600;
    padding-left: 10px;
  }

  .card-head-btn {
    float: right;
    padding: 3px 0;
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
