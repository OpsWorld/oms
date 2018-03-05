<template>
  <div class="components-container" style='height:100vh'>
    <el-row :gutter="20">
      <el-col :span="8">

        <el-card>
          <div slot="header">
            <a class="jobname">【{{jobs.name}}】更新信息</a>
          </div>
          <el-form :model="versionForm" :rules="svnrules" ref="versionForm" label-width="90px">
            <el-form-item label="发布版本" prop="version">
              <el-input v-model="versionForm.version"></el-input>
            </el-form-item>
            <el-form-item label="更新内容" prop="content">
              <el-input v-model="versionForm.content" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
            </el-form-item>
          </el-form>
        </el-card>

        <el-card>
          <div slot="header">
            <a class="jobname">{{jobs.name}}</a>
          </div>

          <el-form :model="ruleForm" :rules="svnrules" ref="ruleForm" label-width="90px">
            <el-form-item label="发布步骤" prop="env">
              <el-select v-model="ruleForm.env" placeholder="请选择发布环境" @change="selectEnv">
                <el-option v-for="item in envs" :key="item.id" :value="item.name"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="发布命令" prop="deploy_cmd">
              <el-select v-model="ruleForm.deploy_cmd" placeholder="请选择发布命令">
                <el-option v-for="item in cmds" :key="item.id" :label="item.name"
                           :value="item.deploy_cmd"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="代码路径">
              <el-input v-model="jobs.code_url" disabled></el-input>
            </el-form-item>
            <el-form-item label="通知skype">
              <el-checkbox v-model="sendnotice">发送通知</el-checkbox>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="submitForm('versionForm')">svn更新</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
      <el-col :span="16">
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
import {
  getJob,
  getDeployJob,
  postDeployJob,
  deleteDeployJob,
  getUpdateJobsStatus,
  getDeployenv,
  getDeploycmd,
  postDeployVersion,
  putDeployVersion,
  getDeployVersion
} from '@/api/job'
import { LIMIT, pagesize, pageformat } from '@/config'
import { mapGetters } from 'vuex'
import { postSendmessage } from '@/api/tool'

export default {
  components: {},

  data() {
    return {
      route_path: this.$route.path.split('/'),
      job_id: this.$route.params.job_id,
      versionForm: {
        job: '',
        version: '',
        content: ''
      },
      ruleForm: {
        job: '',
        env: '',
        deploy_hosts: [],
        deploy_cmd: '',
        action_user: localStorage.getItem('username')
      },
      svnrules: {
        version: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        content: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ]
      },
      envs: [],
      cmds: [],
      jobs: {},
      currentPage: 1,
      listQuery: {
        limit: LIMIT,
        offset: '',
        search: '',
        job__name: ''
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
      check_job_status: '',
      sendnotice: true,
      hasversion: false
    }
  },
  computed: {
    ...mapGetters([
      'role'
    ])
  },
  created() {
    this.fetchJobData()
    this.fetchJobenvData()
  },
  methods: {
    fetchJobData() {
      const parmas = null
      getJob(parmas, this.job_id).then(response => {
        this.jobs = response.data
        this.ruleForm.job = this.listQuery.job__name = this.jobs.name
        this.fetchDeployJobData()
        this.fetchDeployversionData()
      })
    },
    fetchJobenvData() {
      const parmas = {
        job__id: this.job_id
      }
      getDeployenv(parmas).then(response => {
        this.envs = response.data
      })
    },
    fetchDeploycmdData(env) {
      const parmas = {
        env__id: env
      }
      getDeploycmd(parmas).then(response => {
        this.cmds = response.data
      })
    },
    fetchDeployversionData() {
      const parmas = {
        job__name: this.jobs.name
      }
      getDeployVersion(parmas).then(response => {
        this.versionForm = response.data[0]
        if (response.data.length > 0) {
          this.hasversion = true
        } else {
          this.versionForm = {
            job: this.jobs.name,
            version: '',
            content: ''
          }
          this.hasversion = false
        }
      })
    },
    selectEnv(env) {
      const selectenv = this.envs.filter(envs => envs.name === env)[0]
      this.ruleForm.deploy_hosts = selectenv.deploy_hosts
      this.ruleForm.deploy_cmd = ''
      this.fetchDeploycmdData(selectenv.id)
    },
    fetchDeployJobData() {
      getDeployJob(this.listQuery).then(response => {
        this.tableData = response.data.results
        this.tabletotal = response.data.count
        const job_status = this.tableData.map(function(item) {
          return item.deploy_status
        })
        if (job_status.indexOf('deploy') > -1) {
          this.check_job_status = setInterval(() => {
            const pramas = {
              job__name: this.jobs.name
            }
            getUpdateJobsStatus(pramas).then(response => {
              if (response.data.count === 0) {
                clearInterval(this.check_job_status)
                this.fetchDeployJobData()
              } else {
                console.log('check job_status 3/s')
              }
            })
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
      if (this.hasversion) {
        putDeployVersion(this.versionForm.id, this.versionForm)
      } else {
        console.log(this.hasversion)
        postDeployVersion(this.versionForm)
      }
      this.$refs[formdata].validate((valid) => {
        this.ruleForm = Object.assign(this.ruleForm, this.versionForm)
        if (valid) {
          if ((typeof this.ruleForm.deploy_hosts) === 'string') {
            this.ruleForm.deploy_hosts = this.ruleForm.deploy_hosts.split(',')
          }
          this.ruleForm.deploy_hosts = this.ruleForm.deploy_hosts.join()
          if (this.ruleForm.env === 'svn') {
            this.ruleForm.deploy_cmd = this.ruleForm.deploy_cmd.replace(/\$\w+/, this.jobs.deploy_path) + ' -r ' + this.ruleForm.version
          }
          postDeployJob(this.ruleForm).then(response => {
            console.log(response.data.j_id)
            this.$message({
              message: '构建成功，系统正在玩命发布中 ...',
              type: 'success'
            })
            this.fetchDeployJobData()

            if (this.sendnotice) {
              const messageForm = {
                action_user: 'ITDept_SkypeID',
                title: `【${this.ruleForm.job}】更新`,
                message: `版本号: ${this.ruleForm.version}\n更新内容: ${this.ruleForm.content}\n操作人: ${this.ruleForm.action_user}`
              }
              postSendmessage(messageForm)
            }
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
