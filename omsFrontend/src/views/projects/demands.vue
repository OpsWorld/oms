<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <div class="head-lavel">
        <div class="table-button">
          <router-link :to="'adddemand'">
            <el-button type="primary" icon="el-icon-plus">新建</el-button>
          </router-link>
          <el-radio-group v-model="listQuery.status" @change="changeStatus" style="margin-left: 20px">
            <el-radio v-for="item in Object.keys(STATUS_TEXT)" :key="item" :label="item">{{STATUS_TEXT[item]}}
            </el-radio>
          </el-radio-group>
        </div>
        <div class="table-search">
          <el-input style="width: 180px;" placeholder="编号、标题、内容或类型"
                    @keyup.enter.native="searchClick"
                    v-model="listQuery.search">
            <i class="el-icon-search el-input__icon" slot="suffix" @click="searchClick"></i>
          </el-input>
        </div>
      </div>
      <div>
        <el-table :data="tableData" border style="width: 100%" @sort-change="handleSortChange">
          <el-table-column prop='pid' label='编号'>
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper">
                <router-link :to="'viewdemand/' + scope.row.id">
                  <a style="color: #257cff">{{scope.row.pid}}</a>
                </router-link>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='name' label='名称'></el-table-column>
          <el-table-column prop='type' label='类型'></el-table-column>
          <el-table-column prop='status' label='状态'>
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper">
                <el-tag size="mini" :type="STATUS_COLOR[scope.row.status]">
                  {{STATUS_TEXT[scope.row.status]}}
                </el-tag>
                <el-tooltip class="item" effect="dark" content="更改状态" placement="top">
                  <el-button type="text" icon="el-icon-edit" class="modifychange"
                             @click="updateDemand(scope.row.id)"></el-button>
                </el-tooltip>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='create_user' label='需求人'></el-table-column>
          <el-table-column prop='create_time' label='创建时间' sortable="custom">
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper" style="text-align: center; color: rgb(0,0,0)">
                <span>{{scope.row.create_time | parseDate}}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='end_time' label='计划完成时间'></el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <router-link :to="'editdemand/' + scope.row.id">
                <el-button type="success" size="small">修改</el-button>
              </router-link>
              <el-button type="danger" size="small" @click="deleteDemand(scope.row.id)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div class="table-footer">
        <div class="table-button">

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
      </div>
    </el-card>

    <el-dialog :visible.sync="statusForm">
      <el-form label-width="90px">
        <el-form-item label="更改状态" prop="status">
          <el-radio-group v-model="updateform.status">
            <el-radio v-for="item in Object.keys(STATUS_TEXT)" :key="item" :label="item">{{STATUS_TEXT[item]}}
            </el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-button @click="statusForm=false">取 消</el-button>
          <el-button type="primary" @click="changeDemand">确 定</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import { getDemandManager, patchDemandManager, deleteDemandManager } from '@/api/project'
import { LIMIT, pagesize, pageformat } from '@/config'
import { getPlatformPayChannel, patchPlatformPayChannel } from 'api/threeticket'
import { getWorkticket, patchWorkticket } from 'api/workticket'
import { postSendmessage } from 'api/tool'

export default {
  components: {},
  data() {
    return {
      tableData: [],
      tabletotal: 0,
      currentPage: 1,
      pagesize: pagesize,
      pageformat: pageformat,
      STATUS_TEXT: {
        0: '未审核',
        1: '已通过',
        2: '未通过',
        3: '已完成'
      },
      STATUS_COLOR: {
        0: 'danger',
        1: 'success',
        2: 'warning',
        3: 'info'
      },
      listQuery: {
        limit: LIMIT,
        offset: '',
        pid: '',
        status: '',
        create_user__username: '',
        action_user__username: '',
        search: '',
        ordering: ''
      },
      updateform: {
        id: '',
        status: '1'
      },
      statusForm: false
    }
  },
  created() {
    this.fetchData()
  },

  methods: {
    fetchData() {
      getDemandManager(this.listQuery).then(response => {
        this.tableData = response.data.results
        this.tabletotal = response.data.count
      })
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
    changeStatus() {
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
    deleteDemand(id) {
      deleteDemandManager(id).then(response => {
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
    updateDemand(id) {
      this.statusForm = true
      this.updateform.id = id
    },
    changeDemand() {
      patchDemandManager(this.updateform.id, this.updateform).then(response => {
        this.$message({
          message: '恭喜你，修改成功',
          type: 'success'
        })
        if (response.data.status === 3) {
          const piddata = {
            pid: response.data.pid
          }
          if (response.data.type === '来自第三方支付对接') {
            const ticketdata = {
              status: 2
            }
            getPlatformPayChannel(piddata).then(res => {
              patchPlatformPayChannel(res.data[0].id, ticketdata).then(dd => {
                const messageForm = {
                  action_user: dd.data.create_user,
                  title: '【通道已完成】' + dd.data.name,
                  message: `平台: ${dd.data.platform}\n通道类型: ${dd.data.type}}`
                }
                postSendmessage(messageForm)
              })
            })
          } else if (response.data.type === '来自工单') {
            const ticketdata = {
              ticket_status: 2
            }
            getWorkticket(piddata).then(res => {
              patchWorkticket(res.data[0].id, ticketdata).then(tt => {
                const messageForm = {
                  action_user: tt.data.create_user,
                  title: '【工单已完成】' + tt.data.name,
                  message: `指派人: ${tt.data.action_user}\n工单地址: http://${window.location.host}/#/worktickets/editworkticket/${tt.data.pid}`
                }
                postSendmessage(messageForm)
              })
            })
          }
        }
        this.statusForm = false
        this.fetchData()
      }).catch(error => {
        this.$message.error('修改失败')
        console.log(error)
      })
    }
  }
}
</script>

<style lang='scss'>
  .modifychange {
    margin: 5px;
  }
</style>
