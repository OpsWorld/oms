<template>
  <div class="components-container" style='height:100vh'>
    <el-row :gutter="20">
      <el-col :span="10">
        <el-card>
          <div slot="header">
            <a class="jobname">【{{jobs.name}}】</a>
          </div>
          <template v-if="jobs.total_step===1">
            <el-steps :active="jobs.cur_step" process-status="finish" finish-status="success" align-center>
              <el-step title="版本信息"></el-step>
              <el-step title="svn"></el-step>
              <el-step title="完成"></el-step>
            </el-steps>

            <div class="stepitem">
              <el-form v-if="jobs.cur_step===0" :model="versionForm" :rules="svnrules" ref="versionForm"
                       label-width="90px">
                <el-form-item label="发布版本" prop="version">
                  <el-input v-model="versionForm.version" :disabled="onlyread"></el-input>
                </el-form-item>
                <el-form-item label="更新内容" prop="content">
                  <el-input v-model="versionForm.content" type="textarea"
                            :autosize="{ minRows: 5, maxRows: 10}" :disabled="onlyread"></el-input>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="saveVersion('versionForm')">确定</el-button>
                </el-form-item>
              </el-form>

              <el-form v-if="jobs.cur_step>0 && jobs.cur_step<jobs.total_step + 1" :model="ruleForm" ref="ruleForm"
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
                  <el-button type="primary" @click="submitForm('ruleForm')">发布</el-button>
                </el-form-item>
              </el-form>

              <el-form v-if="jobs.cur_step>jobs.total_step" :model="ruleForm" ref="ruleForm" label-width="90px">
                <el-form-item label="发布版本" prop="version">
                  <el-input v-model="jobs.version" disabled></el-input>
                </el-form-item>
                <el-form-item label="更新内容" prop="content">
                  <el-input v-model="jobs.content" type="textarea"
                            :autosize="{ minRows: 5, maxRows: 10}" disabled></el-input>
                </el-form-item>
                <el-form-item label="发送通知">
                  <el-checkbox v-model="sendnotice"></el-checkbox>
                </el-form-item>
              </el-form>
            </div>
          </template>

          <template v-if="jobs.total_step===2">
            <el-steps :active="jobs.cur_step" process-status="finish" finish-status="success" align-center>
              <el-step title="版本信息"></el-step>
              <el-step title="svn"></el-step>
              <el-step title="同步"></el-step>
              <el-step title="完成"></el-step>
            </el-steps>

            <div class="stepitem">
              <el-form v-if="jobs.cur_step===0" :model="versionForm" :rules="svnrules" ref="versionForm"
                       label-width="90px">
                <el-form-item label="发布版本" prop="version">
                  <el-input v-model="versionForm.version" :disabled="onlyread"></el-input>
                </el-form-item>
                <el-form-item label="更新内容" prop="content">
                  <el-input v-model="versionForm.content" type="textarea"
                            :autosize="{ minRows: 5, maxRows: 10}" :disabled="onlyread"></el-input>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="saveVersion('versionForm')">确定</el-button>
                </el-form-item>
              </el-form>

              <el-form v-if="jobs.cur_step>0 && jobs.cur_step<jobs.total_step + 1" :model="ruleForm" ref="ruleForm"
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
                  <el-button type="primary" @click="submitForm('ruleForm')">发布</el-button>
                </el-form-item>
              </el-form>

              <el-form v-if="jobs.cur_step>jobs.total_step" :model="ruleForm" ref="ruleForm" label-width="90px">
                <el-form-item label="发布版本" prop="version">
                  <el-input v-model="jobs.version" disabled></el-input>
                </el-form-item>
                <el-form-item label="更新内容" prop="content">
                  <el-input v-model="jobs.content" type="textarea"
                            :autosize="{ minRows: 5, maxRows: 10}" disabled></el-input>
                </el-form-item>
                <el-form-item label="发送通知">
                  <el-checkbox v-model="sendnotice"></el-checkbox>
                </el-form-item>
              </el-form>
            </div>

          </template>
          <hr class="heng"/>
          <div class="foot_btn">
            <el-button type="danger" plain @click="changeCurstepZero">取消</el-button>
            <el-button v-if="jobs.cur_step < jobs.total_step + 1" type="primary" @click="changeCurstep"
                       :disabled="!jobs.done">下一步
            </el-button>
            <el-button v-else type="success" @click="changeCurstep">完成发布</el-button>
          </div>
        </el-card>
      </el-col>

      <el-col :span="14">
        <job-record ref="jobrecord" @updateStatus="changeJobDone"></job-record>
      </el-col>
    </el-row>
  </div>
</template>
<script>
import { getJob, patchJob, postDeployJob, getDeployenv, getDeploycmd } from '@/api/job'
import { mapGetters } from 'vuex'
import { postSendmessage } from '@/api/tool'
import jobRecord from './jobrecord.vue'

export default {
  components: {
    jobRecord
  },

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
      sendnotice: true,
      hasversion: false,
      stepForm: {
        cur_step: 1,
        done: false
      },
      onlyread: false,
      checkAll: true,
      checkedcmds: []
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
      const parmas = null
      getJob(parmas, this.job_id).then(response => {
        this.jobs = response.data
        this.ruleForm.job = this.jobs.name
        if (this.jobs.cur_step > 0 && this.jobs.cur_step < this.jobs.total_step + 1) {
          this.fetchJobenvData(this.jobs.cur_step)
        }
      })
    },
    fetchJobenvData(level) {
      const parmas = {
        job__id: this.job_id,
        level: level
      }
      getDeployenv(parmas).then(response => {
        this.envs = response.data[0]
        this.ruleForm.env = this.envs.name
        this.fetchDeploycmdData(this.envs.id)
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
      this.$refs[formdata].validate((valid) => {
        if (valid) {
          this.ruleForm.deploy_hosts = this.envs.deploy_hosts.join()
          for (const item of this.checkedcmds) {
            if (this.ruleForm.env === 'svn') {
              this.ruleForm.deploy_cmd = item.deploy_cmd.replace(/\$\w+/, this.jobs.deploy_path) + ' -r ' + this.ruleForm.version
            } else {
              this.ruleForm.deploy_cmd = item.deploy_cmd
            }
            postDeployJob(this.ruleForm).then(response => {
              console.log(response.data.j_id)
              // 调用子组件 job-record 的fetchDeployJobData
              this.$refs.jobrecord.fetchDeployJobData()
            }).catch(error => {
              this.$message.error('构建失败，请检查参数是否正确！')
              console.log(error)
            })
          }
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    changeCurstep() {
      this.jobs.cur_step++
      this.stepForm.done = this.jobs.done = false
      if (this.jobs.cur_step > this.jobs.total_step + 1) {
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
    }
  }
}
</script>

<style lang='scss'>
  .foot_btn {
    float: right;
    margin-bottom: 30px;
  }

  .stepitem {
    margin-top: 50px;
    min-height: 200px;
  }
</style>
