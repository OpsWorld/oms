<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <div class="head-lavel">
        <div class="table-button">
          <el-button type="primary" icon="el-icon-plus">新建</el-button>
        </div>
        <div class="table-search">
          <el-input
            placeholder="search"
            v-model="searchdata"
            @keyup.enter.native="searchClick">
            <i class="el-icon-search el-input__icon" slot="suffix" @click="searchClick"></i>
          </el-input>
        </div>
      </div>
      <div>
        <el-table :data='tableData' style="width: 100%">
          <el-table-column type="index" width="50"></el-table-column>
          <el-table-column prop='name' label='名称' sortable></el-table-column>
          <el-table-column prop='deploy_status' label='发布状态'>
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper" style="text-align: center">
                <el-tag :type="DEPLOY_STATUS[scope.row.deploy_status].type">
                  {{DEPLOY_STATUS[scope.row.assedeploy_statust_type].text}}
                </el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='create_time' label='创建时间'></el-table-column>
          <el-table-column prop='update_time' label='最近发布时间'></el-table-column>
          <el-table-column prop='desc' label='描述'></el-table-column>
        </el-table>
      </div>
      <div class="table-pagination">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page.sync="currentPage"
          :page-sizes="pagesize"
          :page-size="listQuery.limit"
          layout="prev, pager, next, sizes"
          :total="tabletotal">
        </el-pagination>
      </div>
    </el-card>
  </div>
</template>

<script>
import { getJob, deleteJob } from '@/api/job'
import { LIMIT } from '@/config'

export default {
  components: {},
  data() {
    return {
      tableData: [],
      tabletotal: 0,
      searchdata: '',
      currentPage: 1,
      listQuery: {
        limit: LIMIT,
        offset: '',
        search: ''
      },
      limit: LIMIT,
      offset: '',
      pagesize: [10, 25, 50, 100],
      DEPLOY_STATUS: {
        'noaction': { 'text': '未执行', 'type': 'info' },
        'deploy': { 'text': '发布中', 'type': 'primary' },
        'success': { 'text': '发布成功', 'type': 'success' },
        'failed': { 'text': '发布失败', 'type': 'danger' }
      }
    }
  },

  created() {
    this.fetchData()
  },

  methods: {
    fetchData() {
      getJob(this.listQuery).then(response => {
        this.tableData = response.data.results
        this.tabletotal = response.data.count
      })
    },
    deleteGroup(id) {
      deleteJob(id).then(response => {
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
      this.listQuery.search = this.searchdata
      this.fetchData()
    },
    handleSizeChange(val) {
      this.listQuery.limit = val
      this.fetchData()
    },
    handleCurrentChange(val) {
      this.listQuery.offset = (val - 1) * LIMIT
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
    float: left;
  }

  .table-search {
    float: right;
  }

  .table-pagination {
    padding: 10px 0;
    float: right;
  }
</style>
