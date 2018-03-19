<template>
  <div>
    <el-card>
      <div class="table-button">
        <a class="jobname">发布记录</a>
        <el-button style="padding: 3px 0;margin-left: 20px" type="danger" plain icon="el-icon-refresh"
                   @click="fetchDeployJobData">刷新
        </el-button>
      </div>
      <div class="table-search">
        <el-input
          placeholder="search"
          v-model="listQuery.search"
          @keyup.enter.native="searchClick">
          <i class="el-icon-search el-input__icon" slot="suffix" @click="searchClick"></i>
        </el-input>
      </div>
      <div>
        <el-table :data='tableData' @selection-change="handleSelectionChange" style="width: 100%">
          <el-table-column type="selection" v-if="role==='super'"></el-table-column>
          <el-table-column prop='version' label='发布版本'>
            <template slot-scope="scope">
              <div slot="reference">
                <el-popover
                  placement="top"
                  width="200"
                  trigger="hover"
                  :content="scope.row.content">
                  <el-button size="mini" slot="reference">{{scope.row.version}}</el-button>
                </el-popover>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='deploy_status' label='发布状态' sortable>
            <template slot-scope="scope">
              <div slot="reference">
                <el-button plain size="mini" :type="DEPLOY_STATUS[scope.row.deploy_status].type"
                           :icon="DEPLOY_STATUS[scope.row.deploy_status].icon">
                  {{DEPLOY_STATUS[scope.row.deploy_status].text}}
                </el-button>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='env' label='发布步骤'></el-table-column>
          <el-table-column prop='deploy_cmd_host' label='命令目标'></el-table-column>
          <el-table-column prop='action_user' label='发布人'></el-table-column>
          <el-table-column prop='create_time' label='发布时间' sortable>
            <template slot-scope="scope">
              <div slot="reference">
                {{scope.row.create_time | formatTime}}
              </div>
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button @click="showJobResult(scope.row.result)" type="success" size="mini"
                         :disabled="!scope.row.result">结果
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div class="table-footer">

        <div class="table-button" v-if="role==='super'">
          <el-button type="danger" icon="delete" :disabled="butstatus" @click="deleteForm">删除记录</el-button>
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

    <el-dialog :visible.sync="showresult">
      <div>
        <div class="runlog" v-for="item in job_results" :key="item.id">
          <p class="host">{{ item.host }}</p>
          <pre>{{ item.data }}</pre>
        </div>
      </div>
    </el-dialog>
  </div>
</template>
<script>
import {
  getDeployJob,
  deleteDeployJob,
  getUpdateJobsStatus
} from '@/api/job'
import { LIMIT, pagesize, pageformat } from '@/config'
import { mapGetters } from 'vuex'

export default {
  components: {},
  data() {
    return {
      job_id: this.$route.params.job_id,
      currentPage: 1,
      listQuery: {
        limit: LIMIT,
        offset: '',
        search: '',
        job__id: ''
      },
      pagesize: pagesize,
      pageformat: pageformat,
      tableData: [],
      tabletotal: 0,
      DEPLOY_STATUS: {
        deploy: { text: '发布中', type: 'primary', icon: 'el-icon-loading' },
        success: { text: '发布成功', type: 'success', icon: 'el-icon-success' },
        failed: { text: '发布失败', type: 'danger', icon: 'el-icon-error' }
      },
      selectId: [],
      butstatus: true,
      showresult: false,
      job_results: [],
      check_job_status: ''
    }
  },
  computed: {
    ...mapGetters([
      'role'
    ])
  },
  created() {
    this.fetchDeployJobData()
  },
  methods: {
    fetchDeployJobData() {
      this.listQuery.job__id = this.job_id
      getDeployJob(this.listQuery).then(response => {
        this.tableData = response.data.results
        this.tabletotal = response.data.count
        const job_status = this.tableData.map(function(item) {
          return item.deploy_status
        })
        if (job_status.indexOf('deploy') > -1) {
          this.check_job_status = setInterval(() => {
            const pramas = {
              job__id: this.job_id
            }
            getUpdateJobsStatus(pramas).then(response => {
              if (response.data.count === 0) {
                clearInterval(this.check_job_status)
                console.log('game over')
                this.$emit('updateStatus')
                this.fetchDeployJobData()
              } else {
                console.log('check job_status 3/s')
              }
            })
          }, 3000)
        } else {
          console.log('game over22')
          clearInterval(this.check_job_status)
          this.$emit('updateStatus')
        }
      })
    },
    handleSizeChange(val) {
      this.listQuery.limit = val
      this.fetchDeployJobData()
    },
    handleCurrentChange(val) {
      this.listQuery.offset = (val - 1) * LIMIT
      this.fetchDeployJobData()
    },
    handleSelectionChange(val) {
      this.selectId = []
      for (var i = 0, len = val.length; i < len; i++) {
        this.selectId.push(val[i].id)
      }
      if (this.selectId.length > 0) {
        this.butstatus = false
      } else {
        this.butstatus = true
      }
    },
    deleteForm() {
      clearInterval(this.check_job_status)
      for (var i = 0, len = this.selectId.length; i < len; i++) {
        deleteDeployJob(this.selectId[i]).then(response => {
          delete this.selectId[i]
        })
      }
      setTimeout(this.fetchDeployJobData, 1000)
    },
    showJobResult(row) {
      this.showresult = true
      const data = (new Function('return ' + row))()
      const a = []
      Object.keys(data).map(function(k) {
        a.push({ 'host': k, 'data': data[k] })
      })
      this.job_results = a
    },
    searchClick() {
      this.fetchDeployJobData()
    }
  }
}
</script>

<style lang='scss'>
  .jobname {
    font-weight: 600;
    margin-left: 20px;
  }
</style>
