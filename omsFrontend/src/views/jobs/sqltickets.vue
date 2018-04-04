<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <div class="head-lavel">
        <div class="table-button">
          <el-button type="primary" icon="el-icon-plus" @click="addForm=true">新建</el-button>
        </div>
        <div class="table-search">
          <el-input
            placeholder="search"
            v-model="listQuery.search"
            @keyup.enter.native="searchClick">
            <i class="el-icon-search el-input__icon" slot="suffix" @click="searchClick"></i>
          </el-input>
        </div>
      </div>
      <div>
        <el-table :data="tableData" border style="width: 100%" @sort-change="handleSortChange">
          <el-table-column prop='id' label='ID'></el-table-column>
          <el-table-column prop='name' label='标题'></el-table-column>
          <el-table-column prop='version' label='项目和版本'></el-table-column>
          <el-table-column prop='content' label='内容'>
            <template slot-scope="scope">
              <div slot="reference">
                <el-popover
                  placement="top"
                  width="300"
                  trigger="hover"
                  :content="scope.row.content">
                  <el-button size="mini" slot="reference">{{scope.row.content.slice(0, 5)}}...</el-button>
                </el-popover>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='status' label='工单状态' sortable="custom">
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper" style="text-align: center; color: rgb(0,0,0)">
                <el-tag :type="STATUS_COLOR[scope.row.status]">
                  {{STATUS_TEXT[scope.row.status]}}
                </el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='create_user' label='创建人'></el-table-column>
          <el-table-column prop='desc' label='说明'></el-table-column>
          <el-table-column prop='create_time' label='创建时间' sortable="custom">
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper" style="text-align: center; color: rgb(0,0,0)">
                <span>{{scope.row.create_time | parseDate}}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="300">
            <template slot-scope="scope">
              <el-button v-if="scope.row.status===0&&role==='super'" @click="editBefore(scope.row)" type="success"
                         size="mini">修改
              </el-button>
              <!--<el-button v-if="scope.row.status===0&&role==='devmanager'" @click="changeJobPass(scope.row)"-->
              <!--type="primary" size="mini">-->
              <!--通过-->
              <!--</el-button>-->
              <!--<el-button v-if="scope.row.status===0&&role==='devmanager'" @click="changeJobNopass(scope.row)"-->
              <!--type="danger" size="mini">-->
              <!--未通过-->
              <!--</el-button>-->
              <el-button v-if="role==='super'" @click="changeSqlOnline(scope.row)"
                         type="success" size="mini">
                已执行
              </el-button>
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

    <el-dialog :visible.sync="onlineForm" @close="cleanForm">
      <el-form :model="rowdata" ref="ruleForm" label-width="100px">
        <el-form-item label="通知对象">
          <el-checkbox v-model="send_acc">财务</el-checkbox>
          <el-checkbox v-model="send_cs">客服</el-checkbox>
          <el-checkbox v-model="send_it">部门群组</el-checkbox>
        </el-form-item>
        <el-form-item>
          <el-button @click="onlineForm=false">取 消</el-button>
          <el-button type="primary" @click="updateOnline">确 定</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-dialog :visible.sync="nopassForm" @close="cleanForm">
      <el-form :model="nopass" ref="ruleForm" label-width="100px">
        <el-form-item label="原因">
          <el-input v-model="nopass.content" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button @click="nopassForm=false">取 消</el-button>
          <el-button type="primary" @click="updateNopass">确 定</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-dialog :visible.sync="addForm">
      <add-group @DialogStatus="getDialogStatus"></add-group>
    </el-dialog>

    <el-dialog :visible.sync="editForm">
      <edit-group :ruleForm="ticketdata" @DialogStatus="getDialogStatus"></edit-group>
    </el-dialog>

    <el-dialog :visible.sync="showForm">
      <div v-if='enclosureData.length>0' class="ticketenclosure">
        <ul>
          <li v-for="item in enclosureData" :key="item.id" v-if="item.file" style="list-style:none">
            <i class="fa fa-paperclip"></i>
            <a :href="apiurl + '/upload/' + item.file" :download="item.file">{{item.file.split('/')[1]}}</a>
          </li>
        </ul>
      </div>
      <div v-else>
        没有上传附件
      </div>
    </el-dialog>

  </div>
</template>

<script>
import { getDeployTicket, patchDeployTicket, getDeployTicketEnclosur } from '@/api/job'
import { LIMIT, pagesize, pageformat, apiUrl } from '@/config'
import { postSendmessage } from 'api/tool'
import { mapGetters } from 'vuex'
import addGroup from './components/addjobticket.vue'
import editGroup from './components/editjobticket.vue'

export default {
  components: { addGroup, editGroup },
  data() {
    return {
      tableData: [],
      tabletotal: 0,
      currentPage: 1,
      ticket_status: '',
      pagesize: pagesize,
      pageformat: pageformat,
      rowdata: {
        id: '',
        status: 3
      },
      STATUS_TEXT: {
        0: '未上线',
        1: '通过',
        2: '未通过',
        3: '已上线'
      },
      STATUS_COLOR: {
        0: 'danger',
        1: 'success',
        2: 'info',
        3: 'primary'
      },
      listQuery: {
        limit: LIMIT,
        offset: '',
        create_user__username: '',
        search: '',
        ordering: ''
      },
      onlineForm: false,
      addForm: false,
      apiurl: apiUrl,
      enclosureData: [],
      showForm: false,
      editForm: false,
      send_acc: false,
      send_cs: false,
      send_it: false,
      nopassForm: false,
      nopass: {
        id: '',
        content: ''
      },
      ticketdata: {}
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
      getDeployTicket(this.listQuery).then(response => {
        this.tableData = response.data.results
        this.tabletotal = response.data.count
      })
    },
    EnclosureData(id) {
      const parms = {
        ticket__id: id
      }
      getDeployTicketEnclosur(parms).then(response => {
        this.enclosureData = response.data
      })
    },
    getEncloseur(id) {
      this.showForm = true
      this.EnclosureData(id)
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
    changeJobPass(row) {
      const rowdata = {
        status: 1
      }
      patchDeployTicket(row.id, rowdata).then(() => {
        const messageForm = {
          action_user: 'itsupport',
          title: '【上线申请通过】' + row.name,
          message: `上线内容: ${row.version}`
        }
        postSendmessage(messageForm)
        this.fetchData()
      })
    },
    changeJobNopass(row) {
      this.nopass.id = row.id
      this.nopass.name = row.name
      this.nopassForm = true
    },
    updateNopass() {
      const rowdata = {
        status: 2
      }
      patchDeployTicket(this.nopass.id, rowdata).then(() => {
        const messageForm = {
          action_user: 'itsupport',
          title: '【申请未通过】' + this.nopass.name,
          message: `原因: ${this.nopass.content}`
        }
        postSendmessage(messageForm)
        this.nopassForm = false
        this.fetchData()
      })
    },
    changeSqlOnline(row) {
      this.onlineForm = true
      this.rowdata.id = row.id
      this.rowdata.name = row.name
      this.rowdata.content = row.content
    },
    updateOnline() {
      patchDeployTicket(this.rowdata.id, this.rowdata).then(() => {
        if (this.send_acc) {
          const messageForm = {
            action_user: 'molly',
            title: '【已上线】' + this.rowdata.name,
            message: `上线内容: ${this.rowdata.content}`
          }
          postSendmessage(messageForm)
        }
        if (this.send_cs) {
          const messageForm = {
            action_user: 'linda',
            title: '【已上线】' + this.rowdata.name,
            message: `上线内容: ${this.rowdata.content}`
          }
          postSendmessage(messageForm)
        }
        if (this.send_it) {
          const messageForm = {
            action_user: 'ITDept_SkypeID',
            title: '【已上线】' + this.rowdata.name,
            message: `上线内容: ${this.rowdata.content}`
          }
          postSendmessage(messageForm)
        }
        this.fetchData()
        this.onlineForm = false
      })
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
    editBefore(row) {
      this.editForm = true
      this.ticketdata = row
    },
    cleanForm() {
      this.send_acc = false
      this.send_cs = false
    },
    getDialogStatus(data) {
      this.addForm = data
      this.editForm = data
      this.fetchData()
    }
  }
}
</script>

<style lang='scss'>
</style>
