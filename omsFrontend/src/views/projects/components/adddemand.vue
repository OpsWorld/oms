<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="ruleForm.name" placeholder="请输入名称"></el-input>
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
import { postDemandManager, getProjectType, postDemandEnclosure } from '@/api/project'
import { postUpload, postSendmessage } from 'api/tool'
import { uploadurl } from '@/config'
import { getConversionTime } from '@/utils'
import { getUser } from 'api/user'

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
        pid: ''
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
    this.getTypes()
  },
  methods: {
    postForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.ruleForm.pid = 'dm' + getConversionTime()
          postDemandManager(this.ruleForm).then(response => {
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
                postDemandEnclosure(this.enclosureForm)
              })
            }
            const pramas = {
              groups__name: 'OMS_Dev_Manager'
            }
            getUser(pramas).then(res => {
              const users = res.data
              for (const user of users) {
                const messageForm = {
                  action_user: user.username,
                  title: '【新需求】' + this.ruleForm.name,
                  message: `操作人: ${this.ruleForm.create_user}\n地址: http://${window.location.host}/#/projects/viewdemand/${response.data.id}`
                }
                postSendmessage(messageForm)
              }
            })
            this.$router.push('/projects/demands')
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
    getTypes() {
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
