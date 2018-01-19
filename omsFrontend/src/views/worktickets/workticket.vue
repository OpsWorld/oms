<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <div class="head-lavel">
        <div class="table-button">
          <router-link v-if="role==='super'||workticketlist_btn_add" :to="'addworkticket'">
            <el-button type="primary" icon="el-icon-plus">新建工单</el-button>
          </router-link>
          <el-button type="danger" :disabled="btnstatus"
                     v-if="workticketlist_btn_change_status||role==='super'"
                     @click="show_status=true">更改状态
          </el-button>
          <el-button-group>
            <el-button type="danger" plain size="small" @click="showAllTicket">全部</el-button>
            <el-button type="success" plain size="small" @click="showMeCreate">我创建的工单</el-button>
            <el-button type="warning" plain size="small" @click="showMeAction">我处理的工单</el-button>
          </el-button-group>

          <el-radio-group v-model="radio" @change="changeStatus" style="margin-left: 20px">
            <el-radio label="0">未接收</el-radio>
            <el-radio label="1">正在处理</el-radio>
            <el-radio label="2">已解决</el-radio>
          </el-radio-group>

        </div>
        <div class="table-search">
          <el-input style="width: 110px;" class="filter-item" placeholder="工单发起人" @keyup.enter.native="searchClick"
                    v-model="listQuery.create_user"></el-input>
          <el-input style="width: 160px;" class="filter-item" placeholder="工单编号" @keyup.enter.native="searchClick"
                    v-model="listQuery.ticketid"></el-input>
          <el-input style="width: 180px;" class="filter-item" placeholder="工单标题、内容或类型" @keyup.enter.native="searchClick"
                    v-model="listQuery.search"></el-input>
          <el-button class="filter-item" type="primary" icon="search" @click="searchClick">搜索</el-button>
        </div>
      </div>
      <div>
        <el-table :data="tableData" border style="width: 100%" @selection-change="handleSelectionChange"
                  @sort-change="handleSortChange">
          <el-table-column type="selection" v-if="workticketlist_btn_change_status||role==='super'"></el-table-column>
          <el-table-column prop='ticketid' label='工单编号'>
            <template slot-scope="scope">
              <router-link :to="'editworkticket/' + scope.row.ticketid">
                <a style="color: #257cff">{{scope.row.ticketid}}</a>
              </router-link>
            </template>
          </el-table-column>
          <el-table-column prop='title' label='标题'></el-table-column>
          <el-table-column prop='type' label='工单类型'></el-table-column>
          <el-table-column prop='level' label='工单等级' sortable="custom">
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
          <el-table-column prop='ticket_status' label='工单状态' sortable="custom">
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper" style="text-align: center; color: rgb(0,0,0)">
                <el-tag :type="TICKET_STATUS_TYPE[scope.row.ticket_status]">
                  {{TICKET_STATUS_TEXT[scope.row.ticket_status]}}
                </el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='create_user' label='工单创建人'></el-table-column>
          <el-table-column prop='action_user' label='工单指派者'></el-table-column>
          <el-table-column prop='edit_user' label='最新回复人'></el-table-column>
          <el-table-column prop='create_time' label='工单创建时间' sortable="custom">
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper" style="text-align: center; color: rgb(0,0,0)">
                <span>{{scope.row.create_time | parseDate}}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='update_time' label='工单更新时间' sortable="custom">
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper" style="text-align: center; color: rgb(0,0,0)">
                <span>{{scope.row.update_time | parseDate}}</span>
              </div>
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

    <el-dialog
      title="更改状态"
      :visible.sync="show_status">
      <el-radio-group v-model="select_status">
        <el-radio :label="0">未接收</el-radio>
        <el-radio :label="1">正在处理</el-radio>
        <el-radio :label="2">已关闭</el-radio>
      </el-radio-group>
      <span slot="footer" class="dialog-footer">
    <el-button @click="show_status=false">取 消</el-button>
    <el-button type="primary" @click="changeForm">确 定</el-button>
  </span>
    </el-dialog>
  </div>
</template>

<script>
import { getWorkticket, patchWorkticket } from 'api/workticket'
import { LIMIT } from '@/config'
import addWorkticket from './components/addworkticket.vue'
import { mapGetters } from 'vuex'

export default {
  components: { addWorkticket },
  data() {
    return {
      radio: '',
      tableData: [],
      tabletotal: 0,
      currentPage: 1,
      ticket_status: '',
      pagesize: [10, 25, 50, 100],
      rowdata: {
        ticket_status: 0,
        action_user: localStorage.getItem('username')
      },
      TICKET_STATUS_TEXT: { '0': '未接收', '1': '正在处理', '2': '已解决' },
      TICKET_STATUS_TYPE: { '0': 'danger', '1': 'success', '2': 'info' },
      listQuery: {
        limit: LIMIT,
        offset: '',
        ticketid: '',
        ticket_status: '',
        create_user: '',
        action_user: '',
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
      getWorkticket(this.listQuery).then(response => {
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
      this.listQuery.create_user = localStorage.getItem('username')
      this.listQuery.action_user = ''
      this.fetchData()
    },
    showMeAction() {
      this.listQuery.action_user = localStorage.getItem('username')
      this.listQuery.create_user = ''
      this.fetchData()
    },
    showAllTicket() {
      this.listQuery.create_user = ''
      this.listQuery.action_user = ''
      this.listQuery.search = ''
      this.listQuery.ticket_status = ''
      this.fetchData()
    },
    handleSelectionChange(val) {
      this.selectId = []
      for (var i = 0, len = val.length; i < len; i++) {
        this.selectId.push(val[i].id)
      }
      if (this.selectId.length > 0) {
        this.btnstatus = false
      } else {
        this.btnstatus = true
      }
    },
    changeForm() {
      for (var i = 0, len = this.selectId.length; i < len; i++) {
        this.rowdata.ticket_status = this.select_status
        patchWorkticket(this.selectId[i], this.rowdata).then(response => {
          delete this.selectId[i]
        })
      }
      setTimeout(this.fetchData, 2000)
      this.show_status = false
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
  .head-lavel {
    padding-bottom: 50px;
  }

  .table-button {
    padding: 10px 0;
    float: left;
  }

  .table-search {
    float: right;
    padding: 10px 0;
  }

  .table-pagination {
    padding: 10px 0;
    float: right;
  }
</style>
