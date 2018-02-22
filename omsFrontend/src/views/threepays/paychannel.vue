<template>
  <div class="components-container" style='height:100vh'>
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card>
          <div slot="header">
            <span class="card-title">平台商户列表</span>
            <el-button-group>
              <el-button type="success" plain size="mini" @click="handlerAdd">
                添加
              </el-button>
              <el-button type="primary" plain size="mini" v-if="showbtn" @click="handlerEdit">
                编辑
              </el-button>
            </el-button-group>
            <el-input
              style="margin-top: 10px"
              placeholder="搜索平台或商户号..."
              v-model="filterplatform">
            </el-input>
          </div>
          <div class="tree">
            <el-tree
              ref="tree"
              :data="platformData"
              :props="props"
              :load="fetchNodeData"
              :filter-node-method="filterNode"
              accordion
              lazy
              @node-click="handleNodeClick">
            </el-tree>
          </div>
        </el-card>

        <el-card v-if="showenclosure" class="card-box">
          <el-tabs v-model="activeName" type="card">
            <el-tab-pane label="上传附件" name="upload">
              <div>
                <el-upload
                  ref="upload"
                  :action="uploadurl"
                  :show-file-list="false"
                  :disabled="count>10?true:false"
                  :before-upload="beforeAvatarUpload">
                  <el-button slot="trigger" size="mini" type="danger" plain icon="upload2"
                             :disabled="count>10?true:false">
                    上传
                  </el-button>
                  <div slot="tip" class="el-upload__tip">
                    <p><a style="color: red">最多只能上传10个文件</a></p>
                  </div>
                </el-upload>

                <div v-if='enclosureData.length>0' class="ticketenclosure">
                  <ul>
                    <li v-for="item in enclosureData" :key="item.id" v-if="item.file" style="list-style:none">
                      <i class="fa fa-paperclip"></i>
                      <a :href="apiurl + '/upload/' + item.file" :download="item.file">{{item.file.split('/')[1]}}</a>
                      <el-tooltip class="item" effect="dark" content="删除附件" placement="right">
                        <el-button type="text" icon="el-icon-delete" @click="deleteEnclosure(item.id)"></el-button>
                      </el-tooltip>
                    </li>
                  </ul>
                </div>
              </div>
            </el-tab-pane>
            <el-tab-pane label="通道测试" name="testpay">
              <el-table :data="comments" border style="width: 100%">
                <el-table-column prop="create_user" label="测试人" width="80"></el-table-column>
                <el-table-column prop="content" label="代付测试金额" width="120"></el-table-column>
                <el-table-column prop="create_time" label="测试时间">
                  <template slot-scope="scope">
                    <div slot="reference" class="name-wrapper" style="text-align: center; color: rgb(0,0,0)">
                      <span>{{scope.row.create_time | parseDate}}</span>
                    </div>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </el-col>

      <el-col :span="6" v-if="clickbtn">
        <el-card>
          <div slot="header">
            <el-switch
              v-model="selecttype"
              active-text="商户"
              inactive-text="平台">
            </el-switch>
            <el-button style="float: right; padding: 3px 0" type="text" @click="handlerClosed">关闭</el-button>
          </div>

          <el-form v-if="!selecttype" :model="platformForm" ref="ruleForm" label-width="100px">
            <el-form-item label="名称" prop="name">
              <el-input v-model="platformForm.name" :disabled="formStatus === 'view'"></el-input>
            </el-form-item>
            <el-form-item label="ip地址" prop="ipaddr">
              <el-input v-model="platformForm.ipaddr" :disabled="formStatus === 'view'" type="textarea"
                        :autosize="{ minRows: 5, maxRows: 10}"></el-input>
            </el-form-item>
            <el-form-item label="描述" prop="desc">
              <el-input v-model="platformForm.desc" :disabled="formStatus === 'view'" type="textarea"
                        :autosize="{ minRows: 5, maxRows: 10}"></el-input>
            </el-form-item>
            <el-form-item v-if="formStatus == 'create'">
              <el-button type="primary" @click="postPlatformForm('ruleForm')">创建</el-button>
              <el-button @click="resetForm('ruleForm')">重置</el-button>
            </el-form-item>
            <el-form-item v-if="formStatus == 'update'">
              <el-button type="success" @click="putPlatformForm(platformForm)">更新</el-button>
              <el-button type="danger" @click="deletePlatformForm(platformForm.id)">删除</el-button>
            </el-form-item>
          </el-form>

          <el-form v-if="selecttype" :model="merchantForm" ref="ruleForm" label-width="100px">
            <el-form-item label="平台" prop="platform">
              <el-select v-model="merchantForm.platform" placeholder="请选择平台">
                <el-option v-for="item in platformData" :key="item.id" :value="item.name"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="商户号" prop="name">
              <el-input v-model="merchantForm.name" :disabled="formStatus === 'view'"></el-input>
            </el-form-item>
            <el-form-item label="公司名" prop="m_id">
              <el-input v-model="merchantForm.m_id" :disabled="formStatus === 'view'"></el-input>
            </el-form-item>
            <el-form-item label="绑定域名" prop="domain">
              <el-input v-model="merchantForm.domain" :disabled="formStatus === 'view'"></el-input>
            </el-form-item>
            <el-form-item label="业务经理" prop="three">
              <el-input v-model="merchantForm.three" :disabled="formStatus === 'view'"></el-input>
            </el-form-item>
            <el-form-item v-if="formStatus == 'create'">
              <el-button type="primary" @click="postMerchantForm('ruleForm')">创建</el-button>
              <el-button @click="resetForm('ruleForm')">重置</el-button>
            </el-form-item>
            <el-form-item v-if="formStatus == 'update'">
              <el-button type="success" @click="putMerchantForm(merchantForm)">更新</el-button>
              <el-button type="danger" @click="deleteMerchantForm(merchantForm.id)">删除</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <el-col :span="18" v-if="!clickbtn">
        <el-card>
          <div slot="header">
            <el-button size="small" type="primary" plain @click="addChannelForm=true">添加通道
            </el-button>
            <div v-if="showenclosure" class="merchant_info">
              商户号：{{merchantForm.name}} <a class="shu"></a>
              商户公司：{{merchantForm.m_id}} <a class="shu"></a>
              业务经理：{{merchantForm.three}}
            </div>
            <el-button size="small" type="success" plain style="float: right" @click="showAllPaychannel">显示全部
            </el-button>
          </div>

          <el-table ref="channelsTable" :data="dynamicChannels" border style="width: 100%"
                    @row-click="clickPayChannel" @sort-change="handleSortChange">
            <el-table-column type="index" width="50"></el-table-column>
            <el-table-column label='查看明细' type="expand" width="80">
              <template slot-scope="props">
                <el-form label-position="left" inline class="table-expand">
                  <el-form-item label="key信息" prop="keyinfo">
                    <el-input v-model="props.row.keyinfo" type="textarea" disabled
                              :autosize="{ minRows: 5, maxRows: 10}"></el-input>
                  </el-form-item>
                  <el-form-item label="转发域名">
                    <el-input size="small" v-model="props.row.m_forwardurl" disabled></el-input>
                  </el-form-item>
                  <el-form-item label="提交域名">
                    <el-input size="small" v-model="props.row.m_submiturl" disabled></el-input>
                  </el-form-item>
                </el-form>
              </template>
            </el-table-column>
            <el-table-column prop='platform' label='平台'></el-table-column>
            <el-table-column prop='type' label='通道类型'></el-table-column>
            <el-table-column prop='rate' label='费率'></el-table-column>
            <el-table-column prop='create_time' label='创建时间' sortable>
              <template slot-scope="scope">
                <div slot="reference" class="name-wrapper" style="text-align: center; color: rgb(0,0,0)">
                  <span>{{scope.row.create_time | parseDate}}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column label="操作">
              <template slot-scope="scope">
                <el-button @click="editPayChannel(scope.row)" type="success" size="mini">修改</el-button>
                <el-button v-if="scope.row.type == '代付提款'" type="primary" size="mini"
                           @click="editDaifu(scope.row)">代付测试
                </el-button>
                <el-button v-if="paychannel_btn_delete_channel||role==='super'"
                           @click="deletePayChannels(scope.row)"
                           type="danger" size="mini">删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
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
      </el-col>
    </el-row>

    <el-dialog :visible.sync="addChannelForm">
      <add-paychannel @formdata="fetchPayChannelData"></add-paychannel>
    </el-dialog>

    <el-dialog :visible.sync="editChannelForm">
      <edit-paychannel :rowdata="paychannels" @formdata="fetchPayChannelData"></edit-paychannel>
    </el-dialog>

    <el-dialog :visible.sync="daifuForm" width="30%">
      <el-form :model="CommentForm" label-width="100px">
        <el-form-item label="代付测试金额" props="content">
          <el-input v-model="CommentForm.content"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button @click="changeDaifu" type="success" size="mini">确定</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import { getPlatform, postPlatform, putPlatform, deletePlatform } from '@/api/threeticket'
import { getMerchant, postMerchant, putMerchant, deleteMerchant } from 'api/threeticket'
import { getThreePayEnclosure, postThreePayEnclosure, deleteThreePayEnclosure } from 'api/threeticket'
import { postThreePayComment, getThreePayComment } from 'api/threeticket'
import { getPayChannel, deletePayChannel } from 'api/threeticket'
import { mapGetters } from 'vuex'
import addPaychannel from './components/addPaychannel.vue'
import editPaychannel from './components/editPaychannel.vue'
import { LIMIT, pagesize, pageformat, apiUrl, uploadurl } from '@/config'
import { getCreatetime, getConversionTime } from '@/utils'
import { postUpload, postSendmessage } from 'api/tool'

export default {
  components: {
    addPaychannel, editPaychannel
  },
  data() {
    return {
      route_path: this.$route.path.split('/'),
      apiurl: apiUrl,
      platformData: [],
      merchantData: [],
      clickbtn: false,
      showbtn: false,
      selecttype: false,
      formEdit: false,
      formAdd: true,
      formStatus: '',
      completeForm: false,
      daifuForm: false,
      paychannel_btn_delete_channel: false,
      platformForm: {
        name: '',
        ipaddr: '',
        desc: ''
      },
      platformRules: {
        name: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        ipaddr: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ]
      },
      merchantForm: {
        platform: '',
        name: '',
        m_id: '',
        domain: '',
        three: ''
      },
      merchantRules: {
        name: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        m_id: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        three: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ]
      },
      props: {
        label: 'name',
        children: ''
      },
      addChannelForm: false,
      editChannelForm: false,
      dynamicChannels: [],
      listQuery: {
        limit: LIMIT,
        offset: '',
        platform__name: '',
        merchant__name: '',
        ordering: ''
      },
      currentPage: 1,
      pagesize: pagesize,
      pageformat: pageformat,
      tabletotal: 0,
      paychannels: [],
      enclosureData: [],
      count: 0,
      enclosureForm: {
        ticket: '',
        create_user: localStorage.getItem('username'),
        file: ''
      },
      uploadurl: uploadurl,
      showenclosure: false,
      activeName: 'upload',
      channel_create_user: '',
      CommentForm: {
        ticket: '',
        merchant: '',
        content: 0,
        create_user: localStorage.getItem('username')
      },
      comments: [],
      filterplatform: ''
    }
  },
  computed: {
    ...mapGetters([
      'elements',
      'role'
    ])
  },
  created() {
    this.paychannel_btn_delete_channel = this.elements['支付通道列表-删除通道']
    this.fetchPlatformData()
    this.fetchMerchantData()
    this.fetchPayChannelData()
  },
  methods: {
    fetchPlatformData() {
      getPlatform().then(response => {
        this.platformData = response.data
      })
    },
    fetchMerchantData() {
      getMerchant().then(response => {
        this.merchantData = response.data
      })
    },
    clickMerchantData(parmas) {
      getMerchant(parmas).then(response => {
        this.merchantForm = response.data[0]
      })
    },
    fetchPayChannelData() {
      this.addChannelForm = false
      this.editChannelForm = false
      getPayChannel(this.listQuery).then(response => {
        this.dynamicChannels = response.data.results
        this.tabletotal = response.data.count
      })
    },
    postPlatformForm() {
      postPlatform(this.platformForm).then(response => {
        this.$message({
          message: '恭喜你，添加成功',
          type: 'success'
        })
        this.fetchPlatformData()
      }).catch(error => {
        this.$message.error('添加失败')
        console.log(error)
      })
    },
    putPlatformForm(formdata) {
      putPlatform(formdata.id, formdata).then(response => {
        this.$message({
          message: '恭喜你，更新成功',
          type: 'success'
        })
        this.fetchPlatformData()
      }).catch(error => {
        this.$message.error('更新失败')
        console.log(error)
      })
    },
    deletePlatformForm(id) {
      this.$confirm('你确定要删除这个, 是否继续?', '美丽的妲己提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deletePlatform(id)
        this.fetchPlatformData()
        this.$message({
          type: 'success',
          message: '删除成功!'
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    postMerchantForm() {
      postMerchant(this.merchantForm).then(response => {
        this.$message({
          message: '恭喜你，添加成功',
          type: 'success'
        })
        this.fetchPlatformData()
      }).catch(error => {
        this.$message.error('添加失败')
        console.log(error)
      })
    },
    putMerchantForm(formdata) {
      putMerchant(formdata.id, formdata).then(response => {
        this.$message({
          message: '恭喜你，更新成功',
          type: 'success'
        })
        this.fetchPlatformData()
      }).catch(error => {
        this.$message.error('更新失败')
        console.log(error)
      })
    },
    deleteMerchantForm(id) {
      this.$confirm('你确定要删除这个, 是否继续?', '美丽的妲己提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteMerchant(id)
        this.fetchPlatformData()
        this.$message({
          type: 'success',
          message: '删除成功!'
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    deletePayChannels(row) {
      this.$confirm('你确定要删除这个, 是否继续?', '美丽的妲己提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deletePayChannel(row.id)
        this.dynamicChannels.remove(row)
        setTimeout(this.fetchPayChannelData(), 1000)
        this.$message({
          type: 'success',
          message: '删除成功!'
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    handlerAdd() {
      this.clickbtn = true
      this.formEdit = true
      this.formStatus = 'create'
      this.resetForm()
    },
    handlerEdit() {
      this.clickbtn = true
      this.formEdit = true
      this.formStatus = 'update'
    },
    handlerClosed() {
      this.clickbtn = false
      this.formEdit = true
      this.showbtn = false
    },
    editDaifu(row) {
      this.daifuForm = true
      this.CommentForm.ticket = row.id
      this.CommentForm.merchant = row.merchant
      this.channel_create_user = row.create_user
    },
    changeDaifu() {
      postThreePayComment(this.CommentForm)
      const create_time = getCreatetime()
      const messageForm = {
        action_user: `${this.channel_create_user}`,
        title: '【代付通道测试】',
        message: `商户号: ${this.CommentForm.merchant}\n代付测试金额: ${this.CommentForm.content}\n测试时间: ${create_time}`
      }
      postSendmessage(messageForm)
      this.daifuForm = false
      this.showenclosure = true
      setTimeout(this.clickPayChannel({ id: this.CommentForm.ticket }), 500)
    },
    resetForm() {
      this.platformForm = {
        name: '',
        desc: ''
      }
      this.merchantForm = {
        platform: '',
        name: '',
        m_id: '',
        three: ''
      }
    },
    fetchNodeData(node, resolve) {
      if (node.level === 0) {
        return resolve([{ name: 'region' }])
      }
      if (node.level > 1) return resolve([])

      const parmas = {
        platform__name: node.data.name
      }
      getMerchant(parmas).then(response => {
        const data = response.data
        setTimeout(() => {
          resolve(data)
        }, 500)
      })
    },
    handleNodeClick(data, res) {
      this.selecttype = res.isLeaf
      this.showbtn = true
      this.formStatus = 'view'
      this.formEdit = true
      if (this.selecttype) {
        this.merchantForm = data
        this.CommentForm.merchant = this.listQuery.merchant__name = data.name
      } else {
        this.activeName = 'upload'
        this.showenclosure = true
        this.platformForm = data
        this.enclosureForm.ticket = this.listQuery.platform__name = data.name
        this.listQuery.merchant__name = ''
        this.EnclosureData()
      }
      this.fetchPayChannelData()
    },
    editPayChannel(row) {
      this.editChannelForm = true
      this.paychannels = row
    },
    clickPayChannel(row) {
      this.showenclosure = true
      this.activeName = 'testpay'
      const parmas = {
        ticket__id: row.id
      }
      getThreePayComment(parmas).then(response => {
        this.comments = response.data
      })
      this.clickMerchantData({ name: row.merchant })
    },
    EnclosureData() {
      const parms = {
        ticket__name: this.enclosureForm.ticket
      }
      getThreePayEnclosure(parms).then(response => {
        this.enclosureData = response.data
        this.count = response.data.length
      })
    },
    deleteEnclosure(id) {
      deleteThreePayEnclosure(id)
      setTimeout(this.EnclosureData, 1000)
    },
    beforeAvatarUpload(file) {
      const formData = new FormData()
      formData.append('username', this.enclosureForm.create_user)
      formData.append('file', file)
      formData.append('create_time', getConversionTime())
      formData.append('type', file.type)
      formData.append('archive', this.route_path[1])
      postUpload(formData).then(response => {
        this.enclosureForm.file = response.data.filepath
        postThreePayEnclosure(this.enclosureForm)
        setTimeout(this.EnclosureData, 1000)
        if (response.statusText === 'Created') {
          this.$message({
            type: 'success',
            message: '恭喜你，上传成功'
          })
        }
      }).catch(error => {
        this.$message.error('上传失败')
        this.$refs.upload.clearFiles()
        console.log(error)
      })
      return true
    },
    handleSizeChange(val) {
      this.listQuery.limit = val
      this.fetchPayChannelData()
    },
    handleCurrentChange(val) {
      this.listQuery.offset = (val - 1) * LIMIT
      this.fetchPayChannelData()
    },
    showAllPaychannel() {
      this.listQuery = {
        limit: LIMIT,
        offset: '',
        platform__name: '',
        merchant__name: ''
      }
      this.fetchPayChannelData()
    },
    handleSortChange(val) {
      if (val.order === 'ascending') {
        this.listQuery.ordering = val.prop
      } else if (val.order === 'descending') {
        this.listQuery.ordering = '-' + val.prop
      } else {
        this.listQuery.ordering = ''
      }
      this.fetchPayChannelData()
    },
    filterNode(value, data) {
      if (!value) return true
      return data.name.indexOf(value) !== -1
    }
  },
  watch: {
    filterplatform(val) {
      this.$refs.tree.filter(val)
    }
  }
}
</script>

<style lang='scss'>
  .card-title {
    padding-right: 30px;
  }

  .table-expand {
    font-size: 0;
    .el-form-item {
      margin-right: 0;
      margin-bottom: 0;
      width: 100%;
      .el-form-item__label {
        width: 90px;
        color: #99a9bf;
      }
      .el-form-item__content {
        width: 80%;
      }
    }
  }

  .card-box {
    margin-top: 20px;
  }

  .modifychange {
    position: absolute;
    margin: 5px 20px;
  }

  .table-pagination {
    padding: 10px 0;
    float: right;
  }

  .merchant_info {
    display: inline-block;
    margin-left: 20px;
    font-size: 14px;
  }

  .tree {
    height: 350px;
    overflow-y: scroll;
    overflow-x: hidden;
    /* 设置滚动条的样式 */
    &::-webkit-scrollbar {
      width: 10px;
    }
    /* 滚动槽 */
    &::-webkit-scrollbar-track {
      -webkit-box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.2);
      border-radius: 10px;
    }
    /* 滚动条滑块 */
    &::-webkit-scrollbar-thumb {
      border-radius: 10px;
      background: rgba(79, 255, 32, 0.24);
      -webkit-box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.57);
    }
    &::-webkit-scrollbar-thumb:window-inactive {
      background: rgba(79, 255, 32, 0.53);
    }
  }
</style>
