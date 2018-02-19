<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px">
        <el-form-item label="标题" prop="name">
          <el-input v-model="ruleForm.name" placeholder="请输入标题"></el-input>
        </el-form-item>
        <el-form-item label="指派人" prop="action_user">
          <!--<el-select v-model="ruleForm.action_user" filterable placeholder="请选择指派人">-->
            <!--<el-option v-for="item in users" :key="item.id" :value="item.username"></el-option>-->
          <!--</el-select>-->
          <!--<a class="tips"> Tip：当前工单处理人，默认是指派给ITSupport群组</a>-->
          <el-input v-model="ruleForm.action_user" disabled></el-input>
        </el-form-item>
        <el-form-item label="工单类型" prop="type">
          <el-select v-model="ruleForm.type" placeholder="请选择工单类型">
            <el-option v-for="item in types" :key="item.id" :value="item.name"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="工单内容" prop="content">
          <mavon-editor style="z-index: 1" v-model="ruleForm.content" code_style="monokai"
                        :toolbars="toolbars" @imgAdd="imgAdd" ref="md"></mavon-editor>
          <a class="tips"> Tip：截图可以直接 Ctrl + v 粘贴到工单内容里面</a>
        </el-form-item>
        <el-form-item label="工单等级" prop="level">
          <el-rate
            v-model="ruleForm.level"
            :colors="['#99A9BF', '#F7BA2A', '#ff1425']"
            show-text
            :texts="['E', 'D', 'C', 'B', 'A']">
          </el-rate>
          <a class="tips">Tip：星数代表问题紧急程度，星数越多，代表越紧急</a>
        </el-form-item>
        <el-form-item>
          <hr class="heng"/>
          <el-upload
            ref="upload"
            :action="uploadurl"
            :on-success="handleSuccess"
            :on-remove="handleRemove"
            :file-list="fileList">
            <el-button slot="trigger" size="small" type="primary" :disabled="count>2?true:false">
              上传文件
            </el-button>
            (可以不用上传)
            <div slot="tip" class="el-upload__tip">
              <p>上传文件不超过10m，<a style="color: red">最多只能上传3个文件</a></p>
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
import { postWorkticket, postTicketenclosure, getTickettype } from 'api/workticket'
import { postUpload, postSendmessage } from 'api/tool'
import { getUser } from 'api/user'
import { uploadurl } from '@/config'
import { mapGetters } from 'vuex'
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
        level: 2,
        action_user: 'admin',
        edit_user: '',
        create_group: [],
        pid: ''
      },
      rules: {
        name: [
          { required: true, message: '请输入工单标题', trigger: 'blur' }
        ],
        content: [
          { required: true, message: '请输入工单内容', trigger: 'blur' }
        ],
        type: [
          { required: true, message: '请选择工单类型', trigger: 'blur' }
        ],
        level: [
          { required: true, type: 'number', message: '请确认工单等级', trigger: 'blur' }
        ]
      },
      users: [],
      fileList: [],
      count: 0,
      enclosureFile: [],
      enclosureForm: {
        ticket: '',
        create_user: localStorage.getItem('username'),
        file: ''
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
      img_file: {},
      formDataList: [],
      to_list: '',
      cc_list: '',
      uploadurl: uploadurl,
      types: []
    }
  },

  computed: {
    ...mapGetters([
      'groups'
    ])
  },
  created() {
    this.getTicketUsers()
    this.getTicketType()
  },
  methods: {
    postForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.ruleForm.pid = getConversionTime()
          this.ruleForm.create_group = this.groups
          postWorkticket(this.ruleForm).then(response => {
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
                this.enclosureForm.ticket = response.data.id
                postTicketenclosure(this.enclosureForm)
              })
            }
            const messageForm = {
              action_user: this.ruleForm.action_user,
              title: '【新工单】' + this.ruleForm.name,
              message: `提交人: ${this.ruleForm.create_user}\n指派人: ${this.ruleForm.action_user}\n工单地址: http://${window.location.host}/#/worktickets/editworkticket/${this.ruleForm.pid}`
            }
            postSendmessage(messageForm)
            this.$router.push('/worktickets/workticket')
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
    getTicketUsers() {
      getUser().then(response => {
        this.users = response.data
      })
    },

    getTicketType() {
      getTickettype().then(response => {
        this.types = response.data
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
    imgAdd(pos, file) {
      var md = this.$refs.md
      const formData = new FormData()
      formData.append('username', this.enclosureForm.create_user)
      formData.append('file', file)
      formData.append('create_time', getConversionTime(file.lastModified))
      formData.append('type', file.type)
      formData.append('archive', this.route_path[1])
      postUpload(formData).then(response => {
        md.$imglst2Url([[pos, response.data.file]])
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
