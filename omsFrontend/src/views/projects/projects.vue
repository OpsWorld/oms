<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <div class="head-lavel">
        <div class="table-button">
          <router-link v-if="role==='super'||workticketlist_btn_add" :to="'addproject'">
            <el-button type="primary" icon="el-icon-plus">新建任务</el-button>
          </router-link>
          <el-button-group v-model="listQuery.status">
            <el-button plain size="mini" v-for="item in [0,1,2,3,4]" :key="item" :type="STATUS_TYPE[item]">
              {{STATUS_TEXT[item]}}
            </el-button>
          </el-button-group>
        </div>
        <div class="table-search">
          <el-input style="width: 160px;" class="filter-item" placeholder="编号" @keyup.enter.native="searchClick"
                    v-model="listQuery.pid"></el-input>
          <el-input style="width: 180px;" class="filter-item" placeholder="标题、内容或类型" @keyup.enter.native="searchClick"
                    v-model="listQuery.search"></el-input>
          <el-button class="filter-item" type="primary" icon="search" @click="searchClick">搜索</el-button>
        </div>
      </div>
      <div>
        <el-table :data="tableData" border style="width: 100%" @sort-change="handleSortChange">
          <el-table-column prop='pid' label='编号'>
            <template slot-scope="scope">
              <router-link :to="'viewproject/' + scope.row.id">
                <a style="color: #257cff">{{scope.row.pid}}</a>
              </router-link>
            </template>
          </el-table-column>
          <el-table-column prop='title' label='标题'></el-table-column>
          <el-table-column prop='type' label='类型'></el-table-column>
          <el-table-column prop='level' label='等级' sortable="custom">
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper" style="text-align: center; color: rgb(0,0,0)">
                <el-rate
                  v-model="scope.row.level"
                  :colors="['#99A9BF', '#F7BA2A', '#ff1425']"
                  disabled>
                </el-rate>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='status' label='状态' sortable="custom">
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper" style="text-align: center; color: rgb(0,0,0)">
                <el-tag :type="STATUS_TYPE[scope.row.status]">
                  {{STATUS_TEXT[scope.row.status]}}
                </el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='create_user' label='创建人'></el-table-column>
          <el-table-column prop='action_user' label='指派人'>
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper">
                <el-tag v-for="item in scope.row.action_user" :key="item">
                  {{item}}
                </el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='create_time' label='创建时间' sortable="custom">
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper" style="text-align: center; color: rgb(0,0,0)">
                <span>{{scope.row.create_time | parseDate}}</span>
              </div>
            </template>
          </el-table-column>
          <!--<el-table-column prop='update_time' label='更新时间' sortable="custom">-->
          <!--<template slot-scope="scope">-->
          <!--<div slot="reference" class="name-wrapper" style="text-align: center; color: rgb(0,0,0)">-->
          <!--<span>{{scope.row.update_time | parseDate}}</span>-->
          <!--</div>-->
          <!--</template>-->
          <!--</el-table-column>-->
          <!--<el-table-column prop='start_time' label='开始时间' sortable="custom">-->
          <!--<template slot-scope="scope">-->
          <!--<div slot="reference" class="name-wrapper" style="text-align: center; color: rgb(0,0,0)">-->
          <!--<span v-if="scope.row.start_time">{{scope.row.start_time | parseDate}}</span>-->
          <!--<span v-else>无</span>-->
          <!--</div>-->
          <!--</template>-->
          <!--</el-table-column>-->
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button type="success" size="small">修改</el-button>
              <el-button type="danger" size="small">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div class="table-footer">
        <div class="table-button">

        </div>
        <div class="table-pagination">
          <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page.sync="currentPage"
            :page-sizes="pagesize"
            :page-size="listQuery.limit"
            layout="total, sizes, prev, pager, next, jumper"
            :total="tabletotal">
          </el-pagination>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { getProject } from '@/api/project'
import { LIMIT, pagesize } from '@/config'
import { mapGetters } from 'vuex'

export default {
  components: {},
  data() {
    return {
      radio: '',
      tableData: [],
      tabletotal: 0,
      currentPage: 1,
      ticket_status: '',
      pagesize: pagesize,
      rowdata: {
        status: 0,
        action_user: localStorage.getItem('username')
      },
      STATUS_TEXT: { '0': '未指派', '1': '已指派', '2': '处理中', '3': '待审核', '4': '已完成' },
      STATUS_TYPE: { '0': 'danger', '1': 'primary', '2': 'success', '3': 'warning', '4': 'info' },
      listQuery: {
        limit: LIMIT,
        offset: '',
        pid: '',
        status: 1,
        create_user__username: '',
        action_user__username: '',
        search: '',
        ordering: ''
      },
      workticketlist_btn_add: false,
      workticketlist_btn_change_status: false,
      btnstatus: true,
      select_status: 1,
      show_status: false
    }
  },

  computed: {
    ...mapGetters([
      'role',
      'elements'
    ])
  },

  created() {
    this.fetchData()
    this.workticketlist_btn_add = this.elements['工单列表-新建工单按钮']
    this.workticketlist_btn_change_status = this.elements['工单列表-更改工单状态按钮']
  },

  methods: {
    fetchData() {
      getProject(this.listQuery).then(response => {
        this.tableData = response.data.results
        this.tabletotal = response.data.count
      })
    },
    searchClick() {
      this.fetchData()
    },
    handleSizeChange(val) {
      this.listQuery.limit = val
      this.fetchData()
    },
    handleCurrentChange(val) {
      this.listQuery.offset = (val - 1) * LIMIT
      this.fetchData()
    },
    changeStatus(val) {
      this.listQuery.ticket_status = val
      this.fetchData()
    },
    showMeCreate() {
      this.listQuery.create_user__username = localStorage.getItem('username')
      this.listQuery.action_user__username = ''
      this.fetchData()
    },
    showMeAction() {
      this.listQuery.action_user__username = localStorage.getItem('username')
      this.listQuery.create_user__username = ''
      this.fetchData()
    },
    showAllTicket() {
      this.listQuery.create_user__username = ''
      this.listQuery.action_user__username = ''
      this.listQuery.search = ''
      this.listQuery.ticket_status = ''
      this.fetchData()
    },
    handleSortChange(val) {
      if (val.order === 'ascending') {
        this.listQuery.ordering = val.prop
      } else if (val.order === 'descending') {
        this.listQuery.ordering = '-' + val.prop
      } else {
        this.listQuery.ordering = ''
      }
      this.fetchData()
    }
  }
}
</script>

<style lang='scss'>

</style>
