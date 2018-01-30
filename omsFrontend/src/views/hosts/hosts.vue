<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <div class="head-lavel">
        <div class="table-button">
          <el-button type="primary" icon="el-icon-plus" @click="addForm=true">新建</el-button>
          <el-button-group>
            <el-button type="primary" plain size="mini" @click="getHostFromSalt('create')" :loading="autocreate">自动获取
            </el-button>
            <el-button type="success" plain size="mini" @click="getHostFromSalt('update')" :loading="autoupdate">自动更新
            </el-button>
          </el-button-group>
          <el-radio-group v-model="listQuery.status" @change="changeStatus" style="margin-left: 20px">
            <el-radio label="noused">未使用</el-radio>
            <el-radio label="used">使用中</el-radio>
            <el-radio label="broken">故障</el-radio>
            <el-radio label="trash">报废</el-radio>
          </el-radio-group>
        </div>
        <div class="table-search">
          <el-input
            placeholder="主机名或ip"
            v-model="searchdata"
            @keyup.enter.native="searchClick">
            <i class="el-icon-search el-input__icon" slot="suffix" @click="searchClick"></i>
          </el-input>
        </div>
      </div>
      <div>
        <el-table :data='tableData' border style="width: 100%">
          <el-table-column type="expand">
            <template slot-scope="props">
              <el-form label-position="left" inline class="table-expand">
                <el-form-item label="网关" prop="gateway">
                  <span>{{ props.row.gateway }}</span>
                </el-form-item>
                <el-form-item label="系统" prop="os">
                  <span>{{ props.row.os }}</span>
                </el-form-item>
                <el-form-item label="cpu信息" prop="cpu">
                  <span>{{ props.row.cpu }}</span>
                </el-form-item>
                <el-form-item label="内存信息" prop="memory">
                  <span>{{ props.row.memory }}</span>
                </el-form-item>
                <el-form-item label="磁盘信息" prop="disk">
                  <a v-for="disk in props.row.disk.split('|')" :key="disk.id" style="margin-right: 5px" size="mini">
                    <el-tag size="mini">{{disk.split(' ')[0]}}</el-tag>
                    <span>{{disk.split(' ')[1]}}</span>
                  </a>
                </el-form-item>
                <el-form-item label="备注" prop="desc">
                  <span>{{ props.row.desc }}</span>
                </el-form-item>
              </el-form>
            </template>
          </el-table-column>
          <el-table-column prop='hostname' label='主机名'></el-table-column>
          <el-table-column prop='an' label='资产编号'></el-table-column>
          <el-table-column prop='ip' label='ip'>
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper" style="text-align: center">
                <el-tag v-for="item in scope.row.ip.split('|')" :key="item.id" size="mini" style="margin-right: 3px">
                  {{item}}
                </el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='idc' label='机房'></el-table-column>
          <el-table-column prop='asset_type' label='类型'>
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper" style="text-align: center">
                <el-tag style="color: #000" :color="ASSET_TYPE[scope.row.asset_type].color">
                  {{ASSET_TYPE[scope.row.asset_type].type}}
                </el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='status' label='状态'>
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper" style="text-align: center">
                <el-tag :type="ASSET_STATUS[scope.row.status].type">
                  {{ASSET_STATUS[scope.row.status].status}}
                </el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button @click="handleEdit(scope.row)" type="success" size="small">修改</el-button>
              <el-button @click="deleteGroup(scope.row.id)" type="danger" size="small">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div class="table-footer">

        <div class="table-button">
        </div>
        <div class="table-pagination">
          <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page.sync="currentPage"
            :page-sizes="pagesize"
            :page-size="listQuery.limit"
            layout="prev, pager, next, sizes"
            :total="tabletotal">
          </el-pagination>
        </div>
      </div>
    </el-card>
    <el-dialog :visible.sync="addForm">
      <add-obj @formdata="addGroupSubmit"></add-obj>
    </el-dialog>
    <el-dialog :visible.sync="editForm" @close="closeEditForm">
      <edit-obj :rowdata="rowdata" @formdata="editGroupSubmit"></edit-obj>
    </el-dialog>
  </div>
</template>

<script>
import { postHost, getHost, putHost, deleteHost } from '@/api/host'
import { getSyncRemoteServer } from 'api/salt'
import { LIMIT } from '@/config'
import addObj from './components/addhost.vue'
import editObj from './components/edithost.vue'

export default {
  components: { addObj, editObj },
  data() {
    return {
      tableData: [],
      tabletotal: 0,
      searchdata: '',
      currentPage: 1,
      listQuery: {
        limit: LIMIT,
        offset: '',
        search: '',
        status: 'used'
      },
      limit: LIMIT,
      offset: '',
      pagesize: [10, 25, 50, 100],
      addForm: false,
      editForm: false,
      viewForm: false,
      groupName: '',
      rowdata: {},
      ASSET_TYPE: {
        'physical': { 'type': '物理机', 'color': '#c0dbff' },
        'virtual': { 'type': '虚拟机', 'color': '#19ddff' },
        'container': { 'type': '容器', 'color': '#f06292' },
        'network': { 'type': '网络设备', 'color': '#e6d664' },
        'other': { 'type': '其他设备', 'color': '#838383' }
      },
      ASSET_STATUS: {
        'used': { 'status': '使用中', 'type': 'primary' },
        'noused': { 'status': '未使用', 'type': 'info' },
        'broken': { 'status': '故障', 'type': 'danger' },
        'trash': { 'status': '废弃', 'type': 'warning' }
      },
      autocreate: false,
      autoupdate: false
    }
  },

  created() {
    this.fetchData()
  },

  methods: {
    fetchData() {
      getHost(this.listQuery).then(response => {
        this.tableData = response.data.results
        this.tabletotal = response.data.count
      })
    },
    addGroupSubmit(formdata) {
      postHost(formdata).then(response => {
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
    editGroupSubmit(formdata) {
      putHost(this.rowdata.id, formdata).then(response => {
        this.$message({
          message: '恭喜你，更新成功',
          type: 'success'
        })
        this.fetchData()
        this.editForm = false
      }).catch(error => {
        this.$message.error('更新失败')
        console.log(error)
      })
    },
    deleteGroup(id) {
      deleteHost(id).then(response => {
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
    closeEditForm() {
      this.fetchData()
    },
    handleEdit(row) {
      this.editForm = true
      this.rowdata = row
    },
    searchClick() {
      this.listQuery.search = this.searchdata
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
    changeStatus(val) {
      this.listQuery.status = val
      if (val === 'noused') {
        this.havenoused = true
      }
      this.fetchData()
    },
    getHostFromSalt(val) {
      if (val === 'create') {
        this.autocreate = true
        getSyncRemoteServer(val).then(response => {
          this.autocreate = false
          this.listQuery.status = 'noused'
          this.fetchData()
        }).catch(error => {
          this.autocreate = false
          this.listQuery.status = 'noused'
          this.fetchData()
          console.log(error)
        })
      } else {
        this.autoupdate = true
        getSyncRemoteServer(val).then(response => {
          this.autoupdate = false
          this.fetchData()
        }).catch(error => {
          this.autoupdate = false
          this.fetchData()
          console.log(error)
        })
      }
    }
  }
}
</script>

<style lang='scss'>
  .head-lavel {
    padding-bottom: 50px;
  }

  .table-button {
    padding: 10px 0;
    float: left;
  }

  .table-search {
    float: right;
    padding: 10px 0;
  }

  .table-pagination {
    padding: 10px 0;
    float: right;
  }

  .table-expand {
    font-size: 0;
    .el-form-item {
      margin-right: 0;
      margin-bottom: 0;
      width: 50%;
      .el-form-item__label {
        width: 90px;
        color: #99a9bf;
      }
    }
  }
</style>
