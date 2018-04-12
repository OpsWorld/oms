<template>
  <div class="components-container" style='height:100vh'>
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card>
          <div slot="header">
            <span class="card-title">dnsapi列表</span>
          </div>
          <div class="head-lavel">
            <div class="table-button">
              <el-button type="primary" icon="el-icon-plus" @click="addForm=true">新建</el-button>
            </div>
            <div class="table-search">
            </div>
          </div>
          <div>
            <el-table :data='tableData' border style="width: 100%">
              <el-table-column prop='name' label='名称' sortable width="100">
                <template slot-scope="scope">
                  <a style="color: #257cff" @click="selectDns(scope.row)">{{scope.row.name}}</a>
                </template>
              </el-table-column>
              <el-table-column prop='type' label='类型' width="80"></el-table-column>
              <el-table-column label="操作">
                <template slot-scope="scope">
                  <el-button type="success" size="mini" @click="editGroup(scope.row)">修改</el-button>
                  <el-button type="danger" size="mini" @click="deleteGroup(scope.row.id)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-card>
      </el-col>
      <el-col :span="18">
        <v-dnspod v-if="showdnspod" :dnsname="dnsname"></v-dnspod>
        <v-godaddy v-if="showgodaddy" :dnsname="dnsname"></v-godaddy>
      </el-col>
    </el-row>

    <el-dialog :visible.sync="addForm">
      <el-form :model="ruleForm" ref="ruleForm" label-width="100px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="ruleForm.name"></el-input>
        </el-form-item>
        <el-form-item label="key / id" prop="key">
          <el-input v-model="ruleForm.key"></el-input>
        </el-form-item>
        <el-form-item label="secret / token" prop="secret">
          <el-input v-model="ruleForm.secret"></el-input>
        </el-form-item>
        <el-form-item label="类型" prop="type">
          <el-select v-model="ruleForm.type" placeholder="请选择类型">
            <el-option v-for="item in Dns_Types" :key="item.id" :value="item"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="备注" prop="desc">
          <el-input v-model="ruleForm.desc"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="addGroupSubmit('ruleForm')">立即创建</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-dialog :visible.sync="editForm">
      <el-form :model="rowdata" ref="rowdata" label-width="150px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="rowdata.name"></el-input>
        </el-form-item>
        <el-form-item label="key / id" prop="key">
          <el-input v-model="rowdata.key"></el-input>
        </el-form-item>
        <el-form-item label="secret / token" prop="secret">
          <el-input v-model="rowdata.secret"></el-input>
        </el-form-item>
        <el-form-item label="类型" prop="type">
          <el-select v-model="rowdata.type" placeholder="请选择类型">
            <el-option v-for="item in Dns_Types" :key="item.id" :value="item"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="备注" prop="desc">
          <el-input v-model="rowdata.desc"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="editGroupSubmit('rowdata')">立即更新</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

  </div>
</template>

<script>
import { getDnsapiKey, postDnsapiKey, putDnsapiKey, deleteDnsapiKey } from 'api/dnsapi'
import vDnspod from './components/dnspod.vue'
import vGodaddy from './components/godaddy.vue'

export default {
  components: { vDnspod, vGodaddy },
  data() {
    return {
      tableData: [],
      ruleForm: {
        name: '',
        key: '',
        secret: '',
        type: '',
        desc: ''
      },
      addForm: false,
      editForm: false,
      rowdata: {},
      Dns_Types: ['dnspod', 'godaddy'],
      showdnspod: false,
      showgodaddy: false,
      dnsname: ''
    }
  },

  created() {
    this.fetchData()
  },

  methods: {
    fetchData() {
      getDnsapiKey().then(response => {
        this.tableData = response.data
      })
    },
    addGroupSubmit() {
      postDnsapiKey(this.ruleForm).then(() => {
        this.$message({
          message: '恭喜你，添加成功',
          type: 'success'
        })
        this.fetchData()
        this.addForm = false
      }).catch(error => {
        this.$message.error('添加失败')
        console.log(error)
      })
    },
    editGroup(row) {
      this.rowdata = row
      this.editForm = true
    },
    editGroupSubmit() {
      putDnsapiKey(this.rowdata.id, this.rowdata).then(() => {
        this.$message({
          message: '恭喜你，修改成功',
          type: 'success'
        })
        this.fetchData()
        this.editForm = false
      }).catch(error => {
        this.$message.error('修改失败')
        console.log(error)
      })
    },
    deleteGroup(id) {
      deleteDnsapiKey(id).then(response => {
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
    selectDns(row) {
      this.dnsname = row.name
      this.showdnspod = false
      this.showgodaddy = false
      if (row.type === 'dnspod') {
        this.showdnspod = true
      } else if (row.type === 'godaddy') {
        this.showgodaddy = true
      }
    }
  }
}
</script>

<style lang='scss'>

</style>
