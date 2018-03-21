<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="ruleForm.name" placeholder="请输入名称"></el-input>
        </el-form-item>
        <el-form-item label="指派人" prop="action_user">
          <el-select v-model="ruleForm.action_user" filterable placeholder="请选择指派人">
            <el-option v-for="item in users" :key="item.id" :value="item.username"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <mavon-editor style="z-index: 1" v-model="ruleForm.content" code_style="monokai"
                        :toolbars="toolbars" @imgAdd="imgAdd" ref="md"></mavon-editor>
          <a class="tips"> Tip：截图可以直接 Ctrl + v 粘贴到内容里面</a>
        </el-form-item>
        <el-form-item label="时间" prop="end_time">
          <el-date-picker
            v-model="ruleForm.time"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="yyyy-MM-dd">
          </el-date-picker>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="postForm('ruleForm')">提交</el-button>
          <el-button type="danger" @click="resetForm('ruleForm')">清空</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>
<script>
import { postProject } from '@/api/optask'
import { postUpload, postSendmessage } from 'api/tool'
import { getUser } from 'api/user'
import { uploadurl } from '@/config'
import { getConversionTime } from '@/utils'

export default {
  components: {},

  data() {
    return {
      route_path: this.$route.path.split('/'),
      ruleForm: {
        name: '',
        content: '',
        create_user: localStorage.getItem('username'),
        level: 1,
        complete: 0,
        action_user: '',
        pid: '',
        is_public: true
      },
      rules: {
        name: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        content: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ]
      },
      users: [],
      toolbars: {
        preview: true, // 预览
        bold: true, // 粗体
        italic: true, // 斜体
        header: true, // 标题
        underline: true, // 下划线
        strikethrough: true, // 中划线
        ol: true, // 有序列表
        help: true
      },
      uploadurl: uploadurl,
      img_file: {},
      sendnotice: false,
      fileList: [],
      count: 0
    }
  },

  created() {
    this.getUsers()
    this.getUsers()
  },
  methods: {
    postForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.ruleForm.start_time = this.ruleForm.time[0]
          this.ruleForm.end_time = this.ruleForm.time[1]
          this.ruleForm.pid = 'pps' + getConversionTime()
          postProject(this.ruleForm).then(response => {
            if (response.statusText === '"Created"') {
              this.$message({
                type: 'success',
                message: '恭喜你，新建成功'
              })
            }
            if (this.sendnotice) {
              const messageForm = {
                action_user: this.ruleForm.action_user,
                title: `【${this.ruleForm.type}】${this.ruleForm.title}`,
                message: `提交人: ${this.ruleForm.create_user}\n指派人: ${this.ruleForm.action_user}\n任务地址: http://${window.location.host}/#/projects/editproject/${this.ruleForm.id}`
              }
              postSendmessage(messageForm)
            }
            this.$router.push('/opstasks/opsprojects')
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
    getUsers() {
      const query = {
        groups__name: 'ITDept'
      }
      getUser(query).then(response => {
        this.users = response.data
      })
    },
    imgAdd(pos, file) {
      var md = this.$refs.md
      const formData = new FormData()
      formData.append('username', this.ruleForm.create_user)
      formData.append('file', file)
      formData.append('create_time', getConversionTime(file.lastModified))
      formData.append('type', file.type)
      formData.append('archive', this.route_path[1])
      postUpload(formData).then(response => {
        md.$imglst2Url([[pos, response.data.file]])
      })
    },
    handleSuccess(file, fileList) {
      this.fileList.push(fileList.raw)
      this.count += 1
    },
    handleRemove(file, fileList) {
      this.fileList.remove(file)
      this.count -= 1
    }
  }
}
</script>

<style lang='scss'>
  .addticket {
    margin: 50px;
    width: 80%;
  }
</style>
