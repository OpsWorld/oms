<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <div class="head-lavel">
        <div class="table-button">
          <el-button type="primary" icon="el-icon-plus" @click="addForm=true">新建</el-button>

          <el-radio-group v-model="listQuery.showdev" @change="changeStatus" style="margin-left: 20px">
            <el-radio label="">全部</el-radio>
            <el-radio label="false">正式</el-radio>
            <el-radio label="true">测试</el-radio>
          </el-radio-group>
        </div>
        <div class="table-search">
          <el-input
            placeholder="search"
            v-model="searchdata"
            @keyup.enter.native="searchClick">
            <i class="el-icon-search el-input__icon" slot="suffix" @click="searchClick"></i>
          </el-input>
        </div>
      </div>
      <div>
        <el-table :data='tableData' style="width: 100%">
          <el-table-column type="index" width="50"></el-table-column>
          <el-table-column prop='name' label='名称' sortable>
            <template slot-scope="scope">
              <router-link :to="'runjob/' + scope.row.id">
                <a style="color: #257cff">{{scope.row.name}}</a>
              </router-link>
            </template>
          </el-table-column>
          <el-table-column prop='code_url' label='代码地址'></el-table-column>
          <el-table-column prop='desc' label='描述'></el-table-column>
          <el-table-column label="操作" v-if="role==='super'">
            <template slot-scope="scope">
              <router-link :to="'editjob/' + scope.row.id">
                <el-button type="success" size="small" icon="el-icon-setting">配置</el-button>
              </router-link>
              <el-button @click="deleteGroup(scope.row.id)" type="danger" size="small" icon="el-icon-delete">删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div class="table-pagination">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page.sync="currentPage"
          :page-sizes="pagesize"
          :page-size="listQuery.limit"
          :layout="pageformat"
          :total="tabletotal">
        </el-pagination>
      </div>
    </el-card>

    <el-dialog :visible.sync="addForm">
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="ruleForm.name" placeholder="请输入正确的内容"></el-input>
        </el-form-item>
        <el-form-item label="代码地址" prop="code_url">
          <el-input v-model="ruleForm.code_url" placeholder="请输入正确的内容"></el-input>
        </el-form-item>
        <el-form-item label="发布路径" prop="deploy_path">
          <el-input v-model="ruleForm.deploy_path" placeholder="请输入正确的内容"></el-input>
        </el-form-item>
        <el-form-item label="研发可见" prop="showdev">
          <el-switch v-model="ruleForm.showdev" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
        </el-form-item>
        <el-form-item label="描述" prop="desc">
          <el-input v-model="ruleForm.desc" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
          <el-button type="danger" @click="resetForm('ruleForm')">清空</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import { getJob, postJob, deleteJob } from '@/api/job'
import { LIMIT, pagesize, pageformat } from '@/config'
import { mapGetters } from 'vuex'

export default {
  components: {},
  data() {
    return {
      tableData: [],
      tabletotal: 0,
      searchdata: '',
      currentPage: 1,
      listQuery: {
        limit: LIMIT,
        offset: '',
        search: ''
      },
      pagesize: pagesize,
      pageformat: pageformat,
      addForm: false,
      ruleForm: {
        name: '',
        code_url: '',
        deploy_path: '',
        showdev: false,
        desc: ''
      },
      rules: {
        name: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        code_url: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        deploy_path: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    ...mapGetters([
      'role'
    ])
  },
  created() {
    this.fetchData()
  },

  methods: {
    fetchData() {
      getJob(this.listQuery).then(response => {
        this.tableData = response.data.results
        this.tabletotal = response.data.count
      })
    },
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          postJob(this.ruleForm).then(response => {
            this.$message({
              type: 'success',
              message: '恭喜你，新建成功'
            })
            this.$router.push('/jobs/editjob/' + response.data.id)
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
    deleteGroup(id) {
      deleteJob(id).then(response => {
        this.$message({
          message: '恭喜你，删除成功',
          type: 'success'
        })
        this.fetchData()
      }).catch(error => {
        this.$message.error('删除失败')
        console.log(error)
      })
    },
    searchClick() {
      this.listQuery.search = this.searchdata
      this.fetchData()
    },
    handleSizeChange(val) {
      this.listQuery.limit = val
      this.fetchData()
    },
    handleCurrentChange(val) {
      this.listQuery.offset = (val - 1) * LIMIT
      this.fetchData()
    },
    changeStatus(val) {
      this.listQuery.showdev = val
      this.fetchData()
    }
  }
}
</script>

<style lang='scss'>

</style>
