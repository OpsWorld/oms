<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <div class="head-lavel">
        <div class="table-button">
          <el-button type="primary" icon="el-icon-plus" @click="addForm=true">新建</el-button>
        </div>
        <div class="table-search">
          <el-date-picker
            v-model="selectdatatime"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            @change="selectDatetime">
          </el-date-picker>
          <el-input
            placeholder="search"
            v-model="listQuery.search"
            @keyup.enter.native="searchClick"
            style="width: 200px">
            <i class="el-icon-search el-input__icon" slot="suffix" @click="searchClick"></i>
          </el-input>
        </div>
      </div>
      <div>
        <el-table :data='tableData' border style="width: 100%">
          <el-table-column prop='name' label='模块名称' width="100"></el-table-column>
          <el-table-column prop='type' label='添加类型' width="80">
            <template slot-scope="scope">
              <div slot="reference">
                {{AddTypes[scope.row.type]}}
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='asset' label='资产名称' width="210"></el-table-column>
          <el-table-column prop='method' label='操作类型' width="80"></el-table-column>
          <el-table-column prop='before' label='修改前数据' width="150">
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
          <el-table-column prop='after' label='修改后数据' width="150">
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
          <el-table-column prop='diff' label='前后数据对比'>
            <template slot-scope="scope">
              <div slot="reference" v-for="item in strToJson(scope.row.diff)" :key="item.id">
                <el-tag type="danger" size="mini">{{item.replace.replace('/', '')}}</el-tag>
                ：
                <div class="prevalue">
                  前：
                  <el-tag size="mini">{{item.prev}}</el-tag>
                </div>
                <div class="prevalue">
                  后：
                  <el-tag type="primary" size="mini">{{item.value}}</el-tag>
                </div>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='create_user' label='操作人' width="100"></el-table-column>
          <el-table-column prop='create_time' label='创建时间' sortable width="200">
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper" style="text-align: center; color: rgb(0,0,0)">
                <span>{{scope.row.create_time | parseDate}}</span>
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
            :layout="pageformat"
          :total="tabletotal">
        </el-pagination>
      </div>
    </el-card>

    <el-dialog :visible.sync="addForm">
      <add-obj @formdata="addGroupSubmit"></add-obj>
    </el-dialog>
  </div>
</template>

<script>
import { getRecord, postRecord } from '@/api/tool'
import { LIMIT, pagesize, pageformat } from '@/config'
import addObj from './components/addrecord.vue'
import formatDate from '@/utils/dateformat'

export default {
  components: { addObj },
  data() {
    return {
      tableData: [],
      tabletotal: 0,
      currentPage: 1,
      listQuery: {
        limit: LIMIT,
        offset: '',
        search: '',
        create_time_0: '',
        create_time_1: ''
      },
      pagesize: pagesize,
      pageformat: pageformat,
      AddTypes: { 0: '手动', 1: '自动' },
      addForm: false,
      selectdatatime: ''
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
    },
    addGroupSubmit(formdata) {
      postRecord(formdata).then(response => {
        this.$message({
          message: '恭喜你，添加成功',
          type: 'success'
        })
        this.fetchData()
        this.addForm = false
      }).catch(error => {
        this.$message.error('添加失败')
        console.log(error)
      })
    },
    selectDatetime(val) {
      if (val) {
        this.listQuery.create_time_0 = formatDate(val[0], 'YYYY-MM-DD')
        this.listQuery.create_time_1 = formatDate(val[1], 'YYYY-MM-DD')
      } else {
        this.listQuery.create_time_0 = ''
        this.listQuery.create_time_1 = ''
      }
      this.fetchData()
    },
    strToJson(str) {
      var json = (new Function('return ' + str.replace('True', 'true')))()
      return json
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

  .prevalue {
    margin-left: 18px;
  }
</style>
