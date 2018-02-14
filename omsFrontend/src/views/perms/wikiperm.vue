<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <div class="head-lavel">
        <div class="table-button">
          <el-button type="primary" icon="el-icon-plus" @click="addForm=true">新建</el-button>
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
        <el-table :data='tableData' border style="width: 100%">
          <el-table-column prop='name' label='名称' sortable='custom'></el-table-column>
          <el-table-column prop='usergroups' label='用户组'></el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button @click="handleEdit(scope.row)" type="success" size="small">修改</el-button>
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
          :page-size="limit"
          :layout="pageformat"
          :total="tabletotal">
        </el-pagination>
      </div>
    </el-card>
    <el-dialog :visible.sync="addForm" @close="closeDialog">
      <add-group @DialogStatus="getDialogStatus"></add-group>
    </el-dialog>
    <el-dialog :visible.sync="editForm" @close="closeDialog">
      <edit-group :rowdata="rowdata" @DialogStatus="getDialogStatus"></edit-group>
    </el-dialog>
  </div>
</template>

<script>
import { getWikiPerm, deleteWikiPerm } from '@/api/perm'
import { LIMIT, pagesize, pageformat } from '@/config'
import addGroup from './components/addwikiperm.vue'
import editGroup from './components/editwikiperm.vue'

export default {
  components: { addGroup, editGroup },
  data() {
    return {
      tableData: [],
      tabletotal: 0,
      searchdata: '',
      currentPage: 1,
      limit: LIMIT,
      offset: '',
      pagesize: pagesize,
      pageformat: pageformat,
      addForm: false,
      editForm: false,
      rowdata: {}
    }
  },

  created() {
    this.fetchData()
  },

  methods: {
    fetchData() {
      const parms = {
        limit: this.limit,
        offset: this.offset,
        name__contains: this.searchdata
      }
      getWikiPerm(parms).then(response => {
        this.tableData = response.data.results
        this.tabletotal = response.data.count
      })
    },
    getDialogStatus(data) {
      this.editForm = data
      this.addForm = data
      setTimeout(this.fetchData, 1000)
    },
    deleteGroup(id) {
      deleteWikiPerm(id).then(response => {
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
    handleEdit(row) {
      this.editForm = true
      this.rowdata = row
    },
    searchClick() {
      this.fetchData()
    },
    handleSizeChange(val) {
      this.limit = val
      this.fetchData()
    },
    handleCurrentChange(val) {
      this.offset = (val - 1) * LIMIT
      this.fetchData()
    },
    closeDialog() {
      this.fetchData()
    }
  }
}
</script>

<style lang='scss'>

</style>
