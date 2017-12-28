<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <div class="head-lavel">
        <div class="table-button">
        </div>
        <div class="table-search">
          <el-input
            placeholder="搜索 ..."
            v-model="searchdata"
            @keyup.enter.native="searchClick">
            <i class="el-icon-search el-input__icon" slot="suffix" @click="searchClick"></i>
          </el-input>
        </div>
      </div>
      <div>
        <el-table :data="tableData" @selection-change="handleSelectionChange" border style="width: 100%">
          <el-table-column type="selection"></el-table-column>
          <el-table-column prop='user' label='收件人' sortable></el-table-column>
          <el-table-column prop='title' label='标题' sortable></el-table-column>
          <el-table-column prop='message' label='消息内容' sortable></el-table-column>
          <!--<el-table-column prop='is_html' label='是否html' sortable></el-table-column>-->
          <!--<el-table-column prop='duration' label='显示时间'></el-table-column>-->
          <!--<el-table-column prop='state' label='已读' sortable></el-table-column>-->
        </el-table>
      </div>
      <div class="table-footer">
        <div class="table-button">
          <el-button type="danger" icon="delete" :disabled="butstatus" @click="deleteForm">删除记录</el-button>
        </div>
        <div class="table-pagination">
          <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page.sync="listQuery.offset"
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
import { getSendmessage, deleteSendmessage } from 'api/tool'
import { LIMIT } from '@/config'

export default {
  components: {},
  data() {
    return {
      tableData: [],
      tabletotal: 0,
      searchdata: '',
      pagesize: [10, 25, 50, 100],
      rowdata: {},
      selectId: [],
      butstatus: true,
      listQuery: {
        offset: null,
        limit: LIMIT
      }
    }
  },

  created() {
    this.fetchData()
  },

  methods: {
    fetchData() {
      getSendmessage(this.listQuery).then(response => {
        this.tableData = response.data.results
        this.tabletotal = response.data.count
      })
    },

    handleSelectionChange(val) {
      this.selectId = []
      for (var i = 0, len = val.length; i < len; i++) {
        this.selectId.push(val[i].id)
      }
      if (this.selectId.length > 0) {
        this.butstatus = false
      } else {
        this.butstatus = true
      }
    },

    handleSizeChange(val) {
      this.listQuery.limit = val
      this.fetchData()
    },
    handleCurrentChange(val) {
      this.listQuery.offset = (val - 1) * LIMIT
      this.fetchData()
    },
    searchClick() {
      this.fetchData()
    },
    deleteForm() {
      for (var i = 0, len = this.selectId.length; i < len; i++) {
        deleteSendmessage(this.selectId[i]).then(response => {
          delete this.selectId[i]
        })
      }
      setTimeout(this.fetchData, 1000)
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
