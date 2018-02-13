<template>
  <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
    <el-form-item label="用户组" prop="usergroups">
      <el-select v-model="ruleForm.usergroups" placeholder="请选择用户组">
        <el-option v-for="item in groups" :key="item.name" :value="item.name"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="选择文档" prop="hosts">
      <sesect-datas :selectdata="ruleForm.objs" :alldata="allwikis" @getDatas="getWikis"></sesect-datas>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm('ruleForm')">立即创建</el-button>
      <el-button @click="resetForm('ruleForm')">重置</el-button>
    </el-form-item>
  </el-form>
</template>
<script>
import sesectDatas from 'views/components/datatransfer.vue'
import { getGroup } from 'api/user'
import { getWiki } from 'api/wiki'
import { postWikiPerm } from '@/api/perm'

export default {
  components: { sesectDatas },

  data() {
    return {
      ruleForm: {
        usergroups: '',
        objs: []
      },
      rules: {
        usergroups: [
          { required: true, message: '请输入一个正确的内容', trigger: 'blur' }
        ]
      },
      groups: [],
      allwikis: []
    }
  },
  created() {
    this.getGroups()
    this.getAllwikis()
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          postWikiPerm(this.ruleForm).then(response => {
            this.$message({
              message: '恭喜你，添加成功',
              type: 'success'
            })
            this.ruleForm = {
              usergroups: '',
              objs: []
            }
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
      this.getAllwikis()
    },
    getWikis(data) {
      this.ruleForm.objs = data
    },
    getGroups() {
      getGroup().then(response => {
        this.groups = response.data
      })
    },
    getAllwikis() {
      getWiki().then(response => {
        this.allwikis = []
        const results = response.data
        for (var i = 0, len = results.length; i < len; i++) {
          this.allwikis.push({
            key: results[i].title
          })
        }
      })
    }
  }
}
</script>
