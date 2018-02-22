<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <div class="head-lavel">
        <div class="table-button">
          <el-select v-model="platform" placeholder="请选择平台进行筛选" @change="changePlatform">
            <el-option
              v-for="item in platforms"
              :key="item.id"
              :value="item.name">
            </el-option>
          </el-select>

          <el-radio-group v-model="listQuery.status" @change="changeStatus" style="margin-left: 20px">
            <el-radio label="0">未接收</el-radio>
            <el-radio label="1">正在处理</el-radio>
            <el-radio label="2">已完成</el-radio>
          </el-radio-group>
        </div>
        <div class="table-search">
          <el-input
            placeholder="搜索编号"
            v-model="listQuery.pid"
            @keyup.enter.native="searchClick">
            <i class="el-icon-search el-input__icon" slot="suffix" @click="searchClick"></i>
          </el-input>
        </div>
      </div>
      <div>
        <el-table :data="tableData" border style="width: 100%" @sort-change="handleSortChange">
          <el-table-column prop='pid' label='编号'></el-table-column>
          <el-table-column prop='platform' label='平台'></el-table-column>
          <el-table-column prop='type' label='通道类型'></el-table-column>
          <el-table-column prop='level' label='紧急度'>
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper" style="text-align: center; color: rgb(0,0,0)">
                <el-rate
                  v-model="scope.row.level"
                  :colors="['#99A9BF', '#F7BA2A', '#ff1425']"
                  disabled>
                </el-rate>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='status' label='状态' sortable="custom">
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper" style="text-align: center; color: rgb(0,0,0)">
                <el-tag :type="STATUS_TYPE[scope.row.status]">
                  {{STATUS_TEXT[scope.row.status]}}
                </el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200">
            <template slot-scope="scope">
              <el-button type="success" size="mini" @click="updateForm(scope.row)">修改</el-button>
              <el-button v-if="role==='super' && scope.row.status === 0" type="primary" size="mini"
                         @click="copyPaychannel(scope.row)">
                乾坤大挪移
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

    <el-dialog :visible.sync="editForm" width="30%" @close="fetchData">
      <el-form :model="ruleForm" ref="ruleForm" label-width="100px">
        <el-form-item label="编号" prop="pid">
          <el-input v-model="ruleForm.pid" disabled></el-input>
        </el-form-item>
        <el-form-item label="名称" prop="name">
          <el-input v-model="ruleForm.name" disabled></el-input>
        </el-form-item>
        <el-form-item label="紧急度" prop="level">
          <el-rate
            v-model="ruleForm.level"
            :colors="['#99A9BF', '#F7BA2A', '#ff1425']"
            show-text
            :texts="['E', 'D', 'C', 'B', 'A']">
          </el-rate>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="ruleForm.status" filterable placeholder="更新状态">
            <el-option v-for="(item, index) in STATUS_TEXT" :key="index" :label="item" :value="index">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import { getPlatformPayChannel, getPlatform, putPlatformPayChannel, getThreePayEnclosure } from 'api/threeticket'
import { postDemandManager, postDemandEnclosure } from '@/api/project'
import { LIMIT, pagesize, pageformat } from '@/config'
import { mapGetters } from 'vuex'

export default {
  components: {},
  data() {
    return {
      tableData: [],
      tabletotal: 0,
      currentPage: 1,
      listQuery: {
        limit: LIMIT,
        offset: '',
        platform__name: '',
        ordering: '',
        status: '0',
        pid: ''
      },
      pagesize: pagesize,
      pageformat: pageformat,
      editForm: false,
      ruleForm: {},
      platform: '',
      platforms: [],
      STATUS_TEXT: { '0': '未接收', '1': '正在处理', '2': '已完成' },
      STATUS_TYPE: { '0': 'danger', '1': 'success', '2': 'info' },
      enclosureData: []
    }
  },

  computed: {
    ...mapGetters([
      'role'
    ])
  },
  created() {
    this.fetchData()
    this.fetchPlatformData()
  },

  methods: {
    fetchData() {
      getPlatformPayChannel(this.listQuery).then(response => {
        this.tableData = response.data.results
        this.tabletotal = response.data.count
      })
    },

    fetchPlatformData() {
      getPlatform().then(response => {
        this.platforms = [{ 'name': '全部' }].concat(response.data)
      })
    },
    changePlatform(val) {
      if (val === '全部') {
        this.listQuery.platform__name = ''
      } else {
        this.listQuery.platform__name = val
      }
      this.fetchData()
    },
    searchClick() {
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
    handleSortChange(val) {
      if (val.order === 'ascending') {
        this.listQuery.ordering = val.prop
      } else if (val.order === 'descending') {
        this.listQuery.ordering = '-' + val.prop
      } else {
        this.listQuery.ordering = ''
      }
      this.fetchData()
    },
    changeStatus(val) {
      this.fetchData()
    },
    updateForm(row) {
      this.editForm = true
      this.ruleForm = row
    },
    submitForm() {
      putPlatformPayChannel(this.ruleForm.id, this.ruleForm).then(response => {
        this.$message({
          type: 'success',
          message: '恭喜你，更新成功'
        })
        this.editForm = false
      })
    },
    copyPaychannel(row) {
      const DemandForm = {
        pid: row.pid,
        name: row.name,
        content: row.name,
        type: '来自第三方支付对接',
        create_user: row.create_user,
        create_time: row.create_time
      }
      const parms = {
        ticket__name: row.platform
      }
      getThreePayEnclosure(parms).then(res => {
        postDemandManager(DemandForm).then(response => {
          this.$message({
            type: 'success',
            message: '恭喜你，转移成功'
          })
          if (res.data.length > 0) {
            for (const item of res.data) {
              const Demandenclosure = {
                project: response.data.id,
                file: item.file,
                create_user: item.create_user,
                create_time: item.create_time
              }
              postDemandEnclosure(Demandenclosure)
            }
          }
        }).catch(error => {
          const errordata = Object.values(error.response.data)[0]
          this.$message.error(errordata[0])
          console.log(errordata)
        })
      })
    }
  }
}
</script>

<style lang='scss'>

</style>
