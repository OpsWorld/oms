<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <div class="head-lavel">
        <div class="table-button">
          <el-button type="primary" icon="el-icon-plus" @click="addGroup=true">新建用户组</el-button>
        </div>
        <div class="table-search">
          <el-input
            placeholder="搜索 ..."
            v-model="listQuery.name"
            @keyup.enter.native="searchClick">
            <i class="el-icon-search el-input__icon" slot="suffix" @click="searchClick"></i>
          </el-input>
        </div>
      </div>
      <div>
        <el-table :data='tableData' border style="width: 100%">
          <el-table-column prop='name' label='组名'></el-table-column>
          <el-table-column prop='desc' label='描述'></el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button @click="showGroup(scope.row)" type="success" size="small">查看</el-button>
              <el-button @click="deleteGroup(scope.row.id)" type="danger" size="small" disabled>删除</el-button>
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
    <el-dialog :visible.sync="addGroup">
      <add-group @formdata="addGroupSubmit"></add-group>
    </el-dialog>
    <el-dialog :visible.sync="viewGroup" @close="closeViewForm">
      <view-group :rowdata="rowdata"></view-group>
    </el-dialog>
  </div>
</template>

<script>
import { getGroup, postGroup, deleteGroup } from 'api/user'
import { LIMIT, pagesize, pageformat } from '@/config'
import addGroup from '../components/addgroup.vue'
import viewGroup from './components/viewgroup.vue'

export default {
  components: { addGroup, viewGroup },
  data() {
    return {
      tableData: [],
      tabletotal: 0,
      currentPage: 1,
      listQuery: {
        limit: LIMIT,
        offset: '',
        name: ''
      },
      pagesize: pagesize,
      pageformat: pageformat,
      addGroup: false,
      viewGroup: false,
      rowdata: ''
    }
  },

  created() {
    this.fetchData()
  },

  methods: {
    fetchData() {
      getGroup(this.listQuery).then(response => {
        this.tableData = response.data.results
        this.tabletotal = response.data.count
      })
    },
    addGroupSubmit(formdata) {
      postGroup(formdata).then(response => {
        this.$message({
          message: '恭喜你，添加成功',
          type: 'success'
        })
        this.fetchData()
        this.addGroup = false
      }).catch(error => {
        this.$message.error('添加失败')
        console.log(error)
      })
    },
    deleteGroup(id) {
      deleteGroup(id).then(response => {
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
    showGroup(row) {
      this.viewGroup = true
      this.rowdata = row
    },
    closeViewForm() {
      this.rowdata = {}
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

</style>
