<template xmlns="http://www.w3.org/1999/html">
  <div class="components-container" style='height:100vh'>
    <el-card>
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
        <el-form-item label="标题" prop="title">
          <el-input v-model="ruleForm.title" placeholder="请输入标题"></el-input>
        </el-form-item>
        <el-form-item label="指派人" prop="action_user">
          <el-select v-model="ruleForm.action_user" filterable placeholder="请选择指派人">
            <el-option v-for="item in users" :key="item.id" :value="item.username"></el-option>
          </el-select>
          <a class="tips"> Tip：当前工单处理人，默认是指派给ITSupport群组</a>
        </el-form-item>
        <el-form-item label="跟踪者" prop="follower">
          <el-select v-model="ruleForm.follower" filterable multiple placeholder="请选择跟踪者">
            <el-option v-for="item in users" :key="item.id" :value="item.username"></el-option>
          </el-select>
          <a class="tips"> Tip：工单状态发生变更时，邮件抄送给跟踪者</a>
        </el-form-item>
        <el-form-item label="平台" prop="platform">
          <el-select v-model="ruleForm.platform" filterable placeholder="请选择平台" @change="showaddmerchant=true">
            <el-option v-for="item in platforms" :key="item.id" :value="item.name"></el-option>
          </el-select>
          <el-button v-if="showaddmerchant" size="small" type="success" plain @click="addMerchantForm=true">添加商户
          </el-button>
        </el-form-item>
        <el-form-item v-if="showmercant" label="商户列表">
          <el-tag
            style="margin-right: 5px"
            :key="tag.id"
            v-for="tag in dynamicMerchants"
            closable
            @close="handleClose(tag)">
            <el-button type="text" size="mini" @click="selectMerchant(tag)">{{tag.name}}</el-button>
          </el-tag>
          <a class="tips"> Tip：点击商户，增加支付通道明细</a>
        </el-form-item>
        <el-form-item label="通道列表" v-if="showchannels">
          <el-card>
            <el-button size="small" type="success" plain @click="addChannelForm=true">添加通道
            </el-button>
            <el-table ref="channelsTable" :data="dynamicChannels" highlight-current-row style="width: 100%">
              <el-table-column type="index" width="50"></el-table-column>
              <el-table-column type="expand">
                <template slot-scope="props">
                  <el-form label-position="left" inline class="table-expand">
                    <el-form-item label="紧急度">
                      <el-rate
                        v-model="props.row.level"
                        :colors="['#99A9BF', '#F7BA2A', '#ff1425']"
                        show-text
                        :texts="['E', 'D', 'C', 'B', 'A']"
                        :disabled="!editChannelForm">
                      </el-rate>
                    </el-form-item>
                    <el-form-item label="MD5KEY">
                      <el-input size="small" v-model="props.row.m_md5key" :disabled="!editChannelForm"></el-input>
                    </el-form-item>
                    <el-form-item label="商户公钥">
                      <el-input size="small" v-model="props.row.m_public_key" :disabled="!editChannelForm"></el-input>
                    </el-form-item>
                    <el-form-item label="商户私钥">
                      <el-input size="small" v-model="props.row.m_private_key" :disabled="!editChannelForm"></el-input>
                    </el-form-item>
                    <el-form-item label="平台公钥">
                      <el-input size="small" v-model="props.row.p_public_key" :disabled="!editChannelForm"></el-input>
                    </el-form-item>
                    <el-form-item label="转发域名">
                      <el-input size="small" v-model="props.row.m_forwardurl" :disabled="!editChannelForm"></el-input>
                    </el-form-item>
                    <el-form-item label="提交域名">
                      <el-input size="small" v-model="props.row.m_submiturl" :disabled="!editChannelForm"></el-input>
                    </el-form-item>
                    <el-form-item label="回调域名">
                      <el-input size="small" v-model="props.row.m_backurl" :disabled="!editChannelForm"></el-input>
                    </el-form-item>
                  </el-form>
                </template>
              </el-table-column>
              <el-table-column prop='name' label='名称' sortable='custom'></el-table-column>
              <el-table-column prop='level' label='紧急度'></el-table-column>
              <el-table-column prop='merchant' label='依附商户'>reww</el-table-column>
              <el-table-column label="操作">
                <template slot-scope="scope">
                  <el-button v-if="!editChannelForm" @click="editChannelForm=true" type="success" size="small">修改
                  </el-button>
                  <el-button v-if="editChannelForm" @click="editChannelForm=false" type="primary" size="small">保存
                  </el-button>
                  <el-button @click="deleteChannel(scope.row)" type="danger" size="small">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
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
            <a class="tips"> Tip：上传文件不超过10m，<a style="color: red">最多只能上传3个文件</a></a>
          </el-upload>
          <hr class="heng"/>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="postForm('ruleForm')">提交</el-button>
          <el-button type="danger" @click="resetForm('ruleForm')">清空</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-dialog :visible.sync="addMerchantForm">
      <add-merchant :rowdata="ruleForm.platform" @formdata="addMerchantTag"></add-merchant>
    </el-dialog>

    <el-dialog :visible.sync="addChannelForm">
      <add-channel :rowdata="merchant" @formdata="addChannelTable"></add-channel>
    </el-dialog>
  </div>
</template>
<script>
import {
  postThreepayTicket,
  postThreePayEnclosure,
  getPlatform,
  deleteMerchant,
  deletePayChannel
} from 'api/threeticket'
import { postUpload, postSendmail } from 'api/tool'
import { getUser } from 'api/user'
import { uploadurl } from '@/config'
import { mapGetters } from 'vuex'
import { getCreatetime, getConversionTime } from '@/utils'
import addMerchant from './addMerchant.vue'
import addChannel from './addPaychannel.vue'

export default {
  components: {
    addMerchant,
    addChannel
  },

  data() {
    return {
      route_path: this.$route.path.split('/'),
      ruleForm: {
        title: '',
        create_user: localStorage.getItem('username'),
        action_user: 'itsupport',
        follower: '',
        create_group: '',
        ticketid: '',
        platform: ''
      },
      rules: {
        title: [
          { required: true, message: '请输入工单标题', trigger: 'blur' }
        ]
      },
      users: [],
      fileList: [],
      count: 0,
      enclosureFile: [],
      enclosureForm: {
        ticket: '',
        create_user: localStorage.getItem('username'),
        file: ''
      },
      formDataList: [],
      to_list: '',
      cc_list: '',
      uploadurl: uploadurl,
      platforms: [],
      showaddmerchant: false,
      showchannels: false,
      showchannel: false,
      addMerchantForm: false,
      addChannelForm: false,
      editChannelForm: false,
      showmercant: false,
      dynamicMerchants: [],
      dynamicChannels: [],
      merchant: ''
    }
  },

  computed: {
    ...mapGetters([
      'username'
    ])
  },
  created() {
    this.getTicketUsers()
    this.getPlatforms()
  },
  methods: {
    postForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.ruleForm.ticketid = getConversionTime()
          postThreepayTicket(this.ruleForm).then(response => {
            if (response.statusText === '"Created"') {
              this.$message({
                type: 'success',
                message: '恭喜你，新建成功'
              })
            }
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
                postThreePayEnclosure(this.enclosureForm)
              })
            }
            const create_time = getCreatetime()
            const mailForm = {
              to: this.ruleForm.action_user,
              cc: this.ruleForm.follower.join(),
              sub: '【新工单】' + this.ruleForm.title,
              content: `
                    <html xmlns="http://www.w3.org/1999/xhtml">
                    <head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><title>工单通知邮件</title></head>
                    <body><div id="container">
                    <p>工单提交人： ${this.ruleForm.create_user}</p>
                    <p>工单提交时间：${create_time} </p>
                    <p>点击工单地址: <a href='${window.location.host}/#/worktickets/editworkticket/${this.ruleForm.ticketid}'>
                    ${window.location.host}/#/worktickets/editworkticket/${this.ruleForm.ticketid}</a></p>
                    <p>工单详细内容：</p>
                    <p>${this.ruleForm.content}</p>
                    </div></body></html>`
            }
            postSendmail(mailForm)
            this.$router.push('/worktickets/workticket')
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    handleSuccess(file, fileList) {
      this.fileList.push(fileList.raw)
      this.count += 1
    },
    handleRemove(file, fileList) {
      this.fileList.remove(file)
      this.count -= 1
    },
    getTicketUsers() {
      getUser().then(response => {
        this.users = response.data
      })
    },
    getPlatforms() {
      getPlatform().then(response => {
        this.platforms = response.data
      })
    },
    addMerchantTag(data) {
      this.dynamicMerchants.push(data)
      this.addMerchantForm = false
      this.showmercant = true
    },
    handleClose(tag) {
      this.$confirm('你确定要删除这个, 是否继续?', '特朗普提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteMerchant(tag.id)
        this.dynamicMerchants.splice(this.dynamicMerchants.indexOf(tag), 1)
        if (this.dynamicMerchants.length < 1) {
          this.showmercant = false
          this.showchannels = false
        }
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
    selectMerchant(merchant) {
      this.showchannels = true
      this.merchant = merchant
    },
    addChannelTable(data) {
      this.addChannelForm = false
      this.dynamicChannels.push(data)
    },
    deleteChannel(row) {
      this.$confirm('你确定要删除这个, 是否继续?', '特朗普提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deletePayChannel(row.id)
        this.dynamicChannels.remove(row)
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
    }
  }
}
</script>

<style lang='scss'>
  .heng {
    margin: 20px 0;
    height: 1px;
    border: 0px;
    background-color: rgba(174, 127, 255, 0.38);
    color: #29e11c;
  }

  .addticket {
    margin: 50px;
    width: 80%;
  }

  .tips {
    color: rgba(128, 128, 128, 0.82);
  }

  .table-expand {
    font-size: 0;
    label {
      width: 90px;
      color: #99a9bf;
    }
    .el-form-item {
      margin-right: 0;
      margin-bottom: 0;
      width: 50%;
    }
  }
</style>
