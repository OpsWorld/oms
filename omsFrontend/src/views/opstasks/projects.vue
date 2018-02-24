<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <div class="head-lavel">
        <div class="table-button">
          <router-link :to="'addopsproject'">
            <el-button type="primary" icon="el-icon-plus">新建</el-button>
          </router-link>
          <el-button type="danger" plain size="small" @click="showAllTicket">全部</el-button>
          <el-button-group v-model="listQuery.status">
            <el-button plain size="mini" v-for="(item, index) in Object.keys(Project_Status).length" :key="index" @click="changeStatus(index)">
              {{Project_Status[index]}}
            </el-button>
          </el-button-group>
        </div>
        <div class="table-search">
          <el-input style="width: 160px;" class="filter-item" placeholder="编号" @keyup.enter.native="searchClick"
                    v-model="listQuery.pid"></el-input>
          <el-input style="width: 180px;" class="filter-item" placeholder="标题、内容或类型" @keyup.enter.native="searchClick"
                    v-model="listQuery.search"></el-input>
          <el-button class="filter-item" type="primary" icon="search" @click="searchClick">搜索</el-button>
        </div>
      </div>
      <div>
        <el-table :data="tableData" border style="width: 100%" @sort-change="handleSortChange">
          <el-table-column prop='pid' label='编号'>
            <template slot-scope="scope">
              <router-link :to="'viewopsproject/' + scope.row.id">
                <a style="color: #257cff">{{scope.row.pid}}</a>
              </router-link>
            </template>
          </el-table-column>
          <el-table-column prop='name' label='名称'></el-table-column>
          <el-table-column prop='type' label='类型' width="100"></el-table-column>
          <el-table-column prop='level' label='等级' sortable="custom">
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper" style="text-align: center; color: rgb(0,0,0)">
                <el-rate
                  v-model="scope.row.level"
                  :colors="['#99A9BF', '#F7BA2A', '#ff1425']"
                  disabled>
                </el-rate>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='status' label='状态'>
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper">
                <el-tag size="mini">
                  {{Project_Status[scope.row.status]}}
                </el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='task_complete' label='任务进度' sortable="custom">
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper">
                {{scope.row.task_complete}}%
                <el-tooltip class="item" effect="dark" content="更新任务进度" placement="top">
                  <el-button @click="updateTaskComplete(scope.row)" type="text" icon="el-icon-edit"
                             class="modifychange"></el-button>
                </el-tooltip>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='create_user' label='创建人' width="100"></el-table-column>
          <el-table-column prop='action_user' label='指派人' width="100">
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper">
                <el-tag size="mini" v-for="item in scope.row.action_user" :key="item">
                  {{item}}
                </el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='create_time' label='创建时间' sortable="custom">
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper" style="text-align: center; color: rgb(0,0,0)">
                <span>{{scope.row.create_time | parseDate}}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <router-link :to="'editopsproject/' + scope.row.id">
                <el-button type="success" size="small">修改</el-button>
              </router-link>
              <el-button type="danger" size="small" @click="deleteGroup(scope.row.id)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div class="table-footer">
        <div class="table-button">

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
      </div>
    </el-card>
    <el-dialog title="更新任务进度" :visible.sync="TaskCompleteForm">
      <el-form label-width="90px">
        <el-form-item :model="updateform" label="完成百分比">
          <el-slider
            style="margin-right: 50px"
            v-model="updateform.task_complete"
            :step="10">
          </el-slider>
          <a>{{updateform.task_complete}}%</a>
        </el-form-item>
        <el-form-item>
          <el-button @click="changeComplete" type="success" size="mini">确定</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import { getProject, patchProject, deleteProject } from '@/api/optask'
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
      Project_Status: {
        0: '未处理',
        1: '处理中',
        2: '已上线'
      },
      listQuery: {
        limit: LIMIT,
        offset: '',
        pid: '',
        status: '',
        create_user__username: '',
        action_user__username: '',
        search: '',
        ordering: ''
      },
      TaskCompleteForm: false,
      TestCompleteForm: false,
      updateform: {
        id: '',
        task_complete: '',
        test_complete: ''
      }
    }
  },
  created() {
    this.fetchData()
  },

  methods: {
    fetchData() {
      getProject(this.listQuery).then(response => {
        this.tableData = response.data.results
        this.tabletotal = response.data.count
      })
    },
    deleteGroup(id) {
      deleteProject(id).then(response => {
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
    },
    changeStatus(val) {
      this.listQuery.status = val
      this.fetchData()
    },
    showAllTicket() {
      this.listQuery.create_user__username = ''
      this.listQuery.action_user__username = ''
      this.listQuery.pid = ''
      this.listQuery.search = ''
      this.listQuery.status = ''
      this.fetchData()
    },
    handleSortChange(val) {
      if (val.order === 'ascending') {
        this.listQuery.ordering = val.prop
      } else if (val.order === 'descending') {
        this.listQuery.ordering = '-' + val.prop
      } else {
        this.listQuery.ordering = ''
      }
      this.fetchData()
    },
    updateTaskComplete(row) {
      this.TaskCompleteForm = true
      this.updateform.id = row.id
      this.updateform.status = row.status
      this.updateform.task_complete = row.task_complete
      this.updateform.test_complete = row.test_complete
    },
    updateTestComplete(row) {
      this.TestCompleteForm = true
      this.updateform.id = row.id
      this.updateform.status = row.status
      this.updateform.task_complete = row.task_complete
      this.updateform.test_complete = row.test_complete
    },
    changeComplete() {
      patchProject(this.updateform.id, this.updateform).then(response => {
        this.$message({
          type: 'success',
          message: '更新成功!'
        })
        this.TaskCompleteForm = this.TestCompleteForm = false
        this.fetchData()
      })
    }
  }
}
</script>

<style lang='scss'>
  .modifychange {
    margin: 5px;
  }
</style>
