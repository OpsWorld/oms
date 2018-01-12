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
              <el-input v-model="ruleForm.version"></el-input>
              <!--<el-select v-model="ruleForm.version" placeholder="请选择发布版本">-->
              <!--<el-option v-for="item in versions" :key="item.id" :value="item"></el-option>-->
              <!--</el-select>-->
              <a class="tips">Tip：HEAD 代表最新版本号，若要发布其他版本，请改为其他版本号</a>
            </el-form-item>
            <el-form-item label="发布路径" prop="deploy_path">
              <el-input v-model="ruleForm.deploy_path" disabled></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="submitForm(ruleForm)">开始构建</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
      <el-col :span="16">
        <el-card>
          <div slot="header">
            <a class="jobname">发布记录</a>
            <el-button style="padding: 3px 0;margin-left: 20px" type="danger" plain icon="el-icon-refresh">刷新状态
            </el-button>
          </div>
          <div>
            <el-table :data='tableData' @selection-change="handleSelectionChange" style="width: 100%">
              <el-table-column type="selection"></el-table-column>
              <el-table-column prop='id' label='id'></el-table-column>
              <el-table-column prop='env' label='发布环境'></el-table-column>
              <el-table-column prop='version' label='发布版本'></el-table-column>
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
          <div class="table-footer">

            <div class="table-button">
              <el-button type="danger" icon="delete" :disabled="butstatus" @click="deleteForm">删除记录</el-button>
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
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>
<script>
import { getJob, getDeployenv, getDeployJob, postDeployJob, deleteDeployJob } from '@/api/job'
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
        deploy_path: '',
        action_user: localStorage.getItem('username')
      },
      envs: [],
      deploy_envs: [],
      hosts: [],
      versions: [],
      jobs: {},
      currentPage: 1,
      listQuery: {
        limit: LIMIT,
        offset: '',
        search: ''
      },
      pagesize: [LIMIT, 25, 50, 100],
      tableData: [],
      tabletotal: 0,
      DEPLOY_STATUS: {
        deploy: { text: '发布中', type: 'primary', icon: 'el-icon-loading' },
        success: { text: '发布成功', type: 'success', icon: 'el-icon-success' },
        failed: { text: '发布失败', type: 'danger', icon: 'el-icon-error' }
      },
      selectId: [],
      butstatus: false
    }
  },

  created() {
    this.fetchJobData()
    this.fetchDeployJobData()
  },
  methods: {
    fetchJobData() {
      const parms = null
      getJob(parms, this.job_id).then(response => {
        this.jobs = response.data
        this.ruleForm.job = this.jobs.name
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
      this.ruleForm.deploy_path = selectenv.path
    },
    fetchDeployJobData() {
      getDeployJob(this.listQuery).then(response => {
        this.tableData = response.data
        this.tabletotal = response.data.length
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
    submitForm(formdata) {
      this.ruleForm.hosts = this.ruleForm.hosts.join()
      postDeployJob(formdata).then(response => {
        this.$message({
          message: '恭喜你，构建成功',
          type: 'success'
        })
        this.fetchDeployJobData()
        this.resetForm('ruleForm')
      }).catch(error => {
        this.$message.error('构建失败')
        this.resetForm('ruleForm')
        console.log(error)
      })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
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
      for (var i = 0, len = this.selectId.length; i < len; i++) {
        deleteDeployJob(this.selectId[i]).then(response => {
          delete this.selectId[i]
        })
      }
      setTimeout(this.fetchDeployJobData, 1000)
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
    padding: 10px 0;
    float: left;
  }

  .table-search {
    float: right;
    padding: 10px 0;
  }

  .table-pagination {
    padding: 10px 0;
    float: right;
  }
</style>
