<template>
  <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
    <el-form-item label="关联任务" prop="project">
      <el-input v-if="Object.keys(project).length>0" v-model="ruleForm.project" disabled></el-input>
      <el-select v-else v-model="ruleForm.project" filterable placeholder="请选择关联任务" @change="changeProject">
        <el-option v-for="item in projects" :key="item.id" :value="item.pid"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="关联test" prop="test">
      <el-select v-model="ruleForm.test" filterable placeholder="请选择关联test">
        <el-option v-for="item in testData" :key="item.id" :value="item.id"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="名称" prop="name">
      <el-input v-model="ruleForm.name"></el-input>
    </el-form-item>
    <el-form-item label="严重程度" prop="degree">
      <el-rate
        v-model="ruleForm.degree"
        :colors="['#99A9BF', '#F7BA2A', '#ff1425']"
        show-text
        :texts="['E', 'D', 'C', 'B', 'A']">
      </el-rate>
      <a class="tips">Tip：星星代表问题严重程度，星星越多，越严重</a>
    </el-form-item>
    <el-form-item label="优先级" prop="nice">
      <el-select v-model="ruleForm.nice" placeholder="请选择优先级">
        <el-option v-for="item in nices" :key="item.id" :label="item.label" :value="item.value"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="测试人员" prop="test_user">
      <el-select v-model="ruleForm.test_user" filterable placeholder="请选择用户">
        <el-option v-for="item in users" :key="item.id" :value="item.username"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="分配给" prop="action_user">
      <el-select v-model="ruleForm.action_user" filterable placeholder="请选择用户">
        <el-option v-for="item in users" :key="item.id" :value="item.username"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="测试时间" prop="test_time">
      <el-date-picker
        v-model="ruleForm.test_time"
        type="date"
        value-format="yyyy-MM-dd"
        placeholder="选择日期时间">
      </el-date-picker>
    </el-form-item>
    <el-form-item label="关闭时间" prop="end_time">
      <el-date-picker
        v-model="ruleForm.end_time"
        type="date"
        value-format="yyyy-MM-dd"
        placeholder="选择日期时间">
      </el-date-picker>
    </el-form-item>
    <el-form-item label="描述" prop="desc">
      <mavon-editor style="z-index: 1" v-model="ruleForm.desc" code_style="monokai" :toolbars="toolbars"
                    @imgAdd="imgAdd" ref="md"></mavon-editor>
      <a class="tips"> Tip：截图可以直接 Ctrl + v 粘贴到问题处理里面</a>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm('ruleForm')">立即创建</el-button>
      <el-button @click="resetForm('ruleForm')">重置</el-button>
    </el-form-item>
  </el-form>
</template>
<script>
import { getUser } from 'api/user'
import { getProject, postBugManager, getTestManager } from '@/api/project'
import { postUpload, postSendmessage } from 'api/tool'
import { getConversionTime } from '@/utils'

export default {
  props: {
    project: {
      type: Object,
      default: () => {
        return {}
      }
    },
    tests: {
      type: Array,
      default: () => {
        return []
      }
    }
  },
  data() {
    return {
      route_path: this.$route.path.split('/'),
      ruleForm: {
        project: null,
        name: '',
        summary: '',
        degree: 2,
        nice: '',
        test_user: '',
        action_user: '',
        test_time: null,
        end_time: null,
        desc: ''
      },
      rules: {
        name: [
          { required: true, message: '请输入一个正确的内容', trigger: 'blur' }
        ]
      },
      projects: [],
      nices: [
        { 'label': '低', value: '0' },
        { 'label': '中', value: '1' },
        { 'label': '高', value: '2' }
      ],
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
      testData: []
    }
  },
  created() {
    if (this.project) {
      this.ruleForm.project = this.project.pid
      this.testData = this.tests
    }
    this.getUsers()
    this.getProjects()
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          postBugManager(this.ruleForm).then(response => {
            this.$message({
              message: '恭喜你，添加成功',
              type: 'success'
            })
            const messageForm = {
              action_user: response.data.action_user,
              title: '【出bug啦】' + response.data.name,
              message: `地址: ${window.location.href}`
            }
            postSendmessage(messageForm)
            this.$emit('DialogStatus', false)
          }).catch(error => {
            this.$message.error('添加失败')
            console.log(error)
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
    getProjects() {
      getProject().then(response => {
        this.projects = response.data
      })
    },
    changeProject(val) {
      this.getTest(val)
    },
    getTest(pid) {
      const pramas = {
        project__pid: pid
      }
      getTestManager(pramas).then(response => {
        this.testData = response.data
      })
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
    }
  }
}
</script>
