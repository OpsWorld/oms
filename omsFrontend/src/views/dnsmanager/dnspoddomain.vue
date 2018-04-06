<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <data-tables :data="tableData" :search-def="searchDef">
        <el-table-column prop="name" label="域名" sortable="custom"></el-table-column>
        <el-table-column prop="status" label="状态" sortable="custom"></el-table-column>
      </data-tables>
    </el-card>
  </div>
</template>

<script>
import { getDnspodDomain } from 'api/dnsapi'

export default {
  components: {},
  data() {
    return {
      tableData: [],
      tabletotal: 0,
      searchDef: {
        colProps: {
          span: 12
        }
      },
      listQuery: {
        dnsname: 'dnspod01'
      }
    }
  },

  created() {
    this.fetchData()
  },

  methods: {
    fetchData() {
      getDnspodDomain(this.listQuery).then(response => {
        this.tableData = response.data
        this.tabletotal = response.data.length
      })
    }
  }
}
</script>

<style lang='scss'>

</style>
