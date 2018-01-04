<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <div class="head-lavel">
        <div class="table-button">
          <router-link :to="'addwiki'">
            <el-button type="primary" icon="el-icon-plus">新建</el-button>
          </router-link>
        </div>
        <div class="table-search">
          <el-input
            placeholder="主机名或ip"
            v-model="searchdata"
            @keyup.enter.native="searchClick">
            <i class="el-icon-search el-input__icon" slot="suffix" @click="searchClick"></i>
          </el-input>
        </div>
      </div>
      <div>
        <el-table :data='tableData' border style="width: 100%">
          <el-table-column prop='hostname' label='主机名'></el-table-column>
          <el-table-column prop='ip' label='ip'></el-table-column>
          <el-table-column prop='other_ip' label='其他ip'></el-table-column>
          <el-table-column prop='idc' label='机房'></el-table-column>
          <el-table-column prop='asset_type' label='类型'></el-table-column>
          <el-table-column prop='status' label='状态'></el-table-column>
          <el-table-column prop='os' label='系统'></el-table-column>
          <el-table-column prop='cpu' label='CPU信息'></el-table-column>
          <el-table-column prop='memory' label='内存信息'></el-table-column>
          <el-table-column prop='disk' label='硬盘信息'></el-table-column>
          <el-table-column prop='desc' label='状态'></el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button type="primary" size="small">修改</el-button>
              <el-button type="danger" size="small">删除</el-button>
            </template>
          </el-table-column>
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
import { getWiki, deleteWiki } from 'api/wiki'
import { LIMIT } from '@/config'

export default {
  data() {
    return {
      tableData: [],
      tabletotal: 0,
      searchdata: '',
      currentPage: 1,
      pagesize: [10, 25, 50, 100],
      rowdata: {},
      listQuery: {
        limit: LIMIT,
        offset: '',
        create_user__username: localStorage.getItem('username'),
        search: this.searchdata
      }
    }
  },

  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      getWiki(this.listQuery).then(response => {
        this.tableData = response.data.results
        this.tabletotal = response.data.count
      })
    },
    deleteGroup(id) {
      deleteWiki(id).then(response => {
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
    closeEditForm() {
      this.fetchData()
    },
    handleEdit(row) {
      this.editForm = true
      this.rowdata = row
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
