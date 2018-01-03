<template>
  <div class="components-container" style='height:100vh'>
    <el-card style="min-height: 800px">
      <el-form :model="rowdata" :rules="rules" ref="ruleForm" label-width="100px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="rowdata.title"></el-input>
        </el-form-item>
        <el-form-item label="类型" prop="type">
          <el-select v-model="rowdata.type" placeholder="请选择类型">
            <el-option v-for="item in types" :key="item.id" :value="item.name"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="正文" prop="content">
          <mavon-editor style="min-height: 500px" v-model="rowdata.content" code_style="monokai"
                        :toolbars="toolbars" @imgAdd="imgAdd" ref="md"></mavon-editor>
          <a class="tips"> Tip：截图可以直接 Ctrl + v 粘贴到内容里面</a>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm('ruleForm')">立即更新</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>
<script>
import { getConversionTime } from '@/utils'
import { postUpload } from 'api/tool'
import { getTickettype } from 'api/workticket'
import { getWiki, putWiki } from 'api/wiki'

export default {
  data() {
    return {
      rowdata: {},
      toolbars: {
        preview: true, // 预览
        bold: true, // 粗体
        italic: true, // 斜体
        header: true, // 标题
        underline: true, // 下划线
        strikethrough: true, // 中划线
        ol: true, // 有序列表
        fullscreen: true, // 全屏编辑
        help: true
      },
      types: [],
      route_path: this.$route.path.split('/'),
      wikiid: this.$route.params.wikiid,
      rules: {
        rules: {
          title: [
            { required: true, message: '请输入正确的内容', trigger: 'blur' }
          ],
          type: [
            { required: true, message: '请选择正确的内容', trigger: 'change' }
          ],
          content: [
            { required: true, message: '请输入正确的内容', trigger: 'blur' }
          ]
        }
      }
    }
  },
  created() {
    this.fetchData()
    this.getTicketType()
  },
  methods: {
    fetchData() {
      const parms = null
      getWiki(parms, this.wikiid).then(response => {
        this.rowdata = response.data
      })
    },
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          putWiki(this.rowdata.id, this.rowdata).then(response => {
            this.$message({
              message: '恭喜你，更新成功',
              type: 'success'
            })
            this.$router.push('/wikis/wikiadmin')
          }).catch(error => {
            this.$message.error('更新失败')
            console.log(error)
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    getTicketType() {
      getTickettype().then(response => {
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
    }
  }
}
</script>
