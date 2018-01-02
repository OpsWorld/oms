<template>
  <div class="components-container" style='height:100vh'>
    <el-card class="wiki">
      <div class="wiki-header">
        <H2>OMS文档知识库</H2>
        <div class="wiki-search">
          <el-input placeholder="search . . ." v-model="searchdata" class="input-with-select">
            <el-button slot="append" icon="el-icon-search"></el-button>
          </el-input>
        </div>
        <hr class="heng"/>
      </div>
      <div class="wiki-content">
        <div class="wiki-data" v-for="item in tableData" :key="item.id">
          <p>{{item.title}}</p>
          <p>{{item.type}}</p>
          <p>{{item.content}}</p>
        </div>
        <div class="table-pagination">
          <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page.sync="currentPage"
            :page-size="listQuery.limit"
            layout="prev, pager, next"
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
    margin: 0 auto;
    width: 80%;
    text-align: center;
    .wiki-search {
      margin: 0 auto;
      width: 500px;
    }
  }
</style>
