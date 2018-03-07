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
        <job-record ref="jobrecord"></job-record>
      </el-col>
    </el-row>
  </div>
</template>
<script>
import {
  getJob,
  postDeployJob,
  getDeployenv,
  getDeploycmd,
  postDeployVersion,
  putDeployVersion,
  getDeployVersion
} from '@/api/job'
import { mapGetters } from 'vuex'
import { postSendmessage } from '@/api/tool'
import jobRecord from './jobrecord.vue'

export default {
  components: { jobRecord },

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
        this.ruleForm.job = this.jobs.name
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
            // 调用子组件 job-record 的fetchDeployJobData
            this.$refs.jobrecord.fetchDeployJobData()

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
    }
  }
}
</script>

<style lang='scss'>

</style>
