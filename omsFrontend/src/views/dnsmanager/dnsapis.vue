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
            v-model="listQuery.search"
            @keyup.enter.native="searchClick">
            <i class="el-icon-search el-input__icon" slot="suffix" @click="searchClick"></i>
          </el-input>
        </div>
      </div>
      <div>
        <el-table :data='tableData' border style="width: 100%">
          <el-table-column prop='name' label='名称' sortable></el-table-column>
          <el-table-column prop='key' label='key'></el-table-column>
          <el-table-column prop='secret' label='secret'></el-table-column>
          <el-table-column prop='desc' label='备注'></el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button type="success" size="small" @click="editGroup(scope.row)">修改</el-button>
              <el-button type="danger" size="small" @click="deleteGroup(scope.row.id)">删除</el-button>
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
      <el-form :model="ruleForm" ref="ruleForm" label-width="100px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="ruleForm.name"></el-input>
        </el-form-item>
        <el-form-item label="key" prop="key">
          <el-input v-model="ruleForm.key"></el-input>
        </el-form-item>
        <el-form-item label="secret" prop="secret">
          <el-input v-model="ruleForm.secret"></el-input>
        </el-form-item>
        <el-form-item label="备注" prop="desc">
          <el-input v-model="ruleForm.desc"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="addGroupSubmit('ruleForm')">立即创建</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-dialog :visible.sync="editForm">
      <el-form :model="rowdata" ref="rowdata" label-width="100px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="rowdata.name"></el-input>
        </el-form-item>
        <el-form-item label="key" prop="key">
          <el-input v-model="rowdata.key"></el-input>
        </el-form-item>
        <el-form-item label="secret" prop="secret">
          <el-input v-model="rowdata.secret"></el-input>
        </el-form-item>
        <el-form-item label="备注" prop="desc">
          <el-input v-model="rowdata.desc"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="editGroupSubmit('rowdata')">立即创建</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

  </div>
</template>

<script>
import { getDnsapiKey, postDnsapiKey, putDnsapiKey, deleteDnsapiKey } from 'api/dnsapi'
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
      listQuery: {
        limit: LIMIT,
        offset: '',
        search: ''
      },
      ruleForm: {
        name: '',
        key: '',
        secret: '',
        desc: ''
      },
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
      getDnsapiKey(this.listQuery).then(response => {
        this.tableData = response.data.results
        this.tabletotal = response.data.count
      })
    },
    addGroupSubmit() {
      postDnsapiKey(this.ruleForm).then(() => {
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
    editGroup(row) {
      this.rowdata = row
      this.editForm = true
    },
    editGroupSubmit() {
      putDnsapiKey(this.rowdata.id, this.rowdata).then(() => {
        this.$message({
          message: '恭喜你，修改成功',
          type: 'success'
        })
        this.fetchData()
        this.editForm = false
      }).catch(error => {
        this.$message.error('修改失败')
        console.log(error)
      })
    },
    deleteGroup(id) {
      deleteDnsapiKey(id).then(response => {
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
