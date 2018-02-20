<template>
  <div class="components-container" style='height:100vh'>
    <el-card style="max-width: 800px">
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="ruleForm.name" placeholder="请输入正确的内容"></el-input>
        </el-form-item>
        <el-form-item label="代码地址" prop="code_url">
          <el-input v-model="ruleForm.code_url" placeholder="请输入正确的内容"></el-input>
        </el-form-item>
        <el-form-item label="研发可见" prop="showdev">
          <el-switch v-model="ruleForm.showdev" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
        </el-form-item>
        <el-form-item label="配置环境">
          <el-card>
            <div slot="header">
              <el-button class="card-head-btn" type="text" icon="el-icon-plus" @click="addenvForm=true"></el-button>
            </div>
            <el-table :data="envsData" stripe @row-click="clickenvTable" style="width: 100%">
              <el-table-column prop="name" label="名称" width="80"></el-table-column>
              <el-table-column prop="deploy_hosts" label="发布主机">
                <template slot-scope="scope">
                  <div slot="reference" class="name-wrapper">
                    <el-tag v-for="item in scope.row.deploy_hosts" :key="item.id" size="mini"
                            style="margin-right: 3px">
                      {{item}}
                    </el-tag>
                  </div>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="180">
                <template slot-scope="scope">
                  <el-button type="success" size="mini">修改</el-button>
                  <el-button type="danger" size="mini" @click="deleteenvForm(scope.row.id)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-form-item>
        <el-form-item label="描述" prop="desc">
          <el-input v-model="ruleForm.desc" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm(ruleForm)">更新</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-dialog :visible.sync="addenvForm">
      <el-form v-model="envForm" ref="envForm" label-width="70px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="envForm.name" placeholder="请输入正确的内容"></el-input>
        </el-form-item>
        <el-form-item label="选择主机" prop="hosts">
          <sesect-hosts :selecthost="envForm.hosts" @gethosts="getHosts"></sesect-hosts>
        </el-form-item>
        <el-form-item label="描述" prop="desc">
          <el-input v-model="envForm.desc" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
    <el-button type="primary" @click="postenvForm">确 定</el-button>
    </span>
    </el-dialog>

    <el-dialog :visible.sync="addcmdForm">
      <el-form v-model="cmdForm" ref="cmdForm" label-width="70px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="cmdForm.name" placeholder="请输入正确的内容"></el-input>
        </el-form-item>
        <el-form-item label="发布命令" prop="deploy_cmd">
          <el-input v-model="cmdForm.deploy_cmd" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="postcmdForm">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<script>
import {
  getJob,
  putJob,
  getDeployenv,
  postDeployenv,
  deleteDeployenv,
  getDeploycmd,
  postDeploycmd,
  deleteDeploycmd
} from '@/api/job'
import sesectHosts from 'views/components/hosttransfer.vue'

export default {
  components: { sesectHosts },

  data() {
    return {
      route_path: this.$route.path.split('/'),
      job_id: this.$route.params.job_id,
      env_id: '',
      ruleForm: {
        name: '',
        code_url: '',
        showdev: false,
        desc: ''
      },
      rules: {
        name: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        code_url: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ]
      },
      addenvForm: false,
      addcmdForm: false,
      envsData: [],
      envForm: {
        job: this.$route.params.job_id,
        name: '',
        deploy_hosts: [],
        desc: ''
      },
      cmdsData: [],
      cmdForm: {
        env: '',
        name: 'svn',
        deploy_cmd: ''
      }
    }
  },

  created() {
    this.fetchJobData()
    this.fetchJobenvData()
  },
  methods: {
    fetchJobData() {
      const parms = null
      getJob(parms, this.job_id).then(response => {
        this.ruleForm = response.data
      })
    },
    fetchJobenvData() {
      const parms = {
        job: this.job_id
      }
      getDeployenv(parms).then(response => {
        this.envsData = response.data
      })
    },
    fetchJobcmdData() {
      const parms = {
        env: this.env_id
      }
      getDeploycmd(parms).then(response => {
        this.cmdsData = response.data
      })
    },
    clickenvTable(row) {
      this.env_id = row.id
    },
    postenvForm() {
      postDeployenv(this.envForm).then(response => {
        this.$message({
          message: '恭喜你，添加成功',
          type: 'success'
        })
        this.addenvForm = false
        this.fetchJobenvData()
      })
    },
    deleteenvForm(id) {
      deleteDeployenv(id).then(response => {
        this.$message({
          message: '恭喜你，删除成功',
          type: 'success'
        })
        this.fetchJobenvData()
      })
    },
    putenvForm() {
      postDeployenv(this.envForm).then(response => {
        this.$message({
          message: '恭喜你，添加成功',
          type: 'success'
        })
        this.addenvForm = false
        this.fetchJobenvData()
      })
    },
    postcmdForm() {
      postDeploycmd(this.cmdForm).then(response => {
        this.$message({
          message: '恭喜你，添加成功',
          type: 'success'
        })
        this.addcmdForm = false
        this.fetchJobcmdData()
      })
    },
    deletecmdForm(id) {
      deleteDeploycmd(id).then(response => {
        this.$message({
          message: '恭喜你，删除成功',
          type: 'success'
        })
        this.fetchJobcmdData()
      })
    },
    submitForm(formdata) {
      putJob(this.ruleForm.id, formdata).then(response => {
        this.$message({
          message: '恭喜你，更新成功',
          type: 'success'
        })
        this.$router.push('/jobs/jobs')
      }).catch(error => {
        this.$message.error('更新失败')
        console.log(error)
      })
    },
    getHosts(data) {
      this.envForm.deploy_hosts = data
    }
  }
}
</script>

<style lang='scss'>

</style>
