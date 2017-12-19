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

          <el-radio-group v-model="radio" @change="statusChange" style="margin-left: 20px">
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
        <el-table :data="tableData" border style="width: 100%" @selection-change="handleSelectionChange">
          <el-table-column type="selection" v-if="workticketlist_btn_change_status||role==='super'"></el-table-column>
          <el-table-column prop='ticketid' label='工单编号'>
            <template slot-scope="scope">
              <div slot="reference" style="text-align: center; color: rgb(52,91,225)">
                <router-link :to="{name:'editworkticket',params:{ticketid:scope.row.ticketid}}">
                  {{scope.row.ticketid}}
                </router-link>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='title' label='标题'></el-table-column>
          <el-table-column prop='type' label='工单类型' sortable></el-table-column>
          <el-table-column prop='level' label='工单等级' sortable>
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper" style="text-align: center">
                <el-tag :type="LEVEL[scope.row.level].type">
                  {{LEVEL[scope.row.level].text}}
                </el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='ticket_status' label='工单状态'>
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper" style="text-align: center; color: rgb(0,0,0)">
                <el-tag :type="TICKET_STATUS[scope.row.ticket_status].type">
                  {{TICKET_STATUS[scope.row.ticket_status].text}}
                </el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='create_user' label='工单创建人'></el-table-column>
          <el-table-column prop='action_user' label='当前处理人'></el-table-column>
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
            :page-size="limit"
            layout="prev, pager, next, sizes"
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
import addWorkticket from './addworkticket.vue'
import { mapGetters } from 'vuex'

export default {
  components: { addWorkticket },
  data() {
    return {
      radio: '',
      tableData: [],
      tabletotal: 0,
      searchdata: '',
      currentPage: 1,
      limit: LIMIT,
      offset: '',
      ticket_status: '',
      pagesize: [10, 25, 50, 100],
      addForm: false,
      rowdata: {
        ticket_status: 0,
        action_user: localStorage.getItem('username')
      },
      changedata: {
        ticket_status: 0
      },
      TICKET_STATUS: {
        '0': { 'text': '未接收', 'type': 'info' },
        '1': { 'text': '正在处理', 'type': 'success' },
        '2': { 'text': '已解决', 'type': 'danger' }
      },
      LEVEL: {
        '1': { 'text': 'A', 'type': 'danger' },
        '2': { 'text': 'B', 'type': 'warning' },
        '3': { 'text': 'C', 'type': 'success' },
        '4': { 'text': 'D', 'type': 'info' },
        '5': { 'text': 'E', 'type': '' }
      },
      listQuery: {
        ticketid: '',
        create_user: '',
        action_user: '',
        search: ''
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
      const parms = {
        limit: this.limit,
        offset: this.offset,
        search: this.listQuery.search,
        ticket_status: this.ticket_status,
        ticketid: this.listQuery.ticketid,
        create_user__username: this.listQuery.create_user,
        action_user__username: this.listQuery.action_user
      }
      getWorkticket(parms).then(response => {
        this.tableData = response.data.results
        this.tabletotal = response.data.count
      })
    },
    searchClick() {
      this.fetchData()
    },
    handleSizeChange(val) {
      this.limit = val
      this.fetchData()
    },
    handleCurrentChange(val) {
      this.offset = val - 1
      this.fetchData()
    },
    statusChange(val) {
      this.ticket_status = val
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
      this.ticket_status = ''
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
        this.changedata.ticket_status = this.select_status
        patchWorkticket(this.selectId[i], this.changedata).then(response => {
          delete this.selectId[i]
        })
      }
      setTimeout(this.fetchData, 3000)
      this.show_status = false
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
