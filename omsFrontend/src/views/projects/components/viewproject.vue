<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <el-row :gutter="10">
        <el-col :span="17">

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
                <el-tag>
                  {{Project_Status[ticketData.status]}}
                </el-tag>
              </div>
              <div class="appendInfo">
                <span class="han">任务开始时间：</span>
                <a v-if="ticketData.start_time" class="ticketinfo">{{ticketData.start_time}}</a>
                <a v-else class="ticketinfo">未设置</a>
                <a class="shu"></a>
                <span class="han">计划结束时间：</span>
                <a v-if="ticketData.end_time" class="ticketinfo">{{ticketData.end_time}}</a>
                <a v-else class="ticketinfo">未设置</a>
              </div>
              <div class="appendInfo" v-if="ticketData.status!=7">
                <span class="han">操作：</span>
                <el-button v-if="!showinput" type="success" size="small" @click="showinput=true">更改状态</el-button>
                <el-button v-if="showinput" type="warning" size="small" @click="showinput=false">收起</el-button>
                <el-button v-if="showinput" type="primary" size="small" @click="patchForm" :disabled="errortime">确定
                </el-button>
                <div v-if="showinput" class="action">
                  <el-select v-model="rowdata.status" filterable placeholder="更新任务状态" @change="changeProjectstatus">
                    <el-option v-for="(item, index) in Project_Status" :key="index" :label="item" :value="index">
                    </el-option>
                  </el-select>
                  <el-date-picker
                    v-if="rowdata.status === '2' && !ticketData.end_time"
                    v-model="rowdata.end_time"
                    type="date"
                    value-format="yyyy-MM-dd"
                    placeholder="设置计划结束时间"
                    @change="changeProjectendtime"
                    disable="have_endtime">
                  </el-date-picker>
                </div>

              </div>
            </div>
            <vue-markdown :source="ticketData.content"></vue-markdown>
            <hr class="heng"/>
            <div v-if='enclosureData.length>0'>
              <ul>
                <li v-for="item in enclosureData" :key="item.id" v-if="item.file" style="list-style:none">
                  <i class="fa fa-paperclip"></i>
                  <a :href="apiurl + '/upload/' + item.file" :download="item.file">{{item.file.split('/')[1]}}</a>
                </li>
              </ul>
            </div>
          </el-card>

          <div v-if="ticketData.status!=4">
            <el-form :model="commentForm" ref="content" label-width="90px" class="demo-ruleForm">
              <hr class="heng"/>
              <el-form-item label="问题处理" prop="content">
                <mavon-editor style="z-index: 1" v-model="commentForm.content" code_style="monokai" :toolbars="toolbars"
                              @imgAdd="imgAdd" ref="md"></mavon-editor>
                <a class="tips"> Tip：截图可以直接 Ctrl + v 粘贴到问题处理里面</a>
              </el-form-item>
              <el-form-item label="通知个人" prop="action_user">
                <el-select v-model="ticketData.follow_user" filterable multiple placeholder="请选择通知人">
                  <el-option v-for="item in users" :key="item.id" :value="item.username"></el-option>
                </el-select>
                <el-checkbox v-model="sendpeople">发送通知</el-checkbox>
              </el-form-item>
              <el-form-item label="通知技术部" prop="action_user">
                <el-checkbox v-model="sendgroup">发送通知</el-checkbox>
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
                <el-col :span="20">
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
        <el-col :span="7">

          <el-card>
            <div slot="header" class="clearfix">
              <a class="right-title">测试用例</a>
              <el-button class="card-head-btn" type="text" icon="el-icon-plus" @click="addTestFrom=true"></el-button>
            </div>
            <el-table :data="testData" stripe @row-click="clicktestTable" style="width: 100%">
              <el-table-column prop="id" label="Id" width="60">
                <template slot-scope="scope">
                  <div slot="reference">
                    <el-button type="text" @click="showTest(false, scope.row)"><i
                      class="fa fa-hashtag"></i>{{scope.row.id}}
                    </el-button>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="name" label="名称">
                <template slot-scope="scope">
                  <div slot="reference">
                    <el-button type="text" @click="showTest(true, scope.row)">{{scope.row.name}}</el-button>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="status" label="状态" width="70">
                <template slot-scope="scope">
                  <div slot="reference">
                    <el-tag size="mini">{{Test_Status[scope.row.status]}}</el-tag>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="action_user" label="开发" width="80"></el-table-column>
            </el-table>
          </el-card>

          <el-card>
            <div slot="header" class="clearfix">
              <a class="right-title">关联bug</a>
              <el-button size="mini" type="primary" plain @click="showAllBug">all</el-button>
              <el-button class="card-head-btn" type="text" icon="el-icon-plus" @click="addBugFrom=true"></el-button>
            </div>
            <el-table :data="bugData" stripe style="width: 100%">
              <el-table-column prop="id" label="Id" width="60">
                <template slot-scope="scope">
                  <div slot="reference">
                    <el-button type="text" @click="showBug(false, scope.row)"><i
                      class="fa fa-hashtag"></i>{{scope.row.id}}
                    </el-button>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="name" label="名称">
                <template slot-scope="scope">
                  <div slot="reference">
                    <el-button type="text" @click="showBug(true, scope.row)">{{scope.row.name}}</el-button>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="status" label="状态" width="70">
                <template slot-scope="scope">
                  <div slot="reference">
                    <el-tag size="mini">{{Bug_Status[scope.row.status]}}</el-tag>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="action_user" label="开发" width="80"></el-table-column>
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
      <add-bug :project="ticketData.pid" @DialogStatus="getDialogStatus"></add-bug>
    </el-dialog>
    <el-dialog :visible.sync="addTestFrom">
      <add-test :project="ticketData.pid" @DialogStatus="getDialogStatus"></add-test>
    </el-dialog>

    <el-dialog :visible.sync="editBugForm" @close="fetchBugData">
      <edit-bug :ruleForm="selectBug" @DialogStatus="getDialogStatus"></edit-bug>
    </el-dialog>
    <el-dialog :visible.sync="editTestForm" @close="fetchTestData">
      <edit-test :ruleForm="selectTest" @DialogStatus="getDialogStatus"></edit-test>
    </el-dialog>

    <el-dialog :visible.sync="showBugForm" @close="fetchBugData">
      <show-bug :ruleForm="selectBug"></show-bug>
    </el-dialog>
    <el-dialog :visible.sync="showTestForm" @close="fetchTestData">
      <show-test :ruleForm="selectTest"></show-test>
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
  getTestManager,
  getProjectEnclosure
} from '@/api/project'
import { postUpload, postSendmessage } from 'api/tool'
import VueMarkdown from 'vue-markdown' // 前端解析markdown
import BackToTop from '@/components/BackToTop'
import { getConversionTime } from '@/utils'
import addBug from './addbug.vue'
import addTest from './addtest.vue'
import editBug from './editbug.vue'
import editTest from './edittest.vue'
import showBug from './showbug.vue'
import showTest from './showtest.vue'
import { getUser } from 'api/user'
import { getCreatedate } from '@/utils'
import { apiUrl } from '@/config'

export default {
  components: {
    VueMarkdown, BackToTop, addBug, addTest, showBug, showTest, editTest, editBug
  },

  data() {
    return {
      route_path: this.$route.path.split('/'),
      pid: this.$route.params.id,
      ticketData: {},
      commentData: {},
      commentForm: {
        project: '',
        create_user: localStorage.getItem('username'),
        content: ''
      },
      rowdata: {
        status: '',
        start_time: '',
        end_time: ''
      },
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
      BackToTopStyle: {
        right: '50px',
        bottom: '50px',
        width: '40px',
        height: '40px',
        'border-radius': '50px',
        'line-height': '45px', // 请保持与高度一致以垂直居中
        background: '#a2fdff'// 按钮的背景颜色
      },
      Project_Status: {
        0: '未指派',
        1: '已指派',
        2: '处理中',
        3: '待测试',
        4: '测试中',
        5: '已测试',
        6: '待上线',
        7: '已上线'
      },
      Bug_Status: {
        0: '新建',
        1: '打开',
        2: '关闭',
        3: '已修复',
        4: '暂不处理',
        5: '重新打开'
      },
      Test_Status: {
        0: 'Passed',
        1: 'Failed',
        2: 'Block',
        3: 'N/A'
      },
      showinput: false,
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
      showTestForm: false,
      editBugForm: false,
      editTestForm: false,
      sendpeople: false,
      sendgroup: false,
      users: [],
      selectBug: {},
      selectTest: {},
      errortime: false,
      apiurl: apiUrl,
      enclosureData: []
    }
  },

  created() {
    this.bugquery.project__id = this.testquery.project__id = this.commentquery.project__id = this.commentForm.project = this.pid
    this.fetchData()
    this.fetchBugData()
    this.fetchTestData()
    this.CommentData()
    this.getProjectUsers()
    this.fetchEnclosureData()
  },
  methods: {
    fetchData() {
      const query = null
      getProject(query, this.pid).then(response => {
        this.ticketData = response.data
        this.rowdata.start_time = response.data.start_time
        this.rowdata.end_time = response.data.end_time
      })
    },
    getDialogStatus(data) {
      this.addBugFrom = data
      this.addTestFrom = data
      this.editBugForm = data
      this.editTestForm = data
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
      postProjectComment(this.commentForm).then(response => {
        this.CommentData()
        if (this.sendpeople) {
          const messageForm = {
            action_user: this.ticketData.create_user + ',' + this.ticketData.follow_user.join(),
            title: '【任务有新回复】' + this.ticketData.title,
            message: `操作人: ${this.commentForm.create_user}\n内容: ${this.commentForm.content}\n地址: ${window.location.href}`
          }
          postSendmessage(messageForm)
        }
        if (this.sendgroup) {
          const messageForm = {
            action_user: 'ITDept_SkypeID',
            title: '【任务有新回复】' + this.ticketData.title,
            message: `操作人: ${this.commentForm.create_user}\n内容: ${this.commentForm.content}\n地址: ${window.location.href}`
          }
          postSendmessage(messageForm)
        }
      }).catch(() => {
        this.$message({
          type: 'error',
          message: '提交有误'
        })
      })
    },
    patchForm() {
      if (!this.rowdata.status) {
        this.rowdata.status = this.ticketData.status
      }
      patchProject(this.pid, this.rowdata).then(() => {
        this.$message({
          message: '恭喜你，编辑成功',
          type: 'success'
        })
        this.fetchData()
        this.showinput = false
      }).catch(error => {
        this.$message.error('计划结束时间必须大于开始时间！')
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
    showBug(show, row) {
      if (show) {
        this.showBugForm = true
      } else {
        this.editBugForm = true
      }
      this.selectBug = row
    },
    showTest(show, row) {
      if (show) {
        this.showTestForm = true
      } else {
        this.editTestForm = true
      }
      this.selectTest = row
    },
    clicktestTable(row) {
      this.bugquery.test_id = row.id
      this.fetchBugData()
    },
    getProjectUsers() {
      const query = {
        groups__name: 'ITDept'
      }
      getUser(query).then(response => {
        this.users = response.data
      })
    },
    showAllBug() {
      this.bugquery.test_id = ''
      this.fetchBugData()
    },
    changeProjectstatus() {
      if (this.rowdata.status === '2') {
        this.rowdata.start_time = getCreatedate()
      }
    },
    changeProjectendtime() {
      const d1 = new Date(this.rowdata.start_time)
      const d2 = new Date(this.rowdata.end_time)
      // 获取他们的距离1970年以来的毫秒
      const time1 = d1.getTime()
      const time2 = d2.getTime()
      if (time2 < time1) {
        this.$message.error('计划结束时间必须大于开始时间！')
        this.errortime = true
      } else {
        this.errortime = false
      }
    },
    fetchEnclosureData() {
      const parms = {
        project__id: this.pid
      }
      getProjectEnclosure(parms).then(response => {
        this.enclosureData = response.data
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
    margin: 5px;
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
      margin-left: -30px;
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
        .commenttime {
          float: right;
        }
      }
    }
  }
</style>
