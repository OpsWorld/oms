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

          <el-radio-group v-model="radio" @change="changeStatus" style="margin-left: 20px">
            <el-radio label="0">未接收</el-radio>
            <el-radio label="1">正在处理</el-radio>
            <el-radio label="2">已完成</el-radio>
          </el-radio-group>
        </div>
        <div class="table-search">
          <el-input
            placeholder="搜索 ..."
            v-model="searchdata"
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
                <el-tag :type="TICKET_STATUS_TYPE[scope.row.status]">
                  {{TICKET_STATUS_TEXT[scope.row.status]}}
                </el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button @click="editComplete(scope.row)" type="primary" size="mini"
                         v-if="platformpaychannels_btn_change_complete||role==='super'">
                更新进度
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

    <el-dialog :visible.sync="completeForm" width="30%" @close="fetchData">
      <el-form label-width="90px">
        <el-form-item :model="CompleteForm" label="完成百分比">
          <el-slider
            style="margin-right: 50px"
            v-model="CompleteForm.complete"
            :step="10">
          </el-slider>
          <a>{{CompleteForm.complete}}%</a>
        </el-form-item>
        <el-form-item>
          <el-button @click="changeComplete" type="success" size="mini">确定</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import { getPlatformPayChannel, putPlatformPayChannel, getPlatform } from 'api/threeticket'
import { LIMIT, pagesize, pageformat } from '@/config'
import { mapGetters } from 'vuex'
import { postSendmessage } from 'api/tool'

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
        platform__name: '',
        ordering: '',
        complete: '',
        complete__gt: 0,
        complete__lt: 100
      },
      pagesize: pagesize,
      pageformat: pageformat,
      platformpaychannels_btn_change_complete: false,
      completeForm: false,
      CompleteForm: {
        id: '',
        platform: '',
        type: '',
        complete: 0,
        create_user: ''
      },
      platform: '',
      platforms: [],
      radio: '1',
      complete_status: 'exception',
      TICKET_STATUS_TEXT: { '0': '未接收', '1': '正在处理', '2': '已解决' },
      TICKET_STATUS_TYPE: { '0': 'danger', '1': 'success', '2': 'info' }
    }
  },

  computed: {
    ...mapGetters([
      'elements',
      'role'
    ])
  },
  created() {
    this.platformpaychannels_btn_change_complete = this.elements['对接通道进度-更新进度']
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

    changeComplete() {
      putPlatformPayChannel(this.CompleteForm.id, this.CompleteForm).then(response => {
        this.$message({
          type: 'success',
          message: '更新成功!'
        })
        if (this.CompleteForm.complete === 100) {
          const messageForm = {
            action_user: `${this.CompleteForm.create_user}`,
            title: '【通道完成进度】',
            message: `平台: ${this.CompleteForm.platform}\n通道类型: ${this.CompleteForm.type}\n完成度: ${this.CompleteForm.complete}%`
          }
          postSendmessage(messageForm)
          console.log('通道完成100')
        }
        this.completeForm = false
        this.fetchData()
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '更新失败'
        })
      })
    },
    editComplete(row) {
      this.completeForm = true
      this.CompleteForm = row
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
      if (val === '0') {
        this.listQuery.complete = 0
        this.listQuery.complete__gt = ''
        this.listQuery.complete__lt = ''
        this.complete_status = 'exception'
      } else if (val === '2') {
        this.listQuery.complete = 100
        this.listQuery.complete__gt = ''
        this.listQuery.complete__lt = ''
        this.complete_status = 'success'
      } else {
        this.listQuery.complete = ''
        this.listQuery.complete__gt = 0
        this.listQuery.complete__lt = 100
        this.complete_status = 'exception'
      }
      this.fetchData()
    }
  }
}
</script>

<style lang='scss'>

</style>
