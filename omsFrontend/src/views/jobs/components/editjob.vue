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
        <el-form-item label="发布路径" prop="deploy_path">
          <el-input v-model="ruleForm.deploy_path" placeholder="请输入正确的内容"></el-input>
        </el-form-item>
        <el-form-item label="研发可见" prop="showdev">
          <el-switch v-model="ruleForm.showdev" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
        </el-form-item>
        <el-form-item label="发布步骤">
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
                  <el-button type="success" size="mini" @click="updateenvForm(scope.row)">修改</el-button>
                  <el-button type="danger" size="mini" @click="deleteenvForm(scope.row.id)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-form-item>
        <el-form-item v-if="showcmd" label="配置命令">
          <el-card>
            <div slot="header">
              <el-button class="card-head-btn" type="text" icon="el-icon-plus" @click="addcmdForm=true"></el-button>
            </div>
            <el-table :data="cmdsData" stripe style="width: 100%">
              <el-table-column prop="name" label="名称" width="80"></el-table-column>
              <el-table-column prop="deploy_cmd" label="发布命令"></el-table-column>
              <el-table-column label="操作" width="180">
                <template slot-scope="scope">
                  <el-button type="success" size="mini" @click="updatecmdForm(scope.row)">修改</el-button>
                  <el-button type="danger" size="mini" @click="deletecmdForm(scope.row.id)">删除</el-button>
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
          <sesect-hosts :selecthost="envForm.deploy_hosts" @gethosts="getaddHosts"></sesect-hosts>
        </el-form-item>
        <el-form-item label="描述" prop="desc">
          <el-input v-model="envForm.desc" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="postenvForm">确 定</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-dialog :visible.sync="editenvForm">
      <el-form v-model="envdata" ref="envForm" label-width="70px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="envdata.name" placeholder="请输入正确的内容"></el-input>
        </el-form-item>
        <el-form-item label="选择主机" prop="hosts">
          <sesect-hosts :selecthost="envdata.deploy_hosts" @gethosts="geteditHosts"></sesect-hosts>
        </el-form-item>
        <el-form-item label="描述" prop="desc">
          <el-input v-model="envdata.desc" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="putenvForm">确 定</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-dialog :visible.sync="addcmdForm">
      <el-form v-model="cmdForm" ref="cmdForm" label-width="70px">
        <el-form-item label="环境" prop="env">
          <el-select v-model="cmdForm.env" placeholder="请选择环境">
            <el-option v-for="item in envsData" :key="item.id" :label="item.name" :value="item.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="名称" prop="name">
          <el-input v-model="cmdForm.name" placeholder="请输入正确的内容"></el-input>
        </el-form-item>
        <el-form-item label="发布命令" prop="deploy_cmd">
          <el-input v-model="cmdForm.deploy_cmd" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="postcmdForm">确 定</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-dialog :visible.sync="editcmdForm">
      <el-form v-model="cmddata" ref="cmdForm" label-width="70px">
        <el-form-item label="环境" prop="env">
          <el-select v-model="cmddata.env" placeholder="请选择环境">
            <el-option v-for="item in envsData" :key="item.id" :label="item.name" :value="item.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="名称" prop="name">
          <el-input v-model="cmddata.name" placeholder="请输入正确的内容"></el-input>
        </el-form-item>
        <el-form-item label="发布命令" prop="deploy_cmd">
          <el-input v-model="cmddata.deploy_cmd" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="putcmdForm">确 定</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>
<script>
import {
  getJob,
  putJob,
  getDeployenv,
  postDeployenv,
  putDeployenv,
  deleteDeployenv,
  getDeploycmd,
  postDeploycmd,
  putDeploycmd,
  deleteDeploycmd
} from '@/api/job'
import sesectHosts from 'views/components/hosttransfer.vue'

export default {
  components: { sesectHosts },

  data() {
    return {
      route_path: this.$route.path.split('/'),
      job_id: this.$route.params.job_id,
      ruleForm: {
        name: '',
        code_url: '',
        deploy_path: '',
        showdev: false,
        desc: ''
      },
      rules: {
        name: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        code_url: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        deploy_path: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ]
      },
      addenvForm: false,
      editenvForm: false,
      addcmdForm: false,
      editcmdForm: false,
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
      },
      showcmd: false,
      envdata: {},
      cmddata: {}
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
        job__id: this.job_id
      }
      getDeployenv(parms).then(response => {
        this.envsData = response.data
      })
    },
    fetchJobcmdData() {
      const parms = {
        env__id: this.cmdForm.env
      }
      getDeploycmd(parms).then(response => {
        this.cmdsData = response.data
      })
    },
    clickenvTable(row) {
      this.showcmd = true
      this.cmdForm.env = row.id
      this.fetchJobcmdData()
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
    putenvForm() {
      putDeployenv(this.envdata.id, this.envdata).then(response => {
        this.$message({
          message: '恭喜你，更新成功',
          type: 'success'
        })
        this.editenvForm = false
        this.fetchJobenvData()
      })
    },
    updateenvForm(row) {
      this.envdata = row
      this.editenvForm = true
    },
    updatecmdForm(row) {
      this.cmddata = row
      this.editcmdForm = true
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
    putcmdForm() {
      putDeploycmd(this.cmddata.id, this.cmddata).then(response => {
        this.$message({
          message: '恭喜你，更新成功',
          type: 'success'
        })
        this.editcmdForm = false
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
    getaddHosts(data) {
      this.envForm.deploy_hosts = data
    },
    geteditHosts(data) {
      this.envdata.deploy_hosts = data
    }
  }
}
</script>

<style lang='scss'>

</style>
