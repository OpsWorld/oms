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
                  <el-button size="mini" slot="reference">{{scope.row.content.slice(0, 10)}}...</el-button>
                </el-popover>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='status' label='工单状态' sortable="custom">
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper" style="text-align: center; color: rgb(0,0,0)">
                <el-tag>
                  {{STATUS_TEXT[scope.row.status]}}
                </el-tag>
                <el-tooltip class="item" effect="dark" content="更新状态" placement="top">
                  <el-button v-if="scope.row.status===0" @click="changeStatus(scope.row)" type="text"
                             icon="el-icon-edit"
                             class="modifychange"></el-button>
                </el-tooltip>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='create_user' label='创建人'></el-table-column>
          <el-table-column prop='create_time' label='创建时间' sortable="custom">
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper" style="text-align: center; color: rgb(0,0,0)">
                <span>{{scope.row.create_time | parseDate}}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button @click="getEncloseur(scope.row.id)" type="success" size="small">附件</el-button>
              <el-button @click="deleteGroup(scope.row.id)" type="danger" size="small">删除</el-button>
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

    <el-dialog :visible.sync="statusForm" @close="cleanForm">
      <el-form :model="rowdata" ref="ruleForm" label-width="100px">
        <el-form-item label="状态" prop="status">
          <el-radio v-model="rowdata.status" v-for="item in Object.keys(STATUS_TEXT)" :key="item" :label="item">
            {{STATUS_TEXT[item]}}
          </el-radio>
        </el-form-item>
        <el-form-item label="通知对象">
          <el-checkbox v-model="send_acc">财务</el-checkbox>
          <el-checkbox v-model="send_cs">客服</el-checkbox>
          <el-checkbox v-model="send_it">部门群组</el-checkbox>
        </el-form-item>
        <el-form-item>
          <el-button @click="statusForm=false">取 消</el-button>
          <el-button type="primary" @click="updateStatus">确 定</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-dialog :visible.sync="addForm">
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px">
        <el-form-item label="标题" prop="name">
          <el-input v-model="ruleForm.name"></el-input>
        </el-form-item>
        <el-form-item label="项目和版本" prop="version">
          <el-input v-model="ruleForm.version" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input v-model="ruleForm.content" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
        </el-form-item>
        <el-form-item>
          <hr class="heng"/>
          <el-upload
            ref="upload"
            :action="uploadurl"
            :on-success="handleSuccess"
            :on-remove="handleRemove"
            :file-list="fileList">
            <el-button slot="trigger" size="small" type="primary" :disabled="count>2?true:false">
              上传文件
            </el-button>
            (可以不用上传)
            <div slot="tip" class="el-upload__tip">
              <p>上传文件不超过10m，<a style="color: red">最多只能上传3个文件</a></p>
            </div>
          </el-upload>
          <hr class="heng"/>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="postForm('ruleForm')">提交</el-button>
          <el-button type="danger" @click="resetForm('ruleForm')">清空</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-dialog :visible.sync="showForm">
      <div v-if='enclosureData.length>0' class="ticketenclosure">
        <ul>
          <li v-for="item in enclosureData" :key="item.id" v-if="item.file" style="list-style:none">
            <i class="fa fa-paperclip"></i>
            <a :href="apiurl + '/upload/' + item.file" :download="item.file">{{item.file.split('/')[1]}}</a>
            <!--<el-button type="text" icon="el-icon-delete"-->
            <!--@click="deleteEnclosure(item.id)"></el-button>-->
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
import {
  getDeployTicket,
  patchDeployTicket,
  postDeployTicket,
  postDeployTicketEnclosur,
  getDeployTicketEnclosur,
  deleteDeployTicketEnclosur
} from '@/api/job'
import { LIMIT, pagesize, pageformat, uploadurl, apiUrl } from '@/config'
import { postUpload, postSendmessage } from 'api/tool'
import { getConversionTime } from '@/utils'

export default {
  components: {},
  data() {
    return {
      route_path: this.$route.path.split('/'),
      tableData: [],
      tabletotal: 0,
      currentPage: 1,
      ticket_status: '',
      pagesize: pagesize,
      pageformat: pageformat,
      rowdata: {
        id: '',
        status: ''
      },
      STATUS_TEXT: { '0': '未上线', '1': '已上线' },
      listQuery: {
        limit: LIMIT,
        offset: '',
        create_user__username: '',
        search: '',
        ordering: ''
      },
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
      statusForm: false,
      addForm: false,
      ruleForm: {
        name: '',
        version: '',
        content: '',
        create_user: localStorage.getItem('username')
      },
      rules: {
        name: [
          { required: true, message: '请输入工单标题', trigger: 'blur' }
        ],
        version: [
          { required: true, message: '请输入工单内容', trigger: 'blur' }
        ],
        content: [
          { required: true, message: '请输入工单内容', trigger: 'blur' }
        ]
      },
      uploadurl: uploadurl,
      apiurl: apiUrl,
      fileList: [],
      count: 0,
      enclosureForm: {
        ticket: '',
        create_user: localStorage.getItem('username'),
        file: ''
      },
      enclosureData: [],
      showForm: false,
      send_acc: false,
      send_cs: false,
      send_it: false
    }
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
    handleSuccess(file, fileList) {
      this.fileList.push(fileList.raw)
      this.count += 1
    },
    handleRemove(file, fileList) {
      this.fileList.remove(file)
      this.count -= 1
    },
    changeStatus(row) {
      this.statusForm = true
      this.rowdata = row
    },
    updateStatus() {
      patchDeployTicket(this.rowdata.id, this.rowdata).then(() => {
        if (this.rowdata.status === '1') {
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
        }
        this.fetchData()
        this.statusForm = false
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
    postForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          postDeployTicket(this.ruleForm).then(response => {
            this.$message({
              type: 'success',
              message: '恭喜你，新建成功'
            })
            for (var fileList of this.fileList) {
              const formData = new FormData()
              formData.append('username', this.enclosureForm.create_user)
              formData.append('file', fileList)
              formData.append('create_time', getConversionTime(fileList.uid))
              formData.append('type', fileList.type)
              formData.append('archive', this.route_path[1])
              postUpload(formData).then(res => {
                this.enclosureForm.file = res.data.filepath
                this.enclosureForm.ticket = response.data.id
                postDeployTicketEnclosur(this.enclosureForm)
              })
            }
            const messageForm = {
              action_user: 'itsupport',
              title: '【上线申请】' + this.ruleForm.name,
              message: `上线内容: ${this.ruleForm.version}`
            }
            postSendmessage(messageForm)
            this.addForm = false
            this.fetchData()
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    deleteEnclosure(id) {
      deleteDeployTicketEnclosur(id)
      this.EnclosureData(id)
    },
    cleanForm() {
      this.send_acc = false
      this.send_cs = false
    }
  }
}
</script>

<style lang='scss'>
  .modifychange {
    margin: 5px;
  }
</style>
