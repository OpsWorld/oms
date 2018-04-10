<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <div class="head-lavel">
        <div class="table-button">
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
          <el-table-column label="记录" type="expand" width="50">
            <template slot-scope="scope">
              <el-table :data='scope.row.recordData' border style="width: 100%">
                <el-table-column prop='name' label='名称' sortable></el-table-column>
                <el-table-column prop='status' label='状态'>
                  <template slot-scope="props">
                    <div slot="reference" class="name-wrapper" style="text-align: center; color: rgb(0,0,0)">
                      <el-tag>
                        {{Dns_Status[props.row.status]}}
                      </el-tag>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column prop='type' label='类型'></el-table-column>
                <el-table-column prop='value' label='值'></el-table-column>
                <el-table-column prop='ttl' label='ttl'></el-table-column>
              </el-table>
            </template>
          </el-table-column>
          <el-table-column prop='name' label='名称' sortable>
            <!--<template slot-scope="scope">-->
              <!--<router-link :to="'dnsrecords/' + scope.row.name">-->
                <!--<a style="color: #257cff">{{scope.row.name}}</a>-->
              <!--</router-link>-->
            <!--</template>-->
          </el-table-column>
          <el-table-column prop='status' label='状态' width="100">
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper" style="text-align: center; color: rgb(0,0,0)">
                <el-tag>
                  {{Dns_Status[scope.row.status]}}
                </el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='type' label='类型' width="100"></el-table-column>
          <el-table-column prop='dnsname' label='属于' width="100"></el-table-column>
          <el-table-column prop='use' label='用途'></el-table-column>
          <el-table-column prop='desc' label='备注'></el-table-column>
          <el-table-column label="操作" width="300">
            <template slot-scope="scope">
              <el-button type="primary" size="small" @click="syncGroup(scope.row)">同步record</el-button>
              <el-button type="success" size="small" @click="updateDesc(scope.row)">更新</el-button>
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
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="rowdata.status">
            <el-radio v-for="item in Object.keys(Dns_Status)" :key="item" :label="item">{{Dns_Status[item]}}</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="用途" prop="use">
          <el-input v-model="rowdata.use" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
        </el-form-item>
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
import {
  getDnsDomain,
  postDnspodRecord,
  postGodaddyRecord,
  patchDnsDomain,
  getDnsRecord
} from 'api/dnsapi'
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
        search: ''
      },
      Dns_Status: {
        0: '使用中',
        1: '备用',
        2: '被墙'
      },
      Dns_Types: ['dnspod', 'godaddy'],
      addForm: false,
      rowdata: {
        status: '',
        use: '',
        desc: ''
      }
    }
  },

  created() {
    this.fetchData()
  },

  methods: {
    fetchData() {
      getDnsDomain(this.listQuery).then(response => {
        this.tableData = response.data.results
        this.tabletotal = response.data.count
        this.tableData.map(function(item) {
          const parmas = {
            domain__name: item.name
          }
          getDnsRecord(parmas).then(res => {
            item.recordData = res.data
          })
        })
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
    syncGroup(row) {
      row.action = 'sync'
      row.domain = row.name
      this.$message({
        message: '正在同步中，请稍后',
        type: 'info'
      })
      if (row.type === 'dnspod') {
        postDnspodRecord(row).then(() => {
          this.$message({
            message: '同步成功',
            type: 'success'
          })
        })
      } else if (row.type === 'godaddy') {
        postGodaddyRecord(row).then(() => {
          this.$message({
            message: '同步成功',
            type: 'success'
          })
        })
      }
    },
    updateDesc(row) {
      this.addForm = true
      this.rowdata = row
    },
    changeDesc() {
      patchDnsDomain(this.rowdata.id, this.rowdata).then(() => {
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
