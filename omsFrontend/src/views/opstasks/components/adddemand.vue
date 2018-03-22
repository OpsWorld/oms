<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="ruleForm.name" placeholder="请输入名称"></el-input>
        </el-form-item>
        <el-form-item label="目标" prop="content1">
          <el-input v-model="ruleForm.content1" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
        </el-form-item>
        <el-form-item label="范围" prop="content2">
          <el-input v-model="ruleForm.content2" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
        </el-form-item>
        <el-form-item label="预算" prop="content3">
          <el-input v-model="ruleForm.content3" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
        </el-form-item>
        <el-form-item label="时间" prop="time">
          <el-date-picker
            v-model="ruleForm.time"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="yyyy-MM-dd">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="参与者" prop="action_user">
          <el-select v-model="ruleForm.action_user" filterable multiple placeholder="请选择参与者">
            <el-option v-for="item in users" :key="item.id" :value="item.username"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="备注" prop="desc">
          <el-input v-model="ruleForm.desc" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
        </el-form-item>
        <!--<el-form-item label="附件">-->
        <!--<el-upload-->
        <!--ref="upload"-->
        <!--:action="uploadurl"-->
        <!--:on-success="handleSuccess"-->
        <!--:on-remove="handleRemove"-->
        <!--:file-list="fileList">-->
        <!--<el-button slot="trigger" size="mini" type="success" plain :disabled="count>4">-->
        <!--上传-->
        <!--</el-button>-->
        <!--<div slot="tip" class="el-upload__tip">-->
        <!--<p>上传文件不超过10m，<a style="color: red">最多只能上传5个文件</a></p>-->
        <!--</div>-->
        <!--</el-upload>-->
        <!--<hr class="heng"/>-->
        <!--</el-form-item>-->
        <el-form-item>
          <el-button type="primary" @click="postForm('ruleForm')">提交</el-button>
          <el-button type="danger" @click="resetForm('ruleForm')">清空</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>
<script>
import { postopsDemandManager, postopsDemandEnclosure } from '@/api/optask'
import { postUpload } from 'api/tool'
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
        content1: '',
        content2: '',
        content3: '',
        create_user: localStorage.getItem('username'),
        action_user: [],
        pid: '',
        time: ''
      },
      rules: {
        name: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        time: [
          { required: true, type: 'array', message: '请输入正确的内容', trigger: 'blur' }
        ],
        content1: [
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
    this.getUsers()
  },
  methods: {
    postForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.ruleForm.pid = 'ppt' + getConversionTime()
          this.ruleForm.start_time = this.ruleForm.time[0]
          this.ruleForm.end_time = this.ruleForm.time[1]
          postopsDemandManager(this.ruleForm).then(response => {
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
                postopsDemandEnclosure(this.enclosureForm)
              })
            }
            this.$router.push('/opstasks/opsdemands')
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
    },
    getUsers() {
      const query = {
        groups__name: 'ITDept'
      }
      getUser(query).then(response => {
        this.users = response.data
      })
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
