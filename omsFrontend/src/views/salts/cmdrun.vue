<template>
  <div class="components-container" style='height:100vh'>
    <el-card class="runcmd">
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
        <el-form-item label="选择主机" prop="hosts">
          <sesect-hosts :selecthost="ruleForm.hosts" @gethosts="getHosts"></sesect-hosts>
        </el-form-item>
        <el-form-item label="命令列表">
          <el-button type="danger" size="small" v-for="item in commands" :key="item.id" @click="changeCmd(item.cmd)">
            {{item.name}}
          </el-button>
        </el-form-item>
        <el-form-item label="执行命令" prop="cmd">
          <el-input v-model="ruleForm.cmd" placeholder="防止恶意命令，暂时禁止直接输入"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm('ruleForm')">执行</el-button>
          <el-button type="success" :loading="running" v-if="running">执行中</el-button>
          <el-button type="success" v-if="showresult&&!running">执行成功</el-button>
        </el-form-item>

        <div class="runlog" v-for="item in job_results" :key="item.id">
          <p class="host">{{ item.host }}</p>
          <pre>{{ item.data }}</pre>
        </div>
      </el-form>
    </el-card>
  </div>
</template>
<script>
import sesectHosts from '../components/hosttransfer.vue'
import { getCmdrun, getSaltResult } from 'api/salt'

export default {
  components: { sesectHosts },

  data() {
    const cmdRule = (rule, value, callback) => {
      let num = 1
      for (var i of this.denycmd) {
        if (value.indexOf(i) > -1) {
          num = 0
          const cmd = value.split(' ')[0]
          this.results = ['你坏坏！命令【' + cmd + '】已进入黑名单']
        } else {
          num = num * num
        }
      }
      if (num === 0) {
        callback(new Error(this.results))
      } else {
        callback()
      }
    }
    return {
      ruleForm: {
        hosts: [],
        cmd: 'ls /tmp',
        user: 'admin'
      },
      rules: {
        cmd: [
          { required: true, message: '请输入命令', trigger: 'blur' },
          { validator: cmdRule, trigger: 'blur' }
        ]
      },
      commands: [
        { name: '连接数', cmd: 'netstat -nt' },
        { name: '磁盘', cmd: 'df -h' },
        { name: '内存', cmd: 'free -m' },
        {
          name: '乘法口诀',
          cmd: 'for ((i=1;i<=9;i++)); do for ((j=1;j<=i;j++)); do result=$(($i*$j));echo -n "$i"x"$j"=$result" ";done;echo;done'
        },
        { name: '关机', cmd: 'init 0' },
        { name: '删除', cmd: 'rm -rf /tmp' },
        { name: '移动', cmd: 'mv aaa /tmp' },
        { name: '防火墙', cmd: 'iptables -I INPUT -p tcp -j DORP' }
      ],
      denycmd: ['rm', 'rf', 'shutdown', 'reboot', 'init', 'halt', 'rmdir', 'mkdir', 'iptables', 'mv', 'wget', 'mk', '>', 'dev', '&', 'dd', '^'],
      jid: '',
      job_results: undefined,
      running: false,
      showresult: false,
      cmdrun_result: '',
      selecthosts: []
    }
  },
  created() {
  },
  methods: {
    submitForm(formName) {
      this.results = []
      this.$refs[formName].validate(valid => {
        if (valid) {
          getCmdrun(this.ruleForm).then(response => {
            this.jid = response.data.results
            console.log(this.jid)
            this.running = this.showresult = true
            this.cmdrun_result = setInterval(() => {
              console.log('check job_status 3/s')
              this.getResult(this.jid)
            }, 3000)
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    getResult(jid) {
      getSaltResult(jid).then(response => {
        const data = response.data.results
        const a = []
        Object.keys(data).map(function(k) {
          a.push({ host: k, data: data[k] })
        })
        this.job_results = a
        if (response.data.count > 0) {
          this.running = false
          clearInterval(this.cmdrun_result)
        }
      })
    },
    getHosts(data) {
      this.ruleForm.hosts = data
    },
    changeCmd(cmd) {
      this.ruleForm.cmd = cmd
    }
  }
}
</script>

<style lang='scss'>
  .runcmd {
    width: 80%;
  }
</style>
