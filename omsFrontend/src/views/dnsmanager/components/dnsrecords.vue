<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <div class="head-lavel">
        <div class="table-button">
          <a>{{listQuery.domain__name}}</a>
        </div>
        <div class="table-search">
          <el-input
            placeholder="搜索 ..."
            v-model="listQuery.search"
            @keyup.enter.native="searchClick">
            <i class="el-icon-search el-input__icon" slot="suffix" @click="searchClick"></i>
          </el-input>
        </div>
      </div>
      <div>
        <el-table :data='tableData' border style="width: 100%">
          <el-table-column prop='name' label='名称' sortable></el-table-column>
          <el-table-column prop='status' label='状态'>
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper" style="text-align: center; color: rgb(0,0,0)">
                <el-tag>
                  {{Dns_Status[scope.row.status]}}
                </el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='type' label='类型'></el-table-column>
          <el-table-column prop='value' label='值'></el-table-column>
          <el-table-column prop='ttl' label='ttl'></el-table-column>
          <el-table-column prop='desc' label='备注'></el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button type="success" size="small" @click="updateDesc(scope.row)">更新备注</el-button>
            </template>
          </el-table-column>
        </el-table>
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
    </el-card>

    <el-dialog :visible.sync="addForm">
      <el-form label-width="90px">
        <el-form-item label="备注" prop="desc">
          <el-input v-model="rowdata.desc" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="changeDesc">确 定</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import { getDnsRecord, patchDnsRecord } from 'api/dnsapi'
import { LIMIT, pagesize, pageformat } from '@/config'

export default {
  components: {},
  data() {
    return {
      tableData: [],
      tabletotal: 0,
      currentPage: 1,
      pagesize: pagesize,
      pageformat: pageformat,
      listQuery: {
        limit: LIMIT,
        offset: '',
        search: '',
        domain__name: this.$route.params.domain
      },
      Dns_Status: {
        0: '启用',
        1: '停用'
      },
      Dns_Types: ['dnspod', 'godaddy'],
      addForm: false,
      rowdata: {}
    }
  },

  created() {
    this.fetchData()
  },

  methods: {
    fetchData() {
      getDnsRecord(this.listQuery).then(response => {
        this.tableData = response.data.results
        this.tabletotal = response.data.count
      })
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
    updateDesc(row) {
      this.addForm = true
      this.rowdata = row
    },
    changeDesc() {
      patchDnsRecord(this.rowdata.id, this.rowdata).then(() => {
        this.$message({
          message: '更新成功',
          type: 'success'
        })
        this.addForm = false
        this.fetchData()
      })
    }
  }
}
</script>

<style lang='scss'>

</style>
