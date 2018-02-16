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
          <el-table-column type="expand">
            <template slot-scope="props">
              <el-form label-position="left" inline class="table-expand">
                <el-form-item label="测试人员" prop="test_user">
                  <span>{{ props.row.test_user }}</span>
                </el-form-item>
                <el-form-item label="分配给" prop="action_user">
                  <span>{{ props.row.action_user }}</span>
                </el-form-item>
                <el-form-item label="测试时间" prop="test_time">
                  <span>{{ props.row.test_time }}</span>
                </el-form-item>
                <el-form-item label="关闭时间" prop="end_time">
                  <span>{{ props.row.end_time }}</span>
                </el-form-item>
                <el-form-item label="描述" prop="desc">
                  <span>{{ props.row.desc }}</span>
                </el-form-item>
              </el-form>
            </template>
          </el-table-column>
          <el-table-column prop='id' label='编号'></el-table-column>
          <el-table-column prop='name' label='名称'></el-table-column>
          <el-table-column prop='degree' label='严重程度'>
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper" style="text-align: center; color: rgb(0,0,0)">
                <el-rate
                  v-model="scope.row.degree"
                  :colors="['#99A9BF', '#F7BA2A', '#ff1425']"
                  disabled>
                </el-rate>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='nice' label='优先级'>
            <template slot-scope="scope">
              <div slot="reference">
                <el-tag size="mini">{{Bug_Nice[scope.row.nice]}}</el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='status' label='状态'>
            <template slot-scope="scope">
              <div slot="reference">
                <el-button size="mini" @click="changeStatus(scope.row)">{{Bug_Status[scope.row.status]}}</el-button>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='project' label='关联任务'>
            <template slot-scope="scope">
              <div slot="reference">
                <el-button type="text" @click="showProject(scope.row.project)">{{scope.row.project}}</el-button>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='test' label='关联test'></el-table-column>
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
    <el-dialog :visible.sync="addForm">
      <add-group @DialogStatus="getDialogStatus"></add-group>
    </el-dialog>
    <el-dialog :visible.sync="editForm" @close="closeEditForm">
      <edit-group :ruleForm="rowdata" @formdata="editGroupSubmit"></edit-group>
    </el-dialog>

    <el-dialog :visible.sync="showprojectForm">
      <show-project :ruleForm="project"></show-project>
    </el-dialog>

    <el-dialog :visible.sync="changestatusForm">
      <el-form>
        <el-form-item :model="bugdata" label="当前状态">
          <span>{{Bug_Status[bugdata.status]}}</span>
        </el-form-item>
        <el-form-item :model="bugdata" label="状态修改">
          <el-select v-model="bugdata.status" placeholder="请选择状态">
            <el-option v-for="(item,index) in Bug_Status" :key="item.id" :label="item" :value="index"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button @click="UpdateStatus" type="primary" icon="el-icon-check"></el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import { getBugManager, putBugManager, patchBugManager, deleteBugManager, getProject } from '@/api/project'
import { LIMIT, pagesize, pageformat } from '@/config'
import addGroup from './components/addbug.vue'
import editGroup from './components/editbug.vue'
import showProject from './components/showproject.vue'

export default {
  components: {
    addGroup, editGroup, getProject, showProject
  },
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
      rowdata: {},
      Bug_Nice: {
        0: '低',
        1: '中',
        2: '高'
      },
      Bug_Status: {
        0: '新建',
        1: '打开',
        2: '关闭',
        3: '已修复',
        4: '暂不处理',
        5: '重新打开'
      },
      showprojectForm: false,
      changestatusForm: false,
      project: '',
      bugdata: {
        id: '',
        status: ''
      }
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
      getBugManager(parms).then(response => {
        this.tableData = response.data.results
        this.tabletotal = response.data.count
      })
    },
    getDialogStatus(data) {
      this.addForm = data
      setTimeout(this.fetchData, 1000)
    },
    editGroupSubmit(formdata) {
      putBugManager(this.rowdata.id, formdata).then(response => {
        this.$message({
          message: '恭喜你，更新成功',
          type: 'success'
        })
        this.fetchData()
        this.editForm = false
      }).catch(error => {
        this.$message.error('更新失败')
        console.log(error)
      })
    },
    deleteGroup(id) {
      deleteBugManager(id).then(response => {
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
    closeEditForm() {
      this.fetchData()
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
    showProject(pid) {
      this.showprojectForm = true
      const query = {
        pid: pid
      }
      getProject(query).then(response => {
        this.project = response.data[0]
      })
    },
    changeStatus(row) {
      this.bugdata.id = row.id
      this.bugdata.status = row.status
      this.changestatusForm = true
    },
    UpdateStatus() {
      patchBugManager(this.bugdata.id, this.bugdata).then(() => {
        this.changestatusForm = false
        this.fetchData()
      })
    }
  }
}
</script>

<style lang='scss'>

</style>
