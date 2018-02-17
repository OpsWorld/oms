<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="ruleForm.name" placeholder="请输入名称"></el-input>
        </el-form-item>
        <el-form-item label="指派人" prop="action_user">
          <el-select v-model="ruleForm.action_user" filterable multiple placeholder="请选择指派人">
            <el-option v-for="item in users" :key="item.id" :value="item.username"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="抄送人" prop="follow_user">
          <el-select v-model="ruleForm.follow_user" filterable multiple placeholder="请选择跟踪人">
            <el-option v-for="item in users" :key="item.id" :value="item.username"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="需求人" prop="from_user">
          <el-input v-model="ruleForm.from_user" placeholder="请输入需求人"></el-input>
        </el-form-item>
        <el-form-item label="类型" prop="type">
          <el-select v-model="ruleForm.type" placeholder="请选择类型">
            <el-option v-for="item in types" :key="item.id" :value="item.name"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <mavon-editor style="z-index: 1" v-model="ruleForm.content" code_style="monokai"
                        :toolbars="toolbars" @imgAdd="imgAdd" ref="md"></mavon-editor>
          <a class="tips"> Tip：截图可以直接 Ctrl + v 粘贴到内容里面</a>
        </el-form-item>
        <el-form-item label="等级" prop="level">
          <el-rate
            v-model="ruleForm.level"
            :colors="['#99A9BF', '#F7BA2A', '#ff1425']"
            show-text
            :texts="['E', 'D', 'C', 'B', 'A']">
          </el-rate>
          <a class="tips">Tip：星数代表问题紧急程度，星数越多，代表越紧急</a>
        </el-form-item>
        <el-form-item label="是否公开" prop="is_public">
          <el-switch v-model="ruleForm.is_public" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
        </el-form-item>
        <el-form-item label="附件">
          <el-upload
            ref="upload"
            :action="uploadurl"
            :on-success="handleSuccess"
            :on-remove="handleRemove"
            :file-list="fileList">
            <el-button slot="trigger" size="mini" type="success" plain :disabled="count>4">
              上传
            </el-button>
            <div slot="tip" class="el-upload__tip">
              <p>上传文件不超过10m，<a style="color: red">最多只能上传5个文件</a></p>
            </div>
          </el-upload>
          <hr class="heng"/>
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
import { postProject, getProjectType } from '@/api/project'
import { postProjectEnclosure } from '@/api/project'
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
        type: '',
        content: '',
        create_user: localStorage.getItem('username'),
        level: 1,
        complete: 0,
        action_user: '',
        follow_user: '',
        from_user: '',
        pid: '',
        is_public: true,
        desc: ''
      },
      rules: {
        name: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        content: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        type: [
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
      types: [],
      img_file: {},
      sendnotice: false,
      fileList: [],
      count: 0,
      enclosureData: [],
      enclosureForm: {
        project: '',
        create_user: localStorage.getItem('username'),
        file: ''
      }
    }
  },

  created() {
    this.getProjectUsers()
    this.getTicketType()
  },
  methods: {
    postForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.ruleForm.pid = getConversionTime()
          postProject(this.ruleForm).then(response => {
            if (response.statusText === '"Created"') {
              this.$message({
                type: 'success',
                message: '恭喜你，新建成功'
              })
            }
            for (var fileList of this.fileList) {
              const formData = new FormData()
              formData.append('username', this.enclosureForm.create_user)
              formData.append('file', fileList)
              formData.append('create_time', getConversionTime(fileList.uid))
              formData.append('type', fileList.type)
              formData.append('archive', this.route_path[1])
              postUpload(formData).then(res => {
                this.enclosureForm.file = res.data.filepath
                this.enclosureForm.project = response.data.id
                postProjectEnclosure(this.enclosureForm)
              })
            }
            if (this.sendnotice) {
              const messageForm = {
                action_user: this.ruleForm.action_user.join(),
                title: `【${this.ruleForm.type}】${this.ruleForm.title}`,
                message: `提交人: ${this.ruleForm.create_user}\n指派人: ${this.ruleForm.action_user}\n任务地址: http://${window.location.host}/#/projects/editproject/${this.ruleForm.id}`
              }
              postSendmessage(messageForm)
            }
            this.$router.push('/projects/projects')
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
    getProjectUsers() {
      const query = {
        groups__name: 'ITDept'
      }
      getUser(query).then(response => {
        this.users = response.data
      })
    },

    getTicketType() {
      getProjectType().then(response => {
        this.types = response.data
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
