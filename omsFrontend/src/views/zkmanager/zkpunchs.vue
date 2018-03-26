<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <div class="head-lavel">
        <div class="table-button">
        </div>
        <div class="table-search">
          <el-date-picker
            v-model="selectcreatedate"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            @change="selectCreatedate"
            :picker-options="pickerOptions">
          </el-date-picker>
          <el-input
            style="width: 200px;"
            placeholder="搜索 ..."
            v-model="listQuery.search"
            @keyup.enter.native="searchClick">
            <i class="el-icon-search el-input__icon" slot="suffix" @click="searchClick"></i>
          </el-input>
        </div>
      </div>
      <div>
        <el-table :data='tableData' border style="width: 100%">
          <el-table-column prop='user' label='用户'></el-table-column>
          <el-table-column prop='status' label='打卡状态'>
            <template slot-scope="scope">
              <div slot="reference">
                <el-tag :type="Punch_Color[scope.row.status]">{{Punch_Text[scope.row.status]}}</el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='create_date' label='打卡日期'></el-table-column>
          <el-table-column prop='swork_time' label='签到时间'></el-table-column>
          <el-table-column prop='ework_time' label='签退时间'></el-table-column>
          <el-table-column prop='swork_timec' label='迟到时间'></el-table-column>
          <el-table-column prop='ework_timec' label='早退时间'></el-table-column>
          <el-table-column prop='work_time' label='实际工作时间'></el-table-column>
          <!--<el-table-column label="操作">-->
          <!--<template slot-scope="scope">-->
          <!--<el-button @click="deleteGroup(scope.row.id)" type="danger" size="small">删除</el-button>-->
          <!--</template>-->
          <!--</el-table-column>-->
        </el-table>
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
    </el-card>
  </div>
</template>

<script>
import { getzkPunch, deletezkPunch } from 'api/zk'
import { LIMIT, pagesize, pageformat } from '@/config'
import formatDate from '@/utils/dateformat'

export default {
  components: {},
  data() {
    return {
      tableData: [],
      tabletotal: 0,
      searchdata: '',
      currentPage: 1,
      pagesize: pagesize,
      pageformat: pageformat,
      listQuery: {
        limit: LIMIT,
        offset: '',
        search: ''
      },
      selectcreatedate: [],
      pickerOptions: {
        shortcuts: [{
          text: '最近一周',
          onClick(picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '最近一个月',
          onClick(picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '最近三个月',
          onClick(picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
            picker.$emit('pick', [start, end])
          }
        }]
      },
      Punch_Text: {
        0: '旷工',
        1: '签到',
        2: '签退',
        3: '迟到',
        4: '早退'
      },
      Punch_Color: {
        0: 'danger',
        1: 'success',
        2: 'success',
        3: 'warning',
        4: 'warning'
      }
    }
  },

  created() {
    this.fetchData()
  },

  methods: {
    fetchData() {
      getzkPunch(this.listQuery).then(response => {
        this.tableData = response.data.results
        this.tabletotal = response.data.count
      })
    },
    deleteGroup(id) {
      deletezkPunch(id).then(response => {
        this.$message({
          message: '恭喜你，删除成功',
          type: 'success'
        })
        this.fetchData()
      }).catch(error => {
        this.$message.error('删除失败')
        console.log(error)
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
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    selectCreatedate(val) {
      if (val) {
        this.listQuery.create_date_0 = formatDate(val[0], 'YYYY-MM-DD')
        this.listQuery.create_date_1 = formatDate(val[1], 'YYYY-MM-DD')
      } else {
        this.listQuery.create_date_0 = ''
        this.listQuery.create_date_1 = ''
      }
      this.fetchData()
    }
  }
}
</script>

<style lang='scss'>

</style>
