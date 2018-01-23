<template>
  <div class="components-container" style='height:100vh'>
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card>
          <div slot="header">
            <a class="jobname">{{jobs.name}}</a>
          </div>
          <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px">
            <!--<el-form-item label="发布环境" prop="env">-->
            <!--<el-select v-model="ruleForm.env" placeholder="请选择发布环境" @change="selectEnv">-->
            <!--<el-option v-for="item in envs" :key="item.id" :value="item.name"></el-option>-->
            <!--</el-select>-->
            <!--</el-form-item>-->
            <!--<el-form-item label="发布主机" prop="hosts">-->
            <!--<el-select v-model="ruleForm.deploy_hosts" multiple placeholder="请选择发布主机">-->
            <!--<el-option v-for="item in jobs.deploy_hosts" :key="item" :value="item"></el-option>-->
            <!--</el-select>-->
            <!--</el-form-item>-->
            <el-form-item label="代码地址">
              <el-input v-model="jobs.code_url" disabled></el-input>
            </el-form-item>
            <el-form-item label="发布版本" prop="version">
              <el-input v-model="ruleForm.version"></el-input>
            </el-form-item>
            <el-form-item label="发布路径" prop="deploy_path">
              <el-input v-model="jobs.deploy_path" disabled></el-input>
            </el-form-item>
            <el-form-item label="更新内容" prop="content">
              <el-input v-model="ruleForm.content" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="submitForm('ruleForm')">开始构建</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
      <el-col :span="16">
        <el-card>
          <div slot="header">
            <a class="jobname">发布记录</a>
            <el-button style="padding: 3px 0;margin-left: 20px" type="danger" plain icon="el-icon-refresh"
                       @click="fetchDeployJobData">刷新
            </el-button>
          </div>
          <div>
            <el-table :data='tableData' @selection-change="handleSelectionChange" style="width: 100%">
              <el-table-column type="selection" v-if="role==='super'"></el-table-column>
              <el-table-column prop='version' label='发布版本'>
                <template slot-scope="scope">
                  <div slot="reference">
                    <el-tooltip :content="scope.row.content" placement="top">
                      <a style="color: #257cff">{{scope.row.version}}</a>
                    </el-tooltip>
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
                             :disabled="!scope.row.result">查看结果
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
                layout="prev, pager, next, sizes"
                :total="tabletotal">
              </el-pagination>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

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
import { getJob, getDeployenv, getDeployJob, postDeployJob, deleteDeployJob } from '@/api/job'
import { LIMIT } from '@/config'
import { mapGetters } from 'vuex'
import { postSendmessage } from '@/api/tool'

export default {
  components: {},

  data() {
    return {
      route_path: this.$route.path.split('/'),
      job_id: this.$route.params.job_id,
      ruleForm: {
        job: '',
        env: '',
        deploy_hosts: [],
        version: '',
        deploy_path: '',
        content: '',
        action_user: localStorage.getItem('username')
      },
      rules: {
        hosts: [
          { required: true, type: 'array', message: '请输入正确的内容', trigger: 'blur' }
        ],
        version: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        content: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ]
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
        search: '',
        job__name: ''
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
      butstatus: false,
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
    this.fetchJobData()
  },
  methods: {
    fetchJobData() {
      const parms = null
      getJob(parms, this.job_id).then(response => {
        this.jobs = response.data
        this.ruleForm.job = this.jobs.name
        this.ruleForm.repo_cmd = this.jobs.repo_cmd
        this.ruleForm.deploy_hosts = this.jobs.deploy_hosts
        this.ruleForm.deploy_path = this.jobs.deploy_path
        this.listQuery.job__name = this.jobs.name
        this.fetchDeployJobData()
        // this.fetchJobenvData(this.jobs.name)
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
        const job_status = this.tableData.map(function(item) {
          return item.deploy_status
        })
        if (job_status.indexOf('deploy') > -1) {
          this.check_job_status = setInterval(() => {
            console.log('check job_status 3/s')
            this.fetchDeployJobData()
          }, 3000)
        } else {
          clearInterval(this.check_job_status)
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
    submitForm(formdata) {
      this.$refs[formdata].validate((valid) => {
        if (valid) {
          this.ruleForm.deploy_hosts = this.ruleForm.deploy_hosts.join()
          postDeployJob(this.ruleForm).then(response => {
            console.log(response.data.j_id)
            this.$message({
              message: '构建成功，系统正在玩命发布中 ...',
              type: 'success'
            })
            this.fetchDeployJobData()
            const messageForm = {
              action_user: 'ITDept_SkypeID',
              title: `【${this.ruleForm.job}】更新`,
              message: `版本号: ${this.ruleForm.version}\n更新内容: ${this.ruleForm.content}\n操作人: ${this.ruleForm.action_user}\n发布地址：${window.location.href}`
            }
            postSendmessage(messageForm)
            this.resetForm('ruleForm')
          }).catch(error => {
            this.$message.error('构建失败，请检查参数是否正确！')
            console.log(error)
          })
        } else {
          console.log('error submit!!')
          return false
        }
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
    },
    showJobResult(row) {
      this.showresult = true
      const data = (new Function('return ' + row))()
      const a = []
      Object.keys(data).map(function(k) {
        a.push({ 'host': k, 'data': data[k] })
      })
      this.job_results = a
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
