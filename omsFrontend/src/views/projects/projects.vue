<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <div class="head-lavel">
        <div class="table-button">
          <router-link :to="'addproject'">
            <el-button type="primary" icon="el-icon-plus">新建</el-button>
          </router-link>
          <el-button-group>
            <el-button type="danger" plain @click="showAllTicket">全部</el-button>
            <el-button type="success" plain @click="showMeTicket">我的工单</el-button>
          </el-button-group>
        </div>
        <div class="table-search">
          <el-select v-model="listQuery.status" placeholder="请选择状态筛选" clearable @change="changeStatus">
            <el-option
              v-for="item in Object.keys(Status_Text)"
              :key="item"
              :label="Status_Text[item]"
              :value="item">
            </el-option>
          </el-select>
          <el-date-picker
            v-model="selectcreatedate"
            type="daterange"
            range-separator="至"
            start-placeholder="创建日期"
            end-placeholder="结束日期"
            @change="selectCreatedate"
            :picker-options="pickerOptions">
          </el-date-picker>
          <el-date-picker
            v-model="selectupdatedate"
            type="daterange"
            range-separator="至"
            start-placeholder="修改日期"
            end-placeholder="结束日期"
            @change="selectUpdatedate"
            :picker-options="pickerOptions">
          </el-date-picker>
          <el-input style="width: 200px;" class="filter-item" placeholder="编号、标题、内容或类型"
                    @keyup.enter.native="searchClick"
                    v-model="listQuery.search"></el-input>
          <el-button class="filter-item" type="primary" icon="search" @click="searchClick">搜索</el-button>
        </div>
      </div>
      <div>
        <el-table :data="tableData" border style="width: 100%" @sort-change="handleSortChange">
          <el-table-column prop='pid' label='编号'>
            <template slot-scope="scope">
              <router-link :to="'viewproject/' + scope.row.id">
                <a style="color: #257cff">{{scope.row.pid}}</a>
              </router-link>
            </template>
          </el-table-column>
          <el-table-column prop='name' label='名称'></el-table-column>
          <el-table-column prop='type' label='类型'></el-table-column>
          <el-table-column v-if="role==='super'" prop='is_public' label='是否公开' width="80">
            <template slot-scope="scope">
              <a>{{scope.row.is_public}}</a>
            </template>
          </el-table-column>
          <el-table-column prop='level' label='等级' sortable="custom">
            <template slot-scope="scope">
              <div slot="reference" style="text-align: center; color: rgb(0,0,0)">
                <el-rate
                  v-model="scope.row.level"
                  :colors="['#99A9BF', '#F7BA2A', '#ff1425']"
                  disabled>
                </el-rate>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='status' label='状态' width="80">
            <template slot-scope="scope">
              <div slot="reference">
                <el-tag size="mini" :type="Status_Color[scope.row.status]">
                  {{Status_Text[scope.row.status]}}
                </el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='task_complete' label='任务进度' sortable="custom" width="120">
            <template slot-scope="scope">
              <div slot="reference">
                {{scope.row.task_complete}}%
                <el-tooltip class="item" effect="dark" content="更新任务进度" placement="top">
                  <el-button @click="updateTaskComplete(scope.row)" type="text" icon="el-icon-edit"
                             class="modifychange"></el-button>
                </el-tooltip>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='test_complete' label='测试进度' sortable="custom" width="120">
            <template slot-scope="scope">
              <div slot="reference">
                {{scope.row.test_complete}}%
                <el-tooltip class="item" effect="dark" content="更新测试进度" placement="top">
                  <el-button @click="updateTestComplete(scope.row)" type="text" icon="el-icon-edit"
                             class="modifychange"></el-button>
                </el-tooltip>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='demand' label='关联需求'></el-table-column>
          <el-table-column prop='action_user' label='指派人' width="100">
            <template slot-scope="scope">
              <div slot="reference">
                <el-tag size="mini" v-for="item in scope.row.action_user" :key="item">
                  {{item}}
                </el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='create_time' label='创建时间' sortable="custom">
            <template slot-scope="scope">
              <div slot="reference" style="text-align: center; color: rgb(0,0,0)">
                <span>{{scope.row.create_time | parseDate}}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='update_time' label='修改时间' sortable="custom">
            <template slot-scope="scope">
              <div slot="reference" style="text-align: center; color: rgb(0,0,0)">
                <span>{{scope.row.update_time | parseDate}}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150">
            <template slot-scope="scope">
              <router-link :to="'editproject/' + scope.row.id">
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
        <el-form-item label="完成百分比" prop="task_complete">
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

    <el-dialog title="更新测试进度" :visible.sync="TestCompleteForm">
      <el-form label-width="90px">
        <el-form-item :model="updateform" label="完成百分比">
          <el-slider
            style="margin-right: 50px"
            v-model="updateform.test_complete"
            :step="10">
          </el-slider>
          <a>{{updateform.test_complete}}%</a>
        </el-form-item>
        <el-form-item>
          <el-button @click="changeComplete" type="success" size="mini">确定</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import { getProject, patchProject, deleteProject } from '@/api/project'
import { LIMIT, pagesize, pageformat } from '@/config'
import { mapGetters } from 'vuex'
import formatDate from '@/utils/dateformat'

export default {
  components: {},
  data() {
    return {
      tableData: [],
      tabletotal: 0,
      currentPage: 1,
      pagesize: pagesize,
      pageformat: pageformat,
      Status_Text: {
        1: '已指派',
        2: '处理中',
        3: '待测试',
        4: '测试中',
        5: '已测试',
        6: '待上线',
        7: '已上线'
      },
      Status_Color: {
        1: '',
        2: '',
        3: '',
        4: '',
        5: '',
        6: '',
        7: 'info'
      },
      listQuery: {
        limit: LIMIT,
        offset: '',
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
      },
      selectcreatedate: '',
      selectupdatedate: '',
      pickerOptions: {
        shortcuts: [{
          text: '最近一周',
          onClick(picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '最近一个月',
          onClick(picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '最近三个月',
          onClick(picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
            picker.$emit('pick', [start, end])
          }
        }]
      }
    }
  },

  computed: {
    ...mapGetters([
      'role'
    ])
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
      this.listQuery.search = ''
      this.listQuery.status = ''
      this.fetchData()
    },
    showMeTicket() {
      this.listQuery.action_user__username = localStorage.getItem('username')
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
    },
    selectCreatedate(val) {
      if (val) {
        this.listQuery.create_date_0 = formatDate(val[0], 'YYYY-MM-DD')
        this.listQuery.create_date_1 = formatDate(val[1], 'YYYY-MM-DD')
      } else {
        this.listQuery.create_date_0 = ''
        this.listQuery.create_date_1 = ''
      }
      this.fetchData()
    },
    selectUpdatedate(val) {
      if (val) {
        this.listQuery.update_date_0 = formatDate(val[0], 'YYYY-MM-DD')
        this.listQuery.update_date_1 = formatDate(val[1], 'YYYY-MM-DD')
      } else {
        this.listQuery.update_date_0 = ''
        this.listQuery.update_date_1 = ''
      }
      this.fetchData()
    }
  }
}
</script>

<style lang='scss'>
  .modifychange {
    margin: 5px;
  }
</style>
