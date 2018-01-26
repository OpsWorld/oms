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
          <i class="el-icon-question"> deploy_path</i>
        </el-form-item>
        <el-form-item label="发布主机" prop="deploy_hosts">
          <sesect-hosts :selecthost="envForm.hosts" @gethosts="getHosts"></sesect-hosts>
        </el-form-item>
        <el-form-item label="发布命令">
          <el-tabs v-model="actioncmdTab" type="card" editable @tab-add="addcmdForm=true" @tab-remove="removecmdTab">
            <el-tab-pane v-for="item in cmdTabValues" :key="item.name" :label="item.title" :name="item.name">
              <el-card>
                <el-form label-position="right" inline>
                  <el-form-item>
                    <span>{{item.content.deploy_cmd}}</span>
                  </el-form-item>
                </el-form>
              </el-card>
            </el-tab-pane>
          </el-tabs>
        </el-form-item>
        <el-form-item label="研发可见" prop="showdev">
          <el-switch v-model="ruleForm.showdev" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
        </el-form-item>
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
        <!--<el-form-item label="更新内容">-->
        <!--<span>{{item.content.desc}}</span>-->
        <!--</el-form-item>-->
        <!--</el-form>-->
        <!--</el-card>-->
        <!--</el-tab-pane>-->
        <!--</el-tabs>-->
        <!--</el-form-item>-->

        <el-form-item label="描述" prop="desc">
          <el-input v-model="ruleForm.desc" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
          <el-button type="danger" @click="resetForm('ruleForm')">清空</el-button>
        </el-form-item>
      </el-form>
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
import { postJob, postDeploycmd } from '@/api/job'
import sesectHosts from 'views/components/hosttransfer.vue'

export default {
  components: { sesectHosts },

  data() {
    return {
      ruleForm: {
        name: '',
        code_repo: 'svn',
        code_url: '',
        showdev: false,
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
        ],
        deploy_path: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ]
      },
      addenvForm: false,
      envForm: {
        job: '',
        name: '',
        hosts: [],
        path: '',
        desc: ''
      },
      actionTab: '',
      tabIndex: -1,
      TabValues: [],
      cmdForm: {
        job: '',
        name: 'svn更新',
        deploy_cmd: ''
      },
      addcmdForm: false,
      actioncmdTab: '',
      cmdtabIndex: -1,
      cmdTabValues: []
    }
  },

  created() {
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          postJob(this.ruleForm).then(response => {
            if (response.statusText === 'Created') {
              this.$message({
                type: 'success',
                message: '恭喜你，新建成功'
              })
              //              for (const env of this.TabValues) {
              //                const envsForm = env.content
              //                envsForm.job = response.data.name
              //                postDeployenv(envsForm)
              //              }
              for (const cmd of this.cmdTabValues) {
                const cmdsForm = cmd.content
                cmdsForm.job = response.data.name
                postDeploycmd(cmdsForm)
              }
            }
            this.$router.push('/jobs/jobs')
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
    //      addTab() {
    //        this.addenvForm = false
    //        const newTabName = ++this.tabIndex + ''
    //        this.TabValues.push({
    //          title: this.envForm.name,
    //          name: newTabName,
    //          content: this.envForm
    //        })
    //        this.actionTab = newTabName
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
    },
    getHosts(data) {
      this.ruleForm.deploy_hosts = data
    }
  }
}
</script>

<style lang='scss'>

</style>
