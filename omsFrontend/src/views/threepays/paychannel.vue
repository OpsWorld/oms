<template>
  <div class="components-container" style='height:100vh'>
    <el-row :gutter="20">
      <el-col :span="4">
        <el-card>
          <div slot="header">
            <span class="card-title">列表</span>
            <el-button-group>
              <el-button type="success" plain size="mini" v-if="paychannelManager_btn_add" icon="plus"
                         @click="handlerAdd">
                添加
              </el-button>
              <el-button type="primary" plain size="mini" v-if="paychannelManager_btn_edit" icon="edit"
                         @click="handlerEdit">
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
      </el-col>
      <el-col :span="6" v-if="clickbtn">
        <el-card class="box-card">
          <div slot="header">
            <el-switch
              v-model="selecttype"
              active-text="商户"
              inactive-text="平台">
            </el-switch>
            <el-button style="float: right; padding: 3px 0" type="text" @click="clickbtn=false">关闭</el-button>
          </div>

          <el-form v-if="!selecttype" :model="platformForm" ref="ruleForm" label-width="100px">
            <el-form-item label="名称" prop="name">
              <el-input v-model="platformForm.name" :disabled="formEdit"></el-input>
            </el-form-item>
            <el-form-item label="描述" prop="desc">
              <el-input v-model="platformForm.desc" :disabled="formEdit" type="textarea"
                        :autosize="{ minRows: 5, maxRows: 20}"></el-input>
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
            <el-form-item label="名称" prop="name">
              <el-input v-model="merchantForm.name" :disabled="formEdit"></el-input>
            </el-form-item>
            <el-form-item label="商户id" prop="m_id">
              <el-input v-model="merchantForm.m_id" :disabled="formEdit"></el-input>
            </el-form-item>
            <el-form-item label="业务经理" prop="three">
              <el-input v-model="merchantForm.three" :disabled="formEdit"></el-input>
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
      <el-col :span="20" v-if="selecttype&&!clickbtn">
        <el-card>
          <el-button size="small" type="primary" plain @click="addChannelForm=true">添加通道
          </el-button>
          <el-table ref="channelsTable" :data="dynamicChannels" highlight-current-row style="width: 100%">
            <el-table-column type="index" width="50"></el-table-column>
            <el-table-column label='查看明细' type="expand" width="100">
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
            <el-table-column prop='type' label='通道类型'></el-table-column>
            <el-table-column prop='level' label='紧急度'>
              <template slot-scope="scope">
                <el-rate
                  v-model="scope.row.level"
                  :colors="['#99A9BF', '#F7BA2A', '#ff1425']"
                  show-text
                  :texts="['E', 'D', 'C', 'B', 'A']"
                  disabled>
                </el-rate>
              </template>
            </el-table-column>
            <el-table-column prop='platform' label='依附平台'></el-table-column>
            <el-table-column prop='merchant' label='依附商户'></el-table-column>
            <el-table-column label="操作">
              <template slot-scope="scope">
                <el-button v-if="!editChannelForm" @click="editChannelForm=true" type="success" size="small">修改
                </el-button>
                <el-button v-if="editChannelForm" @click="putPayChannels(scope.row)" type="primary" size="small">保存
                </el-button>
                <el-button @click="deletePayChannels(scope.row.id)" type="danger" size="small">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <el-dialog :visible.sync="addChannelForm">
      <add-paychannel @formdata="fetchPayChannelData"></add-paychannel>
    </el-dialog>

  </div>
</template>

<script>
import { getPlatform, postPlatform, putPlatform, deletePlatform } from '@/api/threeticket'
import { getMerchant, postMerchant, putMerchant, deleteMerchant } from 'api/threeticket'
import { getPayChannel, putPayChannel, deletePayChannel } from 'api/threeticket'
import { mapGetters } from 'vuex'
import { LIMIT } from '@/config'
import addPaychannel from './components/addPaychannel.vue'

export default {
  components: { addPaychannel },
  data() {
    return {
      limit: LIMIT,
      platformData: [],
      merchantData: [],
      clickbtn: false,
      selecttype: false,
      formEdit: true,
      formAdd: true,
      formStatus: '',
      paychannelManager_btn_add: true,
      paychannelManager_btn_edit: true,
      platformForm: {
        name: '',
        desc: ''
      },
      platformRules: {
        name: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ]
      },
      merchantForm: {
        platform: '',
        name: '',
        m_id: '',
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
      }
    }
  },
  computed: {
    ...mapGetters([
      'elements'
    ])
  },
  created() {
    this.fetchPlatformData()
    this.fetchMerchantData()
    this.fetchPayChannelData()
    //    this.paychannelManager_btn_add = this.elements['paychannelManager:btn_add']
    //    this.paychannelManager_btn_edit = this.elements['paychannelManager:btn_edit']
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
        this.fetchMerchantData()
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
        this.fetchMerchantData()
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
        this.fetchMerchantData()
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
    putPayChannels(formdata) {
      putPayChannel(formdata.id, formdata).then(response => {
        this.$message({
          message: '恭喜你，更新成功',
          type: 'success'
        })
        this.editChannelForm = false
        this.fetchMerchantData()
      }).catch(error => {
        this.$message.error('更新失败')
        console.log(error)
      })
    },
    deletePayChannels(id) {
      this.$confirm('你确定要删除这个, 是否继续?', '美丽的妲己提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deletePayChannel(id)
        this.fetchMerchantData()
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
      this.formEdit = false
      this.formStatus = 'create'
      this.resetForm()
    },
    handlerEdit() {
      this.clickbtn = true
      this.formEdit = false
      this.formStatus = 'update'
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
      this.formEdit = true
      if (this.selecttype) {
        this.merchantForm = data
        this.listQuery.merchant__name = data.name
      } else {
        this.platformForm = data
        this.listQuery.platform__name = data.name
      }
      this.fetchPayChannelData()
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
