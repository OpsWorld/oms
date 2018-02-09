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
        <el-table :data='tableData' border style="width: 100%">
          <el-table-column prop='name' label='商户号'></el-table-column>
          <el-table-column prop='m_id' label='公司名称' sortable='custom'></el-table-column>
          <el-table-column prop='platform' label='依附平台'></el-table-column>
          <el-table-column prop='domain' label='绑定域名'></el-table-column>
          <el-table-column prop='three' label='业务经理'></el-table-column>
          <!--<el-table-column label="操作">-->
          <!--<template slot-scope="scope">-->
          <!--<el-button @click="handleEdit(scope.row)" type="success" size="small">修改</el-button>-->
          <!--<el-button @click="deleteGroup(scope.row.id)" type="danger" size="small">删除</el-button>-->
          <!--</template>-->
          <!--</el-table-column>-->
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
    <!--<el-dialog :visible.sync="addForm">-->
    <!--<add-group @formdata="addGroupSubmit"></add-group>-->
    <!--</el-dialog>-->
    <!--<el-dialog :visible.sync="editForm">-->
    <!--<edit-group :rowdata="rowdata" @formdata="editGroupSubmit"></edit-group>-->
    <!--</el-dialog>-->
  </div>
</template>

<script>
import { getMerchant } from 'api/threeticket'
// import { getMerchant, postMerchant, putMerchant, deleteMerchant } from 'api/threeticket'
import { LIMIT, pagesize, pageformat } from '@/config'
import addGroup from './components/addMerchant.vue'
import editGroup from './components/editMerchant.vue'

export default {
  components: { addGroup, editGroup },
  data() {
    return {
      tableData: [],
      tabletotal: 0,
      searchdata: '',
      currentPage: 1,
      pagesize: pagesize,
      pageformat: pageformat,
      addForm: false,
      editForm: false,
      rowdata: {},
      listQuery: {
        limit: LIMIT,
        offset: '',
        name__contains: this.searchdata
      }
    }
  },

  created() {
    this.fetchData()
  },

  methods: {
    fetchData() {
      getMerchant(this.listQuery).then(response => {
        this.tableData = response.data.results
        this.tabletotal = response.data.count
      })
    },
    //    addGroupSubmit(formdata) {
    //      postMerchant(formdata).then(response => {
    //        this.$message({
    //          message: '恭喜你，添加成功',
    //          type: 'success'
    //        })
    //        this.fetchData()
    //        this.addForm = false
    //      }).catch(error => {
    //        this.$message.error('添加失败')
    //        console.log(error)
    //      })
    //    },
    //    editGroupSubmit(formdata) {
    //      putMerchant(this.rowdata.id, formdata).then(response => {
    //        this.$message({
    //          message: '恭喜你，更新成功',
    //          type: 'success'
    //        })
    //        this.fetchData()
    //        this.editForm = false
    //      }).catch(error => {
    //        this.$message.error('更新失败')
    //        console.log(error)
    //      })
    //    },
    //    deleteGroup(id) {
    //      deleteMerchant(id).then(response => {
    //        this.$message({
    //          message: '恭喜你，删除成功',
    //          type: 'success'
    //        })
    //        this.fetchData()
    //      }).catch(error => {
    //        this.$message.error('删除失败')
    //        console.log(error)
    //      })
    //    },
    //    handleEdit(row) {
    //      this.editForm = true
    //      this.rowdata = row
    //    },
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
