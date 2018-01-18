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
          <el-table-column prop='platform' label='平台'></el-table-column>
          <el-table-column prop='type' label='通道类型'></el-table-column>
          <el-table-column prop='complete' label='完成百分比' sortable="custom">
            <template slot-scope="scope">
              <el-progress type="circle" :percentage="scope.row.complete" :width="40"></el-progress>
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button @click="editComplete(scope.row)" type="primary" size="mini"
                         v-if="paychannel_btn_change_complete||role==='super'">
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
          layout="prev, pager, next, sizes"
          :total="tabletotal">
        </el-pagination>
      </div>
    </el-card>

    <el-dialog :visible.sync="completeForm" width="30%">
      <el-form label-width="100px">
        <el-form-item :model="CompleteForm" label="完成百分比">
          <el-slider
            v-model="CompleteForm.complete"
            :step="10">
          </el-slider>
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
import { LIMIT } from '@/config'
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
        ordering: ''
      },
      limit: LIMIT,
      offset: '',
      pagesize: [10, 25, 50, 100],
      paychannel_btn_change_complete: false,
      completeForm: false,
      CompleteForm: {
        id: '',
        platform: '',
        type: '',
        complete: 0
      },
      platform: '',
      platforms: []
    }
  },

  computed: {
    ...mapGetters([
      'elements',
      'role'
    ])
  },
  created() {
    this.paychannel_btn_change_complete = this.elements['支付通道列表-更新进度']
    this.fetchData()
    this.fetchPlatformData()
  },

  methods: {
    fetchData() {
      getPlatformPayChannel(this.listQuery).then(response => {
        this.tableData = response.data.results
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
        const messageForm = {
          action_user: `${this.CommentForm.create_user}`,
          title: '【通道完成进度】',
          message: `平台: ${this.CompleteForm.platform}\n通道类型: ${this.CompleteForm.type}\n完成度: ${this.CompleteForm.complete}`
        }
        postSendmessage(messageForm)
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
    changePlatform(res) {
      if (res === '全部') {
        this.listQuery.platform__name = ''
      } else {
        this.listQuery.platform__name = res
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
    handleSortChange(res) {
      if (res.order === 'ascending') {
        this.listQuery.ordering = res.prop
      } else if (res.order === 'descending') {
        this.listQuery.ordering = '-' + res.prop
      } else {
        this.listQuery.ordering = ''
      }
      this.fetchData()
    }
  }
}
</script>

<style lang='scss'>
  .head-lavel {
    padding-bottom: 50px;
  }

  .table-button {
    float: left;
  }

  .table-search {
    float: right;
  }

  .table-pagination {
    padding: 10px 0;
    float: right;
  }
</style>
