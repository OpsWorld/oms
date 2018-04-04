<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <div class="head-lavel">
        <div class="table-button">
        </div>
        <div class="table-search">
          <el-input
            placeholder="搜索 ..."
            v-model="listQuery.search"
            @keyup.enter.native="searchClick">
            <i class="el-icon-search el-input__icon" slot="suffix" @click="searchClick"></i>
          </el-input>
        </div>
      </div>
      <div>
        <el-button type="primary" size="mini" icon="document" @click='handleCopy(listQuery.search,$event)'>copy
        </el-button>
        <prism language="sql" :plugins="['toolbar', 'show-language']" :code="listQuery.search"></prism>
        <el-table :data='tableData' border style="width: 100%">
          <el-table-column prop='username' label='用户' sortable></el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button @click="deleteGroup(scope.row.id)" type="danger" size="small">删除</el-button>
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
          :layout="pageformat"
          :total="tabletotal">
        </el-pagination>
      </div>
    </el-card>
  </div>
</template>

<script>
import { getzkUser, deletezkUser } from 'api/zk'
import { LIMIT, pagesize, pageformat } from '@/config'
import Prism from 'vue-prismjs'
import clip from '@/utils/clipboard' // use clipboard directly
import clipboard from '@/directive/clipboard/index.js' // use clipboard by v-directive

export default {
  components: {
    Prism
  },

  directives: {
    clipboard
  },
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
      }
    }
  },

  created() {
    this.fetchData()
  },

  methods: {
    fetchData() {
      getzkUser(this.listQuery).then(response => {
        this.tableData = response.data.results
        this.tabletotal = response.data.count
      })
    },
    deleteGroup(id) {
      deletezkUser(id).then(response => {
        this.$message({
          message: '恭喜你，删除成功',
          type: 'success'
        })
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
    handleCopy(text, event) {
      clip(text, event)
    },
    clipboardSuccess() {
      this.$message({
        message: '复制成功',
        type: 'success',
        duration: 1500
      })
    }
  }
}
</script>

<style lang='scss'>

</style>
