<template>
  <div class="components-container" style='height:100vh'>
        <el-card>
            <div class="head-lavel">
                <div class="table-button">
                    <router-link :to="'addworkticket'">
                        <el-button type="primary" icon="el-icon-plus">新建工单</el-button>
                    </router-link>

                    <el-radio-group v-model="radio" @change="statusChange" style="margin-left: 20px">
                        <el-radio label="0">未接收</el-radio>
                        <el-radio label="1">正在处理</el-radio>
                        <el-radio label="2">已解决</el-radio>
                        <el-radio label="">全部</el-radio>
                    </el-radio-group>

                </div>
                <div class="table-search">
                    <el-input style="width: 110px;" class="filter-item" placeholder="工单发起人" @keyup.enter.native="searchClick" v-model="listQuery.create_user"></el-input>
                    <el-input style="width: 160px;" class="filter-item" placeholder="工单编号" @keyup.enter.native="searchClick" v-model="listQuery.ticketid"></el-input>
                    <el-input style="width: 160px;" class="filter-item" placeholder="工单内容" @keyup.enter.native="searchClick" v-model="listQuery.content"></el-input>
                    <el-button class="filter-item" type="primary" icon="search" @click="searchClick">搜索</el-button>
                </div>
            </div>
            <div>
                <el-table :data="tableData" border style="width: 100%" v-loading="loading">
                    <el-table-column prop='title' label='工单编号'>
                        <template slot-scope="scope">
                            <div slot="reference" style="text-align: center; color: rgb(52,91,225)">
                                <router-link :to="'editworkticket/'+scope.row.id">
                                    {{scope.row.ticketid}}
                                </router-link>
                            </div>
                        </template>
                    </el-table-column>
                    <el-table-column prop='title' label='标题'></el-table-column>
                    <el-table-column prop='create_user' label='工单创建人'></el-table-column>
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
                    <el-table-column prop='action_user' label='当前处理人'></el-table-column>
                </el-table>
            </div>
            <div class="table-footer">
                <div class="table-pagination">
                    <el-pagination
                            small
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
    </div>
</template>

<script>
import { getWorkticket } from 'api/workticket'
import { LIMIT } from '@/config'
import addWorkticket from './addworkticket.vue'

export default {
  components: { addWorkticket },
  data() {
    return {
      loading: true,
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
        action_user: sessionStorage.getItem('username')
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
        content: ''
      }
    }
  },

  created() {
    this.fetchData()
  },

  methods: {
    fetchData() {
      const id = null
      const parms = {
        limit: this.limit,
        offset: this.offset,
        content__contains: this.listQuery.content,
        ticket_status: this.ticket_status,
        ticketid: this.listQuery.ticketid,
        create_user__username: this.listQuery.create_user
      }
      getWorkticket(id, parms).then(response => {
        this.tableData = response.data.results
        this.tabletotal = response.data.count
        this.loading = false
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
