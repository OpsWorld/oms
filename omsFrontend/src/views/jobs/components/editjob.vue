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
        <el-form-item label="svn命令" prop="repo_cmd">
          <el-input v-model="ruleForm.repo_cmd" placeholder="请输入正确的内容"></el-input>
        </el-form-item>
        <el-form-item label="发布路径" prop="deploy_path">
          <el-input v-model="ruleForm.deploy_path" placeholder="请输入正确的内容"></el-input>
          <i class="el-icon-question"> deploy_path</i>
        </el-form-item>
        <el-form-item label="发布主机" prop="deploy_hosts">
          <sesect-hosts :selecthost="ruleForm.deploy_hosts" @gethosts="getHosts"></sesect-hosts>
        </el-form-item>
        <el-form-item label="扩展命令">
          <el-tabs v-model="actioncmdTab" type="card" editable @tab-add="addcmdForm=true" @tab-remove="removecmdTab">
            <el-tab-pane v-for="item in cmdTabValues" :key="item.name" :label="item.title" :name="item.name">
              <el-card>
                <el-form label-position="right">
                  <el-form-item>
                    <el-tag size="mini" style="margin-right: 3px" v-for="host in item.content.hosts.split('|')" :key="host">{{host}}</el-tag>
                  </el-form-item>
                  <el-form-item>
                    <el-alert :title="item.content.deploy_cmd" type="success" :closable="false"></el-alert>
                  </el-form-item>
                </el-form>
              </el-card>
            </el-tab-pane>
          </el-tabs>
        </el-form-item>
        <el-form-item label="研发可见" prop="showdev">
          <el-switch v-model="ruleForm.showdev" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
        </el-form-item>
        <el-form-item label="描述" prop="desc">
          <el-input v-model="ruleForm.desc" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm(ruleForm)">更新</el-button>
        </el-form-item>
      </el-form>

      <!--<el-form-item label="配置环境">-->
      <!--<el-tabs v-model="actionTab" type="card" editable @tab-add="addenvForm=true" @tab-remove="removeTab">-->
      <!--<el-tab-pane v-for="item in TabValues" :key="item.name" :label="item.title" :name="item.name">-->
      <!--<el-card>-->
      <!--<el-form label-position="right" inline class="table-expand">-->
      <!--<el-form-item label="环境名称">-->
      <!--<span>{{item.content.name}}</span>-->
      <!--</el-form-item>-->
      <!--<el-form-item label="发布路径">-->
      <!--<span>{{item.content.path}}</span>-->
      <!--</el-form-item>-->
      <!--<el-form-item label="发布主机">-->
      <!--<el-tag v-for="host in item.content.hosts" :key="host" style="margin-right: 5px">{{host}}</el-tag>-->
      <!--</el-form-item>-->
      <!--<el-form-item label="描述">-->
      <!--<span>{{item.content.desc}}</span>-->
      <!--</el-form-item>-->
      <!--</el-form>-->
      <!--</el-card>-->
      <!--</el-tab-pane>-->
      <!--</el-tabs>-->
      <!--</el-form-item>-->

    </el-card>

    <!--<el-dialog :visible.sync="addenvForm">-->
    <!--<el-form v-model="envForm" ref="envForm" label-width="70px">-->
    <!--<el-form-item label="名称" prop="name">-->
    <!--<el-input v-model="envForm.name" placeholder="请输入正确的内容"></el-input>-->
    <!--</el-form-item>-->
    <!--<el-form-item label="发布路径" prop="path">-->
    <!--<el-input v-model="envForm.path" placeholder="请输入正确的内容"></el-input>-->
    <!--</el-form-item>-->
    <!--<el-form-item label="选择主机" prop="hosts">-->
    <!--<sesect-hosts :selecthost="envForm.hosts" @gethosts="getHosts"></sesect-hosts>-->
    <!--</el-form-item>-->
    <!--<el-form-item label="描述" prop="desc">-->
    <!--<el-input v-model="envForm.desc" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>-->
    <!--</el-form-item>-->
    <!--</el-form>-->
    <!--<span slot="footer" class="dialog-footer">-->
    <!--<el-button type="primary" @click="addTab">确 定</el-button>-->
    <!--</span>-->
    <!--</el-dialog>-->
    <el-dialog :visible.sync="addcmdForm">
      <el-form v-model="cmdForm" ref="cmdForm" label-width="70px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="cmdForm.name" placeholder="请输入正确的内容"></el-input>
        </el-form-item>
        <el-form-item label="主机" prop="hosts">
          <el-input v-model="cmdForm.hosts" placeholder="1.1.1.1|2.2.2.2|3.3.3.3"></el-input>
        </el-form-item>
        <el-form-item label="发布命令" prop="deploy_cmd">
          <el-input v-model="cmdForm.deploy_cmd" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="addcmdTab">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<script>
import { getJob, putJob, getDeploycmd, postDeploycmd, deleteDeploycmd } from '@/api/job'
import sesectHosts from 'views/components/hosttransfer.vue'

export default {
  components: { sesectHosts },

  data() {
    return {
      route_path: this.$route.path.split('/'),
      job_id: this.$route.params.job_id,
      ruleForm: {
        name: '',
        code_repo: 'svn',
        code_url: '',
        repo_cmd: '"C:\Program Files\TortoiseSVN\bin\svn.exe"',
        deploy_hosts: [],
        deploy_path: '',
        desc: ''
      },
      rules: {
        name: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        deploy_cmd: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        code_url: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ]
      },
      addenvForm: false,
      envForm: {},
      actionTab: '',
      tabIndex: -1,
      TabValues: [],
      removeenvs: [],
      cmdForm: {
        job: '',
        name: '同步',
        hosts: '',
        deploy_cmd: ''
      },
      addcmdForm: false,
      actioncmdTab: '',
      cmdtabIndex: -1,
      cmdTabValues: [],
      removecmds: []
    }
  },

  created() {
    this.fetchJobData()
  },
  methods: {
    fetchJobData() {
      const parms = null
      getJob(parms, this.job_id).then(response => {
        this.ruleForm = response.data
        this.fetchJobenvData(this.ruleForm.name)
      })
    },
    fetchJobenvData(job) {
      const parms = {
        job__name: job
      }
      getDeploycmd(parms).then(response => {
        for (var i = 0; i < response.data.length; i++) {
          this.cmdtabIndex = i
          this.cmdTabValues.push({
            title: response.data[i].name,
            name: i + '',
            content: response.data[i]
          })
        }
      })
    },
    //      addTab() {
    //        this.addenvForm = false
    //        const newTabName = ++this.tabIndex + ''
    //        this.TabValues.push({
    //          title: this.envForm.name,
    //          name: newTabName,
    //          content: this.envForm
    //        })
    //        this.actionTab = newTabName
    //        this.envForm.job = this.ruleForm.name
    //        postDeployenv(this.envForm)
    //        this.envForm = {}
    //      },
    //      removeTab(targetName) {
    //        const tabs = this.TabValues
    //        let activeName = this.actionTab
    //        if (activeName === targetName) {
    //          tabs.forEach((tab, index) => {
    //            if (tab.name === targetName) {
    //              const nextTab = tabs[index + 1] || tabs[index - 1]
    //              if (nextTab) {
    //                activeName = nextTab.name
    //              }
    //            }
    //          })
    //        }
    //        this.actionTab = activeName
    //        this.TabValues = tabs.filter(tab => tab.name !== targetName)
    //        const remove_id = tabs.filter(tab => tab.name === targetName)[0].content.id
    //        this.removeenvs.push(remove_id)
    //      },
    addcmdTab() {
      this.addcmdForm = false
      const newTabName = ++this.cmdtabIndex + ''
      this.cmdTabValues.push({
        title: this.cmdForm.name,
        name: newTabName,
        content: this.cmdForm
      })
      this.actioncmdTab = newTabName
      this.cmdForm.job = this.ruleForm.name
      postDeploycmd(this.cmdForm)
      this.cmdForm = {}
    },
    removecmdTab(targetName) {
      const tabs = this.cmdTabValues
      let activeName = this.actioncmdTab
      if (activeName === targetName) {
        tabs.forEach((tab, index) => {
          if (tab.name === targetName) {
            const nextTab = tabs[index + 1] || tabs[index - 1]
            if (nextTab) {
              activeName = nextTab.name
            }
          }
        })
      }
      this.actioncmdTab = activeName
      this.cmdTabValues = tabs.filter(tab => tab.name !== targetName)
      const remove_id = tabs.filter(tab => tab.name === targetName)[0].content.id
      this.removecmds.push(remove_id)
    },
    submitForm(formdata) {
      putJob(this.ruleForm.id, formdata).then(response => {
        this.$message({
          message: '恭喜你，更新成功',
          type: 'success'
        })
        for (const id of this.removecmds) {
          deleteDeploycmd(id)
        }
        this.$router.push('/jobs/jobs')
      }).catch(error => {
        this.$message.error('更新失败')
        console.log(error)
      })
    },
    getHosts(data) {
      //      this.envForm.hosts = data
      this.ruleForm.deploy_hosts = data
    }
  }
}
</script>

<style lang='scss'>

</style>
