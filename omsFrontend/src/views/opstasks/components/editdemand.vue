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
        <el-form-item label="时间" prop="ttime">
          <el-date-picker
            v-model="ttime"
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
        <!--:show-file-list="false"-->
        <!--:disabled="count>4"-->
        <!--:before-upload="beforeAvatarUpload">-->
        <!--<el-button slot="trigger" size="mini" type="success" plain :disabled="count>4">-->
        <!--上传-->
        <!--</el-button>-->
        <!--<div slot="tip" class="el-upload__tip">-->
        <!--<p><a style="color: red">最多只能上传5个文件</a></p>-->
        <!--</div>-->
        <!--</el-upload>-->
        <!--<hr class="heng"/>-->
        <!--<div v-if='enclosureData.length>0' class="ticketenclosure">-->
        <!--<ul>-->
        <!--<li v-for="item in enclosureData" :key="item.id" v-if="item.file" style="list-style:none">-->
        <!--<i class="fa fa-paperclip"></i>-->
        <!--<a :href="apiurl + '/upload/' + item.file" :download="item.file">{{item.file.split('/')[1]}}</a>-->
        <!--<el-tooltip class="item" effect="dark" content="删除附件" placement="right">-->
        <!--<el-button type="text" icon="el-icon-delete" @click="deleteEnclosure(item.id)"></el-button>-->
        <!--</el-tooltip>-->
        <!--</li>-->
        <!--</ul>-->
        <!--</div>-->
        <!--</el-form-item>-->
        <el-form-item>
          <el-button type="primary" @click="submitForm('ruleForm')">更新</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>
<script>
import { getDemandManager, putDemandManager } from '@/api/optask'
import { postopsDemandEnclosure, getDemandEnclosure, deleteDemandEnclosure } from '@/api/optask'
import { apiUrl, uploadurl } from '@/config'
import { getConversionTime } from '@/utils'
import { postUpload } from 'api/tool'
import { getUser } from 'api/user'

export default {
  components: {},

  data() {
    return {
      route_path: this.$route.path.split('/'),
      pid: this.$route.params.id,
      ruleForm: {},
      rules: {
        name: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        time: [
          { required: true, type: 'array', message: '请输入正确的内容', trigger: 'change' }
        ],
        content1: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        content2: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        content3: [
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
      apiurl: apiUrl,
      uploadurl: uploadurl,
      img_file: {},
      count: 0,
      enclosureData: [],
      enclosureForm: {
        project: '',
        create_user: localStorage.getItem('username'),
        file: ''
      },
      ttime: [],
      users: []
    }
  },

  created() {
    this.fetchData()
    this.fetchEnclosureData()
    this.getUsers()
  },
  methods: {
    fetchData() {
      const query = null
      getDemandManager(query, this.pid).then(response => {
        this.ruleForm = response.data
        this.ttime = [this.ruleForm.start_time, this.ruleForm.end_time]
        this.enclosureForm.project = this.ruleForm.id
        this.count = response.data.length
      })
    },
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.ruleForm.start_time = this.ttime[0]
          this.ruleForm.end_time = this.ttime[1]
          putDemandManager(this.ruleForm.id, this.ruleForm).then(response => {
            if (response.statusText === '"Created"') {
              this.$message({
                type: 'success',
                message: '恭喜你，更新成功'
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
      formData.append('username', localStorage.getItem('username'))
      formData.append('file', file)
      formData.append('create_time', getConversionTime(file.lastModified))
      formData.append('type', file.type)
      formData.append('archive', this.route_path[1])
      postUpload(formData).then(response => {
        md.$imglst2Url([[pos, response.data.file]])
      })
    },
    beforeAvatarUpload(file) {
      const formData = new FormData()
      formData.append('username', this.enclosureForm.create_user)
      formData.append('file', file)
      formData.append('create_time', getConversionTime())
      formData.append('type', file.type)
      formData.append('archive', this.route_path[1])
      postUpload(formData).then(response => {
        this.enclosureForm.file = response.data.filepath
        postopsDemandEnclosure(this.enclosureForm)
        if (response.statusText === 'Created') {
          this.$message({
            type: 'success',
            message: '恭喜你，上传成功'
          })
        }
        this.fetchEnclosureData()
      }).catch(error => {
        this.$message.error('上传失败')
        this.$refs.upload.clearFiles()
        console.log(error)
      })
      return true
    },
    fetchEnclosureData() {
      const parms = {
        project__id: this.pid
      }
      getDemandEnclosure(parms).then(response => {
        this.enclosureData = response.data
        this.count = response.data.length
      })
    },
    deleteEnclosure(id) {
      deleteDemandEnclosure(id)
      this.fetchEnclosureData()
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
</style>
