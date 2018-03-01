<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <div class="head-lavel">
        <div class="table-button">
          <el-button type="primary" icon="el-icon-plus" @click="addForm=true">新建</el-button>
          <el-button type="danger" :disabled="btnstatus" @click="show_status=true">更改状态</el-button>
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
        <el-table :data="tableData" border style="width: 100%" @selection-change="handleSelectionChange"
                  @sort-change="handleSortChange">
          <el-table-column type="selection"></el-table-column>
          <el-table-column prop='id' label='ID'></el-table-column>
          <el-table-column prop='name' label='标题'></el-table-column>
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

    <el-dialog :visible.sync="show_status">
      <el-radio-group v-model="rowdata.status">
        <el-radio v-for="item in Object.keys(STATUS_TEXT)" :key="item" :label="item">{{STATUS_TEXT[item]}}
        </el-radio>
      </el-radio-group>
      <span slot="footer" class="dialog-footer">
        <el-button @click="show_status=false">取 消</el-button>
        <el-button type="primary" @click="changeForm">确 定</el-button>
      </span>
    </el-dialog>

    <el-dialog :visible.sync="addForm">
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
        <el-form-item label="标题" prop="name">
          <el-input v-model="ruleForm.name"></el-input>
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <mavon-editor style="z-index: 1" v-model="ruleForm.content" code_style="monokai"
                        :toolbars="toolbars"></mavon-editor>
          <a class="tips"> Tip：截图可以直接 Ctrl + v 粘贴到工单内容里面</a>
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
            <el-button type="text" icon="el-icon-delete"
                       @click="deleteEnclosure(item.id)"></el-button>
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
        status: '1'
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
      btnstatus: true,
      show_status: false,
      addForm: false,
      ruleForm: {
        name: '',
        content: '',
        create_user: localStorage.getItem('username')
      },
      rules: {
        name: [
          { required: true, message: '请输入工单标题', trigger: 'blur' }
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
      showForm: false
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
    changeStatus() {
      this.fetchData()
    },
    handleSelectionChange(val) {
      this.selectId = []
      for (var i = 0, len = val.length; i < len; i++) {
        this.selectId.push(val[i].id)
      }
      if (this.selectId.length > 0) {
        this.btnstatus = false
      } else {
        this.btnstatus = true
      }
    },
    changeForm() {
      for (var i = 0, len = this.selectId.length; i < len; i++) {
        patchDeployTicket(this.selectId[i], this.rowdata).then(response => {
          delete this.selectId[i]
        })
      }
      this.fetchData()
      this.show_status = false
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
              message: `上线内容: ${this.ruleForm.content}`
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
    }
  }
}
</script>

<style lang='scss'>

</style>
