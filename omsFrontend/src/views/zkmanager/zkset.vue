<template>
  <div class="components-container" style='height:100vh'>
    <el-card style="width: 400px">
      <div slot="header">
        <span style="margin-right: 10px">打卡时间设置</span>
        <el-button-group>
          <el-button v-if="!tabletotal" type="primary" plain size="mini" @click="addGroup">添加</el-button>
          <el-button v-if="tabletotal" type="success" plain size="mini" @click="editGroup">编辑</el-button>
          <el-button v-if="tabletotal" type="danger" plain size="mini" @click="rmPunchSet">删除</el-button>
        </el-button-group>
      </div>
      <div>
        <el-form v-if="tabletotal" label-position="left" label-width="120px">
          <el-form-item label="上班时间">
            <span>{{tableData.swork_time }}</span>
          </el-form-item>
          <el-form-item label="下班时间">
            <span>{{tableData.ework_time }}</span>
          </el-form-item>
          <el-form-item label="签到开始时间">
            <span>{{tableData.swork_stime }}</span>
          </el-form-item>
          <el-form-item label="签到结束时间">
            <span>{{tableData.swork_etime }}</span>
          </el-form-item>
          <el-form-item label="签退开始时间">
            <span>{{tableData.ework_stime }}</span>
          </el-form-item>
          <el-form-item label="签退结束时间">
            <span>{{tableData.ework_etime }}</span>
          </el-form-item>
          <!--<el-form-item label="允许超时分钟">-->
          <!--<span>{{tableData.timeout }}</span>-->
          <!--</el-form-item>-->
        </el-form>
      </div>
    </el-card>

    <el-dialog :visible.sync="showForm">
      <el-form :model="ruleForm" ref="ruleForm" label-width="100px">
        <el-form-item label="上班时间" prop="swork_time">
          <el-time-select
            v-model="ruleForm.swork_time"
            :picker-options="{
    start: '08:30',
    step: '00:30',
    end: '12:30'
  }"
            placeholder="选择时间">
          </el-time-select>
        </el-form-item>
        <el-form-item label="下班时间" prop="ework_time">
          <el-time-select
            v-model="ruleForm.ework_time"
            :picker-options="{
    start: '18:30',
    step: '00:30',
    end: '20:30'
  }"
            placeholder="选择时间">
          </el-time-select>
        </el-form-item>
        <el-form-item label="签到开始时间" prop="swork_stime">
          <el-time-select
            v-model="ruleForm.swork_stime"
            :picker-options="{
    start: '06:30',
    step: '00:30',
    end: '09:30'
  }"
            placeholder="选择时间">
          </el-time-select>
        </el-form-item>
        <el-form-item label="签到结束时间" prop="swork_etime">
          <el-time-select
            v-model="ruleForm.swork_etime"
            :picker-options="{
    start: '09:30',
    step: '00:30',
    end: '12:30'
  }"
            placeholder="选择时间">
          </el-time-select>
        </el-form-item>
        <el-form-item label="签退开始时间" prop="ework_stime">
          <el-time-select
            v-model="ruleForm.ework_stime"
            :picker-options="{
    start: '14:30',
    step: '00:30',
    end: '18:30'
  }"
            placeholder="选择时间">
          </el-time-select>
        </el-form-item>
        <el-form-item label="签退结束时间" prop="ework_etime">
          <el-time-select
            v-model="ruleForm.ework_etime"
            :picker-options="{
    start: '18:30',
    step: '00:30',
    end: '23:30'
  }"
            placeholder="选择时间">
          </el-time-select>
        </el-form-item>
        <!--<el-form-item label="允许超时分钟" prop="timeout">-->
        <!--<el-input v-model="ruleForm.timeout"></el-input>-->
        <!--</el-form-item>-->
        <el-form-item>
          <el-button v-if="addForm" type="primary" @click="addPunchSet('ruleForm')">创建</el-button>
          <el-button v-if="editForm" type="primary" @click="editPunchSet('ruleForm')">更新</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import { getzkPunchSet, postzkPunchSet, putzkPunchSet, deletezkPunchSet } from 'api/zk'

export default {
  components: {},
  data() {
    return {
      tableData: {},
      tabletotal: 0,
      ruleForm: {
        swork_time: '',
        ework_time: '',
        swork_stime: '',
        swork_etime: '',
        ework_stime: '',
        ework_etime: '',
        timeout: ''
      },
      addForm: false,
      editForm: false,
      showForm: false
    }
  },

  created() {
    this.fetchData()
  },

  methods: {
    fetchData() {
      getzkPunchSet().then(response => {
        this.tableData = response.data[0]
        this.tabletotal = response.data.length
      })
    },
    addGroup() {
      this.addForm = true
      this.showForm = true
    },
    editGroup() {
      this.editForm = true
      this.showForm = true
      this.ruleForm = this.tableData
    },
    addPunchSet() {
      postzkPunchSet(this.ruleForm).then(response => {
        this.fetchData()
        this.addForm = false
        this.showForm = false
      })
    },
    editPunchSet() {
      putzkPunchSet(this.ruleForm.id, this.ruleForm).then(response => {
        this.fetchData()
        this.editForm = false
        this.showForm = false
      })
    },
    rmPunchSet() {
      deletezkPunchSet(this.tableData.id).then(response => {
        this.$message({
          message: '恭喜你，删除成功',
          type: 'success'
        })
        this.fetchData()
      }).catch(error => {
        this.$message.error('删除失败')
        console.log(error)
      })
    }
  }
}
</script>

<style lang='scss'>

</style>
