<template>
  <div class="components-container" style='height:100vh'>
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
          <a class="ticketinfo action_user"><span class="han">
                              <a class="shu"></a>
                                指派人：</span>{{ticketData.action_user}}</a>
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
          <el-button v-if="!showinput" type="success" size="small" @click="showinput=true">编辑</el-button>
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
    <el-tooltip placement="top" content="一路向西">
      <back-to-top transitionName="fade" :customStyle="BackToTopStyle" :visibilityHeight="300"
                   :backPosition="50"></back-to-top>
    </el-tooltip>
  </div>
</template>
<script>
import { getProject, patchProject, getProjectEnclosure } from '@/api/opstask'
import { postUpload } from 'api/tool'
import VueMarkdown from 'vue-markdown' // 前端解析markdown
import BackToTop from '@/components/BackToTop'
import { getConversionTime } from '@/utils'
import { getUser } from 'api/user'
import { getCreatedate } from '@/utils'
import { apiUrl } from '@/config'

export default {
  components: {
    VueMarkdown, BackToTop
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
      showinput: false,
      commentquery: {
        project__id: ''
      },
      users: [],
      errortime: false,
      apiurl: apiUrl,
      enclosureData: []
    }
  },

  created() {
    this.bugquery.project__id = this.testquery.project__id = this.commentquery.project__id = this.commentForm.project = this.pid
    this.fetchData()
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
    getProjectUsers() {
      const query = {
        groups__name: 'ITDept'
      }
      getUser(query).then(response => {
        this.users = response.data
      })
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
