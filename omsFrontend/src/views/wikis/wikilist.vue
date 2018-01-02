<template>
  <div class="components-container" style='height:100vh'>
    <el-card class="wiki">
      <el-row :gutter="20">
        <el-col :span="4">
          <div style="margin: 15px">文档知识库</div>
        </el-col>
        <el-col :span="20">
          <el-input placeholder="search . . ." v-model="searchdata" class="input-with-select">
            <el-button slot="append" icon="el-icon-search"></el-button>
          </el-input>
        </el-col>
      </el-row>
      <hr class="heng"/>
      <div class="content">
        <div class="table-data" v-for="item in tableData" :key="item.id">
          <p>{{item.title}}</p>
          <p>{{item.type}}</p>
          <p>{{item.content}}</p>
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
      </div>
    </el-card>
  </div>
</template>
<script>
import { getWiki } from 'api/wiki'
import { LIMIT } from '@/config'

export default {
  data() {
    return {
      searchdata: '',
      tableData: [],
      tabletotal: 0,
      currentPage: 1,
      pagesize: [10, 25, 50, 100],
      listQuery: {
        limit: LIMIT,
        offset: '',
        title__contains: this.searchdata
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
  .wiki {
    margin: 50px;
  }

  .table-pagination {
    padding: 10px 0;
    float: right;
  }
</style>
