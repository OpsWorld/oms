<template>
  <el-card style="width: 500px;margin: 20px;padding: 20px">
    收件人: <el-input v-model="mailForm.to_list" placeholder="请输入收件人"></el-input>
    抄送者: <el-input v-model="mailForm.cc_list" placeholder="请输入抄送者" disabled></el-input>
    主 题: <el-input v-model="mailForm.sub" placeholder="请输入主题" disabled></el-input>
    邮件内容: <el-input v-model="mailForm.context" placeholder="请输入邮件内容" disabled></el-input>
    <el-button type="success" plain @click="sendMail">发送测试邮件</el-button>
  </el-card>
</template>
<script>
import { ws_url } from '@/config'
import ElCard from '../../../../../omsFrontend/node_modules/element-ui/packages/card/src/main'
import ElInput from '../../../../../omsFrontend/node_modules/element-ui/packages/input/src/input'

export default {
  components: {
    ElInput,
    ElCard
  },
  data() {
    return {
      mailForm: {
        to_list: 'kiven@tb-gaming.com',
        cc_list: 'kiven@tb-gaming.com',
        sub: 'test',
        context: '我是一只小小鸟'
      },
      ws_stream: '/salt/sendmail/',
      ws: ''
    }
  },
  created() {
    this.wsInit()
  },
  methods: {
    sendMail() {
      this.ws.send(JSON.stringify(this.mailForm))
    },
    wsInit() {
      const self = this
      self.ws = new WebSocket(ws_url + self.ws_stream)
      if (self.ws.readyState === WebSocket.OPEN) self.ws.onopen()
      self.ws.onmessage = (e) => {
        this.$message({
          type: e.code,
          message: e.msg
        })
        // self.results.push(e.data);
      }
    }
  }
}
</script>
