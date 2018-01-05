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
          </div>
          <el-tree
            :data="platformData"
            :props="props"
            :load="fetchNodeData"
            accordion
            lazy
            @node-click="handleNodeClick">
          </el-tree>
        </el-card>

        <el-card v-if="showenclosure" class="card-box">
          <el-tabs v-model="activeName" type="card">
            <el-tab-pane label="上传附件" name="upload">
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
                    <p>上传文件不超过10m，<a style="color: red">最多只能上传10个文件</a></p>
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
              <el-input v-model="platformForm.ipaddr" :disabled="formStatus === 'view'" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
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

      <el-col :span="18" v-if="selecttype&&!clickbtn">
        <el-card>
          <div slot="header">
            <el-button size="small" type="primary" plain @click="addChannelForm=true">添加通道
            </el-button>
            <a style="margin-left: 20px;color: #fa11ff">商户号：{{listQuery.merchant__name}}</a>
          </div>

          <el-table ref="channelsTable" :data="dynamicChannels" border style="width: 100%"
                    @row-click="clickPayChannel">
            <el-table-column type="index" width="50"></el-table-column>
            <el-table-column label='查看明细' type="expand" width="100">
              <template slot-scope="props">
                <el-form label-position="left" inline class="table-expand">
                  <el-form-item label="key信息" prop="keyinfo">
                    <el-input v-model="props.row.keyinfo" type="textarea" :disabled="!editChannelForm" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
                  </el-form-item>
                  <el-form-item label="转发域名">
                    <el-input size="small" v-model="props.row.m_forwardurl" :disabled="!editChannelForm"></el-input>
                  </el-form-item>
                  <el-form-item label="提交域名">
                    <el-input size="small" v-model="props.row.m_submiturl" :disabled="!editChannelForm"></el-input>
                  </el-form-item>
                </el-form>
              </template>
            </el-table-column>
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
            <el-table-column prop='complete' label='完成百分比'>
              <template slot-scope="scope">
                <el-progress type="circle" :percentage="scope.row.complete" :width="40"></el-progress>
                <el-tooltip class="item" effect="dark" content="更新进度" placement="top">
                    <el-button @click="EditComplete(scope.row)" type="primary" plain size="mini" icon="el-icon-edit" class="modifychange"></el-button>
                </el-tooltip>
              </template>
            </el-table-column>
            <el-table-column prop='create_time' label='创建时间'>
              <template slot-scope="scope">
                <div slot="reference" class="name-wrapper" style="text-align: center; color: rgb(0,0,0)">
                  <span>{{scope.row.create_time | parseDate}}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column label="操作">
              <template slot-scope="scope">
                <el-button @click="editPayChannel(scope.row)" type="success" size="mini">修改</el-button>
                <el-button v-if="paychannel_btn_delete_channel||role==='super'" @click="deletePayChannels(scope.row)" type="danger" size="mini">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <el-dialog :visible.sync="addChannelForm">
      <add-paychannel @formdata="fetchPayChannelData"></add-paychannel>
    </el-dialog>

    <el-dialog :visible.sync="editChannelForm">
      <edit-paychannel :rowdata="paychannels" @formdata="fetchPayChannelData"></edit-paychannel>
    </el-dialog>

    <el-dialog :visible.sync="completeForm" width="30%">
      <el-form :model="CommentForm" label-width="100px">
        <el-form-item label="代付测试金额" props="content">
          <el-input v-model="CommentForm.content"></el-input>
        </el-form-item>
        <el-form-item label="完成百分比">
          <el-slider
            v-model="complete"
            :step="10">
          </el-slider>
        </el-form-item>
        <el-form-item>
          <el-button @click="changePayChannel" type="success" size="mini">确定</el-button>
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
import { getPayChannel, deletePayChannel, patchPayChannel } from 'api/threeticket'
import { mapGetters } from 'vuex'
import addPaychannel from './components/addPaychannel.vue'
import editPaychannel from './components/editPaychannel.vue'
import { LIMIT, apiUrl, uploadurl } from '@/config'
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
      limit: LIMIT,
      platformData: [],
      merchantData: [],
      clickbtn: false,
      showbtn: false,
      selecttype: false,
      formEdit: false,
      formAdd: true,
      formStatus: '',
      completeForm: false,
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
        platform__name: '',
        merchant__name: ''
      },
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
      complete: 0,
      channel_create_user: '',
      CommentForm: {
        ticket: '',
        merchant: '',
        content: '一个亿',
        create_user: localStorage.getItem('username')
      },
      comments: []
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
    fetchPayChannelData() {
      this.addChannelForm = false
      this.editChannelForm = false
      getPayChannel(this.listQuery).then(response => {
        this.dynamicChannels = response.data
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
        this.fetchPayChannelData()
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
    EditComplete(row) {
      this.completeForm = true
      this.complete = row.complete
      this.CommentForm.ticket = row.id
      this.channel_create_user = row.create_user
    },
    changePayChannel() {
      this.completeForm = false
      postThreePayComment(this.CommentForm)
      const parmas = {
        complete: this.complete
      }
      patchPayChannel(this.CommentForm.ticket, parmas).then(response => {
        this.$message({
          type: 'success',
          message: '更新成功!'
        })
        const create_time = getCreatetime()
        const messageForm = {
          action_user: `${this.channel_create_user}`,
          title: '【支付通道测试】',
          message: `商户号: ${this.CommentForm.merchant}\n代付测试金额: ${this.CommentForm.content}\n测试时间: ${create_time}`
        }
        postSendmessage(messageForm)
        this.fetchPayChannelData()
        this.fetchPayChannelData()
        this.clickPayChannel({ id: this.CommentForm.ticket })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '更新失败'
        })
      })
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
        this.CommentForm.merchant = this.enclosureForm.ticket = this.listQuery.merchant__name = data.name
        this.EnclosureData()
        this.showenclosure = true
        this.activeName = 'upload'
      } else {
        this.showenclosure = false
        this.platformForm = data
        this.listQuery.platform__name = data.name
      }
      this.fetchPayChannelData()
    },
    editPayChannel(row) {
      this.editChannelForm = true
      this.paychannels = row
    },
    clickPayChannel(row) {
      this.activeName = 'testpay'
      const parmas = {
        ticket__id: row.id
      }
      getThreePayComment(parmas).then(response => {
        this.comments = response.data
      })
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
      const isLt = file.size / 1024 / 1024 < 10
      if (!isLt) {
        this.$message.error('上传文件大小不能超过 10MB!')
        return false
      } else {
        const formData = new FormData()
        formData.append('username', this.enclosureForm.create_user)
        formData.append('file', file)
        formData.append('create_time', getConversionTime(file.lastModified))
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
      }
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
</style>
