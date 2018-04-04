<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <div class="head-lavel">
        <div class="table-button">
          <el-button type="primary" icon="el-icon-plus" @click="addForm=true">新建</el-button>
        </div>
        <div class="table-search">
          <el-input
            placeholder="search"
            v-model="listQuery.search"
            @keyup.enter.native="searchClick">
            <i class="el-icon-search el-input__icon" slot="suffix" @click="searchClick"></i>
          </el-input>
        </div>
      </div>
      <div>
        <el-table :data="tableData" border style="width: 100%" @sort-change="handleSortChange">
          <el-table-column prop='id' label='ID'></el-table-column>
          <el-table-column prop='name' label='标题'></el-table-column>
          <el-table-column prop='content' label='SQL'>
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper" style="text-align: center; color: rgb(0,0,0)">
                <el-button type="primary" size="mini" @click="showSqlContent(scope.row.content)">查看</el-button>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='desc' label='说明'></el-table-column>
          <el-table-column prop='status' label='状态' sortable="custom">
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper" style="text-align: center; color: rgb(0,0,0)">
                <el-tag :type="STATUS_COLOR[scope.row.status]">
                  {{STATUS_TEXT[scope.row.status]}}
                </el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='create_user' label='创建人'></el-table-column>
          <el-table-column prop='create_time' label='创建时间' sortable="custom">
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper" style="text-align: center; color: rgb(0,0,0)">
                <span>{{scope.row.create_time | parseDate}}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column v-if="role==='super'" label="操作">
            <template slot-scope="scope">
              <el-button-group v-if="scope.row.status!=1">
                <el-button @click="editSqlContent(scope.row)" type="success" size="mini">修改</el-button>
                <el-button @click="changeSqlOnline(scope.row)" type="primary" size="mini">已执行</el-button>
              </el-button-group>
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
            :layout="pageformat"
            :total="tabletotal">
          </el-pagination>
        </div>
      </div>
    </el-card>

    <el-dialog :visible.sync="addForm">
      <add-group @DialogStatus="getDialogStatus"></add-group>
    </el-dialog>

    <el-dialog :visible.sync="editForm">
      <edit-group :ruleForm="rowdata" @DialogStatus="getDialogStatus"></edit-group>
    </el-dialog>

    <el-dialog :visible.sync="showForm">
      <el-button type="primary" size="mini" icon="document" @click='handleCopy(selectsql,$event)'>copy
      </el-button>
      <prism language="sql" :plugins="['toolbar', 'show-language']" :code="selectsql"></prism>
    </el-dialog>
  </div>
</template>

<script>
import { getSqlTicket, patchSqlTicket } from '@/api/job'
import { LIMIT, pagesize, pageformat } from '@/config'
import { postSendmessage } from 'api/tool'
import { mapGetters } from 'vuex'
import addGroup from './components/addsqlticket.vue'
import editGroup from './components/editsqlticket.vue'
import Prism from 'vue-prismjs'
import clip from '@/utils/clipboard' // use clipboard directly
import clipboard from '@/directive/clipboard/index.js' // use clipboard by v-directive

export default {
  components: {
    addGroup, editGroup, Prism
  },
  directives: {
    clipboard
  },
  data() {
    return {
      tableData: [],
      tabletotal: 0,
      currentPage: 1,
      ticket_status: '',
      pagesize: pagesize,
      pageformat: pageformat,
      STATUS_TEXT: {
        0: '未执行',
        1: '已执行'
      },
      STATUS_COLOR: {
        0: 'danger',
        1: 'success'
      },
      listQuery: {
        limit: LIMIT,
        offset: '',
        search: '',
        ordering: ''
      },
      addForm: false,
      editForm: false,
      showForm: false,
      rowdata: {},
      selectsql: ''
    }
  },
  computed: {
    ...mapGetters([
      'role'
    ])
  },
  created() {
    this.fetchData()
  },

  methods: {
    fetchData() {
      getSqlTicket(this.listQuery).then(response => {
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
    changeSqlOnline(row) {
      const data = {
        status: 1
      }
      patchSqlTicket(row.id, data).then(() => {
        const messageForm = {
          action_user: 'ITDept_SkypeID',
          title: '【sql已执行】',
          message: this.rowdata.name
        }
        postSendmessage(messageForm)
        this.fetchData()
      })
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
    },
    editSqlContent(row) {
      this.editForm = true
      this.rowdata = row
    },
    getDialogStatus(data) {
      this.addForm = data
      this.editForm = data
      this.fetchData()
    },
    showSqlContent(sql) {
      this.showForm = true
      this.selectsql = sql
    },
    handleCopy(text, event) {
      clip(text, event)
    },
    clipboardSuccess() {
      this.$message({
        message: '复制成功',
        type: 'success',
        duration: 1000
      })
    }
  }
}
</script>

<style lang='scss'>
</style>
