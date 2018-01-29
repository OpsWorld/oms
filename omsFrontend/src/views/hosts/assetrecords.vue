<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <div class="head-lavel">
        <div class="table-button">
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
        <el-table :data='tableData' border style="width: 100%">
          <el-table-column prop='name' label='模块名称'></el-table-column>
          <el-table-column prop='type' label='添加类型'>
            <template slot-scope="scope">
              <div slot="reference" style="text-align: center">
                {{AddTypes[scope.row.type]}}
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='asset' label='资产名称'></el-table-column>
          <el-table-column prop='method' label='操作类型'></el-table-column>
          <el-table-column prop='before' label='修改前数据'>
            <template slot-scope="scope">
              <div slot="reference" style="text-align: center">
                <el-popover
                  placement="top"
                  width="300"
                  trigger="hover"
                  :content="scope.row.before">
                  <el-button size="mini" slot="reference">{...}</el-button>
                </el-popover>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='after' label='修改后数据'>
            <template slot-scope="scope">
              <div slot="reference" style="text-align: center">
                <el-popover
                  placement="top"
                  width="300"
                  trigger="hover"
                  :content="scope.row.after">
                  <el-button size="mini" slot="reference">{...}</el-button>
                </el-popover>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='create_time' label='创建时间' sortable>
            <template slot-scope="scope">
              <div slot="reference">
                {{scope.row.create_time | formatTime}}
              </div>
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
import { getRecord } from '@/api/tool'
import { LIMIT } from '@/config'

export default {
  components: {},
  data() {
    return {
      tableData: [],
      tabletotal: 0,
      currentPage: 1,
      listQuery: {
        limit: LIMIT,
        offset: '',
        search: ''
      },
      limit: LIMIT,
      offset: '',
      pagesize: [10, 25, 50, 100],
      AddTypes: { 0: '手动', 1: '自动' }
    }
  },

  created() {
    this.fetchData()
  },

  methods: {
    fetchData() {
      getRecord(this.listQuery).then(response => {
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
