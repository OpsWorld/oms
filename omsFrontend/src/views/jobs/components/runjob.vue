<template>
  <div class="components-container" style='height:100vh'>
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card>
          <div slot="header">
            <a class="jobname">{{jobs.name}}</a>
          </div>
          <el-form :model="ruleForm" ref="ruleForm" label-width="100px">
            <el-form-item label="发布环境" prop="env">
              <el-select v-model="ruleForm.env" placeholder="请选择发布环境" @change="selectEnv">
                <el-option v-for="item in envs" :key="item.id" :value="item.name"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="发布主机" prop="hosts">
              <el-select v-model="ruleForm.hosts" multiple placeholder="请选择发布主机">
                <el-option v-for="item in hosts" :key="item.id" :value="item"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="代码地址">
              <el-input v-model="jobs.code_url" disabled></el-input>
            </el-form-item>
            <el-form-item label="发布版本" prop="version">
              <el-select v-model="ruleForm.version" placeholder="请选择发布版本">
                <el-option v-for="item in versions" :key="item.id" :value="item"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="发布路径">
              <el-input v-model="deploy_path" disabled></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary">开始构建</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
      <el-col :span="16">
        <el-card>
          <div slot="header">
            <a class="jobname">发布记录</a>
          </div>
          <div>
            <el-table :data='tableData' style="width: 100%">
              <el-table-column type="index" width="50"></el-table-column>
              <el-table-column prop='j_id' label='任务id'></el-table-column>
              <el-table-column prop='env' label='发布环境'></el-table-column>
              <el-table-column prop='version' label='发布版本'></el-table-column>
              <el-table-column prop='deploy_status' label='发布状态' sortable>
                <template slot-scope="scope">
                  <div slot="reference">
                    <el-tag :type="DEPLOY_STATUS[scope.row.deploy_status].type">
                      {{DEPLOY_STATUS[scope.row.deploy_status].text}}
                    </el-tag>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop='action_user' label='发布人'></el-table-column>
              <el-table-column prop='create_time' label='发布时间' sortable>
                <template slot-scope="scope">
                  <div slot="reference">
                    {{scope.row.create_time | formatTime}}
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
              layout="prev, pager, next, sizes"
              :total="tabletotal">
            </el-pagination>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>
<script>
import { getJob, getDeployenv, getDeployJob } from '@/api/job'
import { LIMIT } from '@/config'

export default {
  components: {},

  data() {
    return {
      route_path: this.$route.path.split('/'),
      job_id: this.$route.params.job_id,
      ruleForm: {
        job: '',
        env: '',
        hosts: [],
        version: 'HEAD',
        action_user: localStorage.getItem('username')
      },
      envs: [],
      deploy_envs: [],
      hosts: [],
      versions: [],
      jobs: {},
      deploy_path: '',
      currentPage: 1,
      listQuery: {
        limit: LIMIT,
        offset: '',
        search: ''
      },
      pagesize: [10, 25, 50, 100],
      tableData: [],
      tabletotal: 0,
      DEPLOY_STATUS: {
        'noaction': { 'text': '未执行', 'type': 'info' },
        'deploy': { 'text': '发布中', 'type': 'primary' },
        'success': { 'text': '发布成功', 'type': 'success' },
        'failed': { 'text': '发布失败', 'type': 'danger' }
      }
    }
  },

  created() {
    this.fetchJobData()
  },
  methods: {
    fetchJobData() {
      const parms = null
      getJob(parms, this.job_id).then(response => {
        this.jobs = response.data
        this.fetchJobenvData(this.jobs.name)
      })
    },
    fetchJobenvData(job) {
      const parms = {
        job__name: job
      }
      getDeployenv(parms).then(response => {
        this.envs = response.data
      })
    },
    selectEnv(env) {
      const selectenv = this.envs.filter(envs => envs.name === env)[0]
      this.hosts = selectenv.hosts
      this.deploy_path = selectenv.path
    },
    fetchDeployJobData() {
      getDeployJob(this.listQuery).then(response => {
        this.tableData = response.data.results
        this.tabletotal = response.data.count
      })
    }
  }
}
</script>

<style lang='scss'>
  .jobname {
    font-weight: 600;
    margin-left: 20px;
  }

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
