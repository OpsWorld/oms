<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <div class="head-lavel">
        <div class="table-button">
          <router-link :to="'addopsdemand'">
            <el-button type="primary" icon="el-icon-plus">新建</el-button>
          </router-link>
          <el-button type="danger" size="small" @click="showAll">全部</el-button>
          <el-radio-group v-model="listQuery.status" @change="changeStatus" style="margin-left: 20px">
            <el-radio v-for="item in Object.keys(STATUS_TEXT)" :key="item" :label="item">{{STATUS_TEXT[item]}}
            </el-radio>
          </el-radio-group>
        </div>
        <div class="table-search">
          <el-input style="width: 180px;" placeholder="编号、标题、内容"
                    @keyup.enter.native="searchClick"
                    v-model="listQuery.search">
            <i class="el-icon-search el-input__icon" slot="suffix" @click="searchClick"></i>
          </el-input>
        </div>
      </div>
      <div>
        <el-table :data="tableData" border style="width: 100%" @sort-change="handleSortChange">
          <el-table-column label="任务" type="expand" width="50">
            <template slot-scope="scope">
              <el-table :data="scope.row.projectData" border stripe style="width: 100%">
                <el-table-column type="index" width="50"></el-table-column>
                <el-table-column prop="pid" label="编号"></el-table-column>
                <el-table-column prop="name" label="任务概要"></el-table-column>
                <el-table-column prop="action_user" label="负责人"></el-table-column>
                <el-table-column prop="start_time" label="开始日期" sortable></el-table-column>
                <el-table-column prop="end_time" label="完成日期"></el-table-column>
                <el-table-column prop="status" label="状态">
                  <template slot-scope="props">
                    <div slot="reference">
                      <el-tag size="mini" :type="STATUS_COLOR[props.row.status]">
                        {{STATUS_TEXT[props.row.status]}}
                      </el-tag>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column prop="task_complete" label="进度" sortable>
                  <template slot-scope="props">
                    <div slot="reference" class="name-wrapper">
                      {{props.row.task_complete}}%
                      <el-tooltip class="item" effect="dark" content="更新任务进度" placement="top">
                        <el-button v-if="scope.row.status==0&&props.row.task_complete!=100"
                                   @click="updateTaskComplete(props.row)" type="text"
                                   icon="el-icon-edit"></el-button>
                      </el-tooltip>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="230">
                  <template slot-scope="props">
                    <el-button-group>
                      <el-button type="success" plain size="mini" @click=showProject(props.row)>详情</el-button>
                      <el-button type="primary" plain size="mini" @click=updateProjectContent2(props.row)>完成情况
                      </el-button>
                      <el-button type="danger" plain size="mini" @click=deleteProject(props.row)>删除</el-button>
                    </el-button-group>
                  </template>
                </el-table-column>
              </el-table>
            </template>
          </el-table-column>
          <el-table-column prop='pid' label='编号'>
            <!--<template slot-scope="scope">-->
            <!--<div slot="reference">-->
            <!--<router-link :to="'viewopsdemand/' + scope.row.id">-->
            <!--<a style="color: #257cff">{{scope.row.pid}}</a>-->
            <!--</router-link>-->
            <!--</div>-->
            <!--</template>-->
          </el-table-column>
          <el-table-column prop='name' label='名称'></el-table-column>
          <el-table-column prop='start_time' label='开始日期' sortable="custom"></el-table-column>
          <el-table-column prop='end_time' label='结束日期'></el-table-column>
          <el-table-column prop='status' label='状态' sortable="custom">
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper">
                <el-tag size="mini" :type="STATUS_COLOR[scope.row.status]">
                  {{STATUS_TEXT[scope.row.status]}}
                </el-tag>
                <el-tooltip class="item" effect="dark" content="更改状态" placement="top">
                  <el-button v-if="scope.row.status!=1" type="text" icon="el-icon-edit" class="modifychange"
                             @click="updateDemand(scope.row.id)"></el-button>
                </el-tooltip>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='task_complete' label='项目进度' sortable="custom">
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper">
                {{scope.row.task_complete}}%
              </div>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="230">
            <template slot-scope="scope">
              <el-button-group>
                <router-link :to="'editopsdemand/' + scope.row.id">
                  <el-button type="success" size="mini">修改</el-button>
                </router-link>
                <el-button type="primary" size="mini" @click="addProject(scope.row)">增加任务</el-button>
                <el-button type="danger" size="mini" @click="deleteDemand(scope.row.id)">删除</el-button>
              </el-button-group>
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

    <el-dialog :visible.sync="addProForm">
      <add-project :demand="demand_id" @DialogStatus="getDialogStatus"></add-project>
    </el-dialog>

    <el-dialog title="任务详情" :visible.sync="showProForm">
      <el-form label-width="100px">
        <el-form-item label="内容" prop="status">
          <div>{{proContent.content1}}</div>
        </el-form-item>
        <el-form-item label="实际完成情况" prop="status">
          <div>{{proContent.content2}}</div>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-dialog :visible.sync="demandstatusForm">
      <el-form label-width="90px">
        <el-form-item label="更改状态" prop="status">
          <el-radio-group v-model="updateform.status">
            <el-radio v-for="item in Object.keys(STATUS_TEXT)" :key="item" :label="item">{{STATUS_TEXT[item]}}
            </el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="changeDemandStatus">确 定</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-dialog title="更新任务进度" :visible.sync="taskCompleteForm">
      <el-form label-width="90px">
        <el-form-item label="完成百分比" prop="task_complete">
          <el-slider
            style="margin-right: 50px"
            v-model="updatetaskform.task_complete"
            :step="10">
          </el-slider>
          <a>{{updatetaskform.task_complete}}%</a>
        </el-form-item>
        <el-form-item>
          <el-button @click="changeComplete" type="success" size="mini">确定</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-dialog title="更新完成情况" :visible.sync="content2ProForm">
      <el-form label-width="100px">
        <el-form-item label="实际完成情况" prop="content2">
          <el-input v-model="updatecontent2form.content2" type="textarea"
                    :autosize="{ minRows: 5, maxRows: 10}"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button @click="changeProjectContent2" type="success" size="mini">确定</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import {
  getDemandManager,
  deleteDemandManager,
  patchDemandManager,
  getProject,
  deleteProject,
  patchProject
} from '@/api/optask'
import { LIMIT, pagesize, pageformat } from '@/config'
import addProject from './components/addproject.vue'

export default {
  components: { addProject },
  data() {
    return {
      tableData: [],
      tabletotal: 0,
      currentPage: 1,
      pagesize: pagesize,
      pageformat: pageformat,
      STATUS_TEXT: { 0: '进行中', 1: '已完成', 2: '搁置' },
      STATUS_COLOR: { 0: 'primary', 1: 'success', 2: 'warning' },
      listQuery: {
        limit: LIMIT,
        offset: '',
        pid: '',
        status: '',
        create_user__username: '',
        search: '',
        ordering: ''
      },
      addProForm: false,
      showProForm: false,
      demand_id: '',
      proContent: {},
      demandstatusForm: false,
      taskCompleteForm: false,
      updateform: {
        id: '',
        status: '1'
      },
      updatetaskform: {
        id: '',
        task_complete: ''
      },
      updatecontent2form: {
        id: '',
        content2: ''
      },
      content2ProForm: false
    }
  },
  created() {
    this.fetchData()
  },

  methods: {
    fetchData() {
      getDemandManager(this.listQuery).then(response => {
        this.tableData = response.data.results
        this.tabletotal = response.data.count
        this.tableData.map(function(item) {
          const parmas = {
            demand__id: item.id
          }
          getProject(parmas).then(res => {
            item.projectData = res.data
            item.task_complete = 0
            for (const pp of res.data) {
              item.task_complete += Math.round(pp.task_complete / res.data.length)
            }
            const data = {
              task_complete: item.task_complete
            }
            patchDemandManager(item.id, data)
          })
        })
      })
    },
    showAll() {
      this.listQuery = {
        limit: LIMIT,
        offset: '',
        pid: '',
        status: '',
        create_user__username: '',
        search: '',
        ordering: ''
      }
      this.fetchData()
    },
    getDialogStatus(data) {
      this.addProForm = data
      this.fetchData()
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
    changeStatus() {
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
    deleteDemand(id) {
      deleteDemandManager(id).then(response => {
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
    addProject(row) {
      this.addProForm = true
      this.demand_id = row.id
    },
    showProject(row) {
      this.showProForm = true
      this.proContent = row
    },
    deleteProject(row) {
      deleteProject(row.id).then(response => {
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
    updateDemand(id) {
      this.demandstatusForm = true
      this.updateform.id = id
    },
    changeDemandStatus() {
      patchDemandManager(this.updateform.id, this.updateform).then(() => {
        this.demandstatusForm = false
        this.fetchData()
      })
    },
    updateTaskComplete(row) {
      this.taskCompleteForm = true
      this.updatetaskform.id = row.id
      this.updatetaskform.task_complete = row.task_complete
    },
    changeComplete() {
      if (this.updatetaskform.task_complete === 100) {
        this.updatetaskform.status = 1
      }
      patchProject(this.updatetaskform.id, this.updatetaskform).then(response => {
        this.fetchData()
        this.taskCompleteForm = false
      })
    },
    updateProjectContent2(row) {
      this.content2ProForm = true
      this.updatecontent2form.id = row.id
      this.updatecontent2form.content2 = row.content2
    },
    changeProjectContent2() {
      patchProject(this.updatecontent2form.id, this.updatecontent2form).then(response => {
        this.content2ProForm = false
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
