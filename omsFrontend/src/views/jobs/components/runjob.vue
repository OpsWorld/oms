<template>
  <div class="components-container" style='height:100vh'>
    <el-row :gutter="20">
      <el-col :span="10">
        <el-card>
          <div slot="header">
            <a class="jobname">【{{jobs.name}}】</a>
          </div>
          <template>
            <el-steps :active="jobs.cur_step" process-status="finish" finish-status="success" align-center>
              <el-step title="版本信息"></el-step>
              <el-step v-for="item in steps" :key="item.level" :title="item.name"></el-step>
            </el-steps>

            <div class="stepitem">
              <el-form v-if="jobs.cur_step===0" :model="versionForm" ref="versionForm"
                       label-width="90px">
                <el-form-item label="发布版本" prop="version">
                  <el-input v-model="versionForm.version" :disabled="onlyread"></el-input>
                </el-form-item>
                <el-form-item label="更新内容" prop="content">
                  <el-input v-model="versionForm.content" type="textarea"
                            :autosize="{ minRows: 5, maxRows: 10}" :disabled="onlyread"></el-input>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="saveVersion('versionForm')">Submit</el-button>
                </el-form-item>
              </el-form>

              <el-form v-if="jobs.cur_step>0" :model="ruleForm" ref="ruleForm"
                       label-width="90px">
                <el-form-item label="发布命令" prop="deploy_cmd">
                  <el-checkbox v-model="checkAll" @change="handleCheckAllChange">全选
                  </el-checkbox>
                  <div style="margin: 15px 0;"></div>
                  <el-checkbox-group v-model="checkedcmds" @change="handleCheckedcmdsChange">
                    <el-checkbox v-for="item in cmds" :label="item" :key="item.deploy_cmd">{{item.name}}</el-checkbox>
                  </el-checkbox-group>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="submitForm('ruleForm')">Deploy</el-button>
                </el-form-item>
              </el-form>
            </div>

          </template>
          <hr class="heng"/>
          <div class="foot_btn">
            <el-checkbox v-if="jobs.cur_step===jobs.total_step && jobs.done" v-model="sendnotice"
                         style="margin-right: 20px">发送通知
            </el-checkbox>
            <el-button type="danger" plain @click="changeCurstepZero">Cancel</el-button>
            <el-button v-if="jobs.cur_step===jobs.total_step" type="success" @click="changeCurstep"
                       :disabled="!jobs.done">Complete
            </el-button>
            <el-button v-else type="primary" @click="changeCurstep">Next</el-button>
          </div>
        </el-card>
      </el-col>

      <el-col :span="14">
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
  import {getJob, patchJob, postDeployJob, getDeployenv, getDeploycmd} from '@/api/job'
  import {getDeployJob, deleteDeployJob, getUpdateJobsStatus} from '@/api/job'
  import {mapGetters} from 'vuex'
  import {LIMIT, pagesize, pageformat} from '@/config'
  import {postSendmessage} from '@/api/tool'

  export default {
    data() {
      return {
        route_path: this.$route.path.split('/'),
        job_id: this.$route.params.job_id,
        versionForm: {
          version: '',
          content: ''
        },
        ruleForm: {
          job: '',
          env: '',
          deploy_hosts: [],
          deploy_cmd: '',
          action_user: localStorage.getItem('username'),
          deploy_cmd_host: 'null'
        },
        steps: [],
        cur_env: {},
        cmds: [],
        jobs: {},
        sendnotice: true,
        hasversion: false,
        stepForm: {
          cur_step: 1,
          done: false
        },
        onlyread: false,
        checkAll: true,
        checkedcmds: [],
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
          deploy: {text: '发布中', type: 'primary', icon: 'el-icon-loading'},
          success: {text: '发布成功', type: 'success', icon: 'el-icon-success'},
          failed: {text: '发布失败', type: 'danger', icon: 'el-icon-error'}
        },
        selectId: [],
        butstatus: true,
        showresult: false,
        job_results: [],
        check_job_status: '',
        deploy_cmds: []
      }
    },
    computed: {
      ...mapGetters([
        'role'
      ])
    },
    created() {
      this.fetchJobData()
      this.fetchDeployJobData()
    },
    methods: {
      fetchJobData() {
        const parmas = null
        getJob(parmas, this.job_id).then(response => {
          this.jobs = response.data
          this.ruleForm.job = this.jobs.name
          const parmas = {
            job__id: this.job_id
          }
          getDeployenv(parmas).then(response => {
            this.steps = response.data
          })
          const data = {
            job__id: this.job_id,
            level: this.jobs.cur_step
          }
          this.fetchJobenvData(data)
        })
      },
      fetchJobenvData(parmas) {
        getDeployenv(parmas).then(response => {
          this.cur_env = response.data[0]
          if (this.cur_env) {
            this.ruleForm.env = this.cur_env.id
            this.fetchDeploycmdData(this.cur_env.id)
          }
        })
      },
      fetchDeploycmdData(env) {
        const parmas = {
          env__id: env
        }
        getDeploycmd(parmas).then(response => {
          this.checkedcmds = this.cmds = response.data
        })
      },
      submitForm(formdata) {
        this.ruleForm.content = this.jobs.content
        this.ruleForm.version = this.jobs.version
        this.ruleForm.deploy_hosts = this.cur_env.deploy_hosts.join()
        this.deploy_cmds = []
        for (const item of this.checkedcmds) {
          this.deploy_cmds.push(item.name)
        }
        this.ruleForm.deploy_cmd = this.deploy_cmds.join('||')
        this.ruleForm.deploy_path = this.jobs.deploy_path
        postDeployJob(this.ruleForm).then(response => {
          console.log(response.data.j_id)
          this.fetchDeployJobData()
        }).catch(error => {
          this.$message.error('构建失败，请检查参数是否正确！')
          console.log(error)
        })
      },
      changeCurstep() {
        this.jobs.cur_step++
        this.stepForm.done = this.jobs.done = false
        if (this.jobs.cur_step > this.jobs.total_step) {
          this.jobs.cur_step = this.stepForm.cur_step = 0
          if (this.sendnotice) {
            const messageForm = {
              action_user: 'ITDept_SkypeID',
              title: `【${this.jobs.name}】更新`,
              message: `版本号: ${this.jobs.version}\n更新内容: ${this.jobs.content}\n操作人: ${this.ruleForm.action_user}`
            }
            postSendmessage(messageForm)
          }
          patchJob(this.job_id, this.stepForm).then(() => {
            this.$router.push('/jobs/jobs')
          })
        } else {
          this.stepForm.cur_step = this.jobs.cur_step
          patchJob(this.job_id, this.stepForm).then(() => {
            this.fetchJobData()
          })
        }
      },
      changeCurstepZero() {
        this.onlyread = this.stepForm.done = this.jobs.done = false
        this.jobs.cur_step = this.stepForm.cur_step = 0
        patchJob(this.job_id, this.stepForm)
      },
      changeJobDone() {
        this.onlyread = this.stepForm.done = this.jobs.done = true
        patchJob(this.job_id, this.stepForm)
      },
      saveVersion(formdata) {
        this.$refs[formdata].validate((valid) => {
          if (valid) {
            patchJob(this.job_id, this.versionForm)
            this.onlyread = this.stepForm.done = this.jobs.done = true
          }
        })
      },
      handleCheckAllChange(val) {
        this.checkedcmds = val ? this.cmds : []
      },
      handleCheckedcmdsChange(value) {
        const checkedCount = value.length
        this.checkAll = checkedCount === this.cmds.length
      },
      fetchDeployJobData() {
        this.listQuery.job__id = this.job_id
        getDeployJob(this.listQuery).then(response => {
          this.tableData = response.data.results
          this.tabletotal = response.data.count
          const job_status = this.tableData.map(function (item) {
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
                  this.jobs.done = true
                  this.fetchDeployJobData()
                } else {
                  console.log('check job_status 3/s')
                }
              })
            }, 3000)
          } else {
            console.log('setInterval_id:' + this.check_job_status)
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
        Object.keys(data).map(function (k) {
          a.push({'host': k, 'data': data[k]})
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

  .foot_btn {
    float: right;
    margin-bottom: 30px;
  }

  .stepitem {
    margin-top: 50px;
    min-height: 200px;
  }
</style>
