<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <div class="head-lavel">
        <div class="table-button">
          <router-link :to="'addopsdemand'">
            <el-button type="primary" icon="el-icon-plus">新建</el-button>
          </router-link>
          <el-radio-group v-model="listQuery.status" @change="changeStatus" style="margin-left: 20px">
            <el-radio v-for="item in Object.keys(STATUS_TEXT)" :key="item" :label="item">{{STATUS_TEXT[item]}}
            </el-radio>
          </el-radio-group>
        </div>
        <div class="table-search">
          <el-input style="width: 180px;" placeholder="编号、标题、内容"
                    @keyup.enter.native="searchClick"
                    v-model="listQuery.search">
            <i class="el-icon-search el-input__icon" slot="suffix" @click="searchClick"></i>
          </el-input>
        </div>
      </div>
      <div>
        <el-table :data="tableData" border style="width: 100%" @sort-change="handleSortChange">
          <el-table-column prop='pid' label='编号'>
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper">
                <router-link :to="'viewopsdemand/' + scope.row.id">
                  <a style="color: #257cff">{{scope.row.pid}}</a>
                </router-link>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='name' label='名称'></el-table-column>
          <el-table-column prop='status' label='状态'>
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper">
                <el-tag size="mini">
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
          <el-table-column prop='start_time' label='开始日期'></el-table-column>
          <el-table-column prop='end_time' label='结束日期'></el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <router-link :to="'editopsdemand/' + scope.row.id">
                <el-button type="success" size="small">修改</el-button>
              </router-link>
              <el-button type="danger" size="small" @click="deleteDemand(scope.row.id)">删除</el-button>
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
  </div>
</template>

<script>
import { getDemandManager, deleteDemandManager } from '@/api/optask'
import { LIMIT, pagesize, pageformat } from '@/config'

export default {
  components: {},
  data() {
    return {
      tableData: [],
      tabletotal: 0,
      currentPage: 1,
      pagesize: pagesize,
      pageformat: pageformat,
      STATUS_TEXT: {
        0: '进行中',
        1: '已完成',
        2: '搁置'
      },
      listQuery: {
        limit: LIMIT,
        offset: '',
        pid: '',
        status: '0',
        create_user__username: '',
        search: '',
        ordering: ''
      },
      updateform: {
        id: '',
        status: '1'
      }
    }
  },
  created() {
    this.fetchData()
  },

  methods: {
    fetchData() {
      getDemandManager(this.listQuery).then(response => {
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
    changeStatus() {
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
    },
    deleteDemand(id) {
      deleteDemandManager(id).then(response => {
        this.$message({
          message: '恭喜你，删除成功',
          type: 'success'
        })
        this.fetchData()
      }).catch(error => {
        this.$message.error('删除失败')
        console.log(error)
      })
    }
  }
}
</script>

<style lang='scss'>
  .modifychange {
    margin: 5px;
  }
</style>
