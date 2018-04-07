<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <el-row :gutter="20">
        <el-col :span="6">
          <el-tabs v-model='listQuery.dnsname' @tab-click="handleClick" type="border-card">
            <el-tab-pane v-for="item in dnsapis" :key="item.id" :label="item.name" :name="item.name">
              <data-tables :data="tableData" :search-def="domain_searchDef" :pagination-def="paginationDef"
                           @row-click="handleRowClick">
                <el-table-column prop="domain" label="域名" sortable="custom"></el-table-column>
                <el-table-column prop="status" label="状态" sortable="custom"></el-table-column>
              </data-tables>
            </el-tab-pane>
          </el-tabs>
        </el-col>
        <el-col :span="18">
          <el-card v-if="showrecord">
            <data-tables :data="recordData" :actions-def="actionsDef" :action-col-def="actionColDef"
                         :search-def="record_searchDef" :pagination-def="paginationDef">
              <el-table-column prop="name" label="记录" sortable="custom"></el-table-column>
              <el-table-column prop="type" label="类型" sortable="custom"></el-table-column>
              <el-table-column prop="data" label="值" sortable="custom"></el-table-column>
              <el-table-column prop="ttl" label="ttl" sortable="custom"></el-table-column>
            </data-tables>
          </el-card>
        </el-col>
      </el-row>
    </el-card>

    <el-dialog :visible.sync="addForm">
      <el-form :model="ruleForm" ref="ruleForm" label-width="100px">
        <el-form-item label="名称" prop="sub_domain">
          <el-input v-model="ruleForm.sub_domain"></el-input>
        </el-form-item>
        <el-form-item label="类型" prop="record_type">
          <el-select v-model="ruleForm.record_type" placeholder="请选择类型">
            <el-option v-for="item in record_types" :key="item.id" :value="item"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="ip" prop="value">
          <el-input v-model="ruleForm.value"></el-input>
        </el-form-item>
        <el-form-item label="ttl" prop="ttl">
          <el-input v-model="ruleForm.ttl"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="addGroupSubmit('ruleForm')">立即创建</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-dialog :visible.sync="editForm">
      <el-form :model="rowdata" ref="rowdata" label-width="100px">
        <el-form-item label="名称" prop="sub_domain">
          <el-input v-model="rowdata.sub_domain" disabled></el-input>
        </el-form-item>
        <el-form-item label="类型" prop="record_type">
          <el-input v-model="rowdata.record_type" disabled></el-input>
        </el-form-item>
        <el-form-item label="值" prop="value">
          <el-input v-model="rowdata.value"></el-input>
        </el-form-item>
        <el-form-item label="ttl" prop="ttl">
          <el-input v-model="rowdata.ttl"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="editGroupSubmit('rowdata')">立即修改</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

  </div>
</template>

<script>
import { getDnsapiKey, getGodaddyDomain, getGodaddyRecord, postGodaddyRecord } from 'api/dnsapi'

export default {
  components: {},
  data() {
    return {
      tableData: [],
      tabletotal: 0,
      dnsapis: [],
      domain_searchDef: {
        colProps: {
          span: 20
        }
      },
      record_searchDef: {
        colProps: {
          span: 8
        }
      },
      listQuery: {
        dnsname: ''
      },
      paginationDef: {
        show: false
      },
      showrecord: false,
      recordData: [],
      actionsDef: {
        colProps: {
          span: 16
        },
        def: [{
          name: '添加',
          icon: 'el-icon-plus',
          handler: () => {
            this.addForm = true
          }
        }]
      },
      addForm: false,
      ruleForm: {
        action: 'create',
        dnsname: '',
        domain: '',
        sub_domain: '',
        value: '',
        record_type: 'A',
        ttl: 600
      },
      record_types: ['A', 'CNAME'],
      editForm: false,
      rowdata: {},
      actionColDef: {
        label: '操作',
        tableColProps: {
          align: 'center'
        },
        def: [{
          handler: row => {
            this.editForm = true
            this.rowdata = {
              action: 'update',
              sub_domain: row.name,
              record_type: row.type,
              value: row.data,
              ttl: row.ttl
            }
          },
          buttonProps: {
            type: 'success'
          },
          name: '编辑'
        }]
      }
    }
  },

  created() {
    this.fetchDnsapiData()
  },

  methods: {
    fetchData(dnsname) {
      this.listQuery.dnsname = dnsname
      getGodaddyDomain(this.listQuery).then(response => {
        this.tableData = response.data
        this.tabletotal = response.data.length
      })
    },
    fetchDnsapiData() {
      const data = {
        type: 'godaddy'
      }
      getDnsapiKey(data).then(response => {
        this.dnsapis = response.data
        this.fetchData(this.dnsapis[0].name)
      })
    },
    fetchRecordData() {
      const data = {
        dnsname: this.listQuery.dnsname,
        domain: this.ruleForm.domain
      }
      this.ruleForm.dnsname = this.listQuery.dnsname
      getGodaddyRecord(data).then(response => {
        this.recordData = response.data
      })
    },
    handleClick(tab) {
      this.fetchData(tab.name)
    },
    handleRowClick(row) {
      this.showrecord = true
      this.ruleForm.domain = row.domain
      this.fetchRecordData()
    },
    addGroupSubmit() {
      postGodaddyRecord(this.ruleForm).then(() => {
        this.$message({
          message: '恭喜你，添加成功',
          type: 'success'
        })
        this.fetchRecordData()
        this.addForm = false
      }).catch(error => {
        this.$message.error('添加失败')
        console.log(error)
      })
    },
    editGroupSubmit() {
      this.rowdata.dnsname = this.ruleForm.dnsname
      this.rowdata.domain = this.ruleForm.domain
      postGodaddyRecord(this.rowdata).then(() => {
        this.$message({
          message: '恭喜你，修改成功',
          type: 'success'
        })
        this.fetchRecordData()
        this.editForm = false
      }).catch(error => {
        this.$message.error('修改失败')
        console.log(error)
      })
    }
  }
}
</script>

<style lang='scss'>

</style>
