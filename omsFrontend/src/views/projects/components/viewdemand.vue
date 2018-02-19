<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <el-row :gutter="20">
        <el-col :span="24">
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
                <a class="shu"></a>
                <span class="han">计划结束时间：</span>
                <a v-if="ticketData.end_time" class="ticketinfo">{{ticketData.end_time}}</a>
                <a v-else class="ticketinfo">未设置</a>
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
        </el-col>
      </el-row>
    </el-card>
    <el-tooltip placement="top" content="一路向西">
      <back-to-top transitionName="fade" :customStyle="BackToTopStyle" :visibilityHeight="300"
                   :backPosition="50"></back-to-top>
    </el-tooltip>
  </div>
</template>
<script>
import { getDemandManager, getDemandEnclosure } from '@/api/project'
import VueMarkdown from 'vue-markdown' // 前端解析markdown
import BackToTop from '@/components/BackToTop'
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
        0: '未审核',
        1: '已通过',
        2: '未通过'
      },
      users: [],
      errortime: false,
      apiurl: apiUrl,
      enclosureData: []
    }
  },

  created() {
    this.fetchData()
    this.fetchEnclosureData()
  },
  methods: {
    fetchData() {
      const query = null
      getDemandManager(query, this.pid).then(response => {
        this.ticketData = response.data[0]
      })
    },
    fetchEnclosureData() {
      const parms = {
        project__id: this.pid
      }
      getDemandEnclosure(parms).then(response => {
        console.log(response)
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
</style>
