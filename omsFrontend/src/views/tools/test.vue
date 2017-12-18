<template>
  <el-card style="width: 500px;margin: 20px;padding: 20px">
    收件人:
    <el-input v-model="mailForm.to" placeholder="请输入收件人"></el-input>
    抄送者:
    <el-input v-model="mailForm.cc" placeholder="请输入抄送者" disabled></el-input>
    主 题:
    <el-input v-model="mailForm.sub" placeholder="请输入主题" disabled></el-input>
    邮件内容:
    <el-input v-model="mailForm.content" placeholder="请输入邮件内容" disabled></el-input>
    <el-button type="success" plain @click="sendMail">发送测试邮件</el-button>
  </el-card>
</template>
<script>
import { postSendmail } from 'api/tool'

export default {
  components: {
  },
  data() {
    return {
      mailForm: {
        to: 'kiven',
        cc: 'kiven',
        sub: 'test',
        content: '我是一只小小鸟'
      }
    }
  },
  created() {
  },
  methods: {
    sendMail() {
      postSendmail(this.mailForm)
    }
    //    wsInit() {
    //      const self = this
    //      self.ws = new WebSocket(ws_url + self.ws_stream)
    //      if (self.ws.readyState === WebSocket.OPEN) self.ws.onopen()
    //      self.ws.onmessage = (e) => {
    //        this.$message({
    //          type: e.code,
    //          message: e.msg
    //        })
    //        // self.results.push(e.data);
    //      }
    //    }
  }
}
</script>
