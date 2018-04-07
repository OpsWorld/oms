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
          <el-card>
            <data-tables :data="recordData" :search-def="record_searchDef" :pagination-def="paginationDef">
              <el-table-column prop="name" label="记录" sortable="custom"></el-table-column>
              <el-table-column prop="type" label="类型" sortable="custom"></el-table-column>
              <el-table-column prop="data" label="值" sortable="custom"></el-table-column>
              <el-table-column prop="ttl" label="ttl" sortable="custom"></el-table-column>
            </data-tables>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script>
import { getDnsapiKey, getGodaddyDomain, getGodaddyRecord } from 'api/dnsapi'

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
          span: 10
        }
      },
      listQuery: {
        dnsname: ''
      },
      paginationDef: {
        show: false
      },
      recordData: []
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
    fetchRecordData(domain) {
      const data = {
        dnsname: this.listQuery.dnsname,
        domain: domain
      }
      getGodaddyRecord(data).then(response => {
        this.recordData = response.data
      })
    },
    handleClick(tab) {
      this.fetchData(tab.name)
    },
    handleRowClick(row) {
      this.fetchRecordData(row.domain)
    }
  }
}
</script>

<style lang='scss'>

</style>
