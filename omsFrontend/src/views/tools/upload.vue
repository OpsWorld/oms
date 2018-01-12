<template>
  <div class="components-container" style='height:100vh'>
        <el-card>
            <div class="head-lavel">
                <div class="table-button">
                </div>
                <div class="table-search">
                    <el-input @keyup.enter.native="handleFilter" style="width: 110px;" class="filter-item"
                              placeholder="上传人员"
                              v-model="listQuery.username__contains">
                    </el-input>
                    <el-input @keyup.enter.native="handleFilter" style="width: 110px;" class="filter-item"
                              placeholder="文件类型"
                              v-model="listQuery.type">
                    </el-input>
                    <!--<el-date-picker-->
                    <!--class="filter-item"-->
                    <!--v-model="datefilter"-->
                    <!--type="daterange"-->
                    <!--placeholder="选择日期范围">-->
                    <!--</el-date-picker>-->
                    <el-button class="filter-item" type="primary" icon="search" @click="searchClick">搜索
                    </el-button>
                </div>
            </div>
            <div>
                <el-table :data="tableData" @selection-change="handleSelectionChange" border style="width: 100%">
                    <el-table-column type="selection"></el-table-column>
                    <el-table-column prop='username' label='上传用户' sortable></el-table-column>
                    <el-table-column prop='filename' label='文件名' sortable></el-table-column>
                    <el-table-column prop='archive' label='文件归档' sortable></el-table-column>
                    <el-table-column prop='type' label='文件类型' sortable></el-table-column>
                    <el-table-column prop='size' label='文件大小'></el-table-column>
                    <el-table-column prop='create_time' label='文件日期' sortable></el-table-column>
                    <!--<el-table-column label="操作">-->
                        <!--<template slot-scope="scope">-->
                            <!--<el-button type="success" size="small"><a :href="scope.row.file" target="_blank">查看文件</a>-->
                            <!--</el-button>-->
                        <!--</template>-->
                    <!--</el-table-column>-->
                </el-table>
            </div>
            <div class="table-footer">
                <div class="table-button">
                    <el-button type="danger" :disabled="butstatus" @click="deleteForm">删除记录</el-button>
                </div>
                <div class="table-pagination">
                    <el-pagination
                            @size-change="handleSizeChange"
                            @current-change="handleCurrentChange"
                            :current-page.sync="listQuery.offset"
                            :page-sizes="pagesize"
                            :page-size="listQuery.limit"
                            layout="prev, pager, next, sizes"
                            :total="tabletotal">
                    </el-pagination>
                </div>
            </div>
        </el-card>
        <el-dialog :visible.sync="showPhoto">
            <img :src="photo" class="photo-align">
        </el-dialog>
    </div>
</template>

<script>
import { getUploadList, deleteUpload } from 'api/tool'
import { LIMIT } from '@/config'
import format from '@/utils/dateformat'

export default {
  components: {},
  data() {
    return {
      tableData: [],
      tabletotal: 0,
      searchdata: '',
      pagesize: [10, 25, 50, 100],
      rowdata: {},
      selectId: [],
      butstatus: true,
      listQuery: {
        offset: null,
        limit: LIMIT,
        username__contains: '',
        type: ''
      },
      datefilter: [],
      photo: '',
      showPhoto: false
    }
  },

  created() {
    this.fetchData()
  },

  methods: {
    fetchData() {
      getUploadList(this.listQuery).then(response => {
        this.tableData = response.data.results
        this.tabletotal = response.data.count
      })
    },

    handleSelectionChange(val) {
      this.selectId = []
      for (var i = 0, len = val.length; i < len; i++) {
        this.selectId.push(val[i].id)
      }
      if (this.selectId.length > 0) {
        this.butstatus = false
      } else {
        this.butstatus = true
      }
    },

    handleIconUserClick() {
      this.listQuery.username__contains = ''
    },
    handleIconTypeClick() {
      this.listQuery.type = ''
    },
    searchClick() {
      this.listQuery.date_gte = format(new Date(this.datefilter[0]), 'YYYY-MM-DD')
      this.listQuery.date_lte = format(new Date(this.datefilter[1]), 'YYYY-MM-DD')
      this.fetchData()
    },
    handleSizeChange(val) {
      this.listQuery.limit = val
      this.fetchData()
    },
    handleCurrentChange(val) {
      console.log(val)
      this.listQuery.offset = (val - 1) * LIMIT
      this.fetchData()
    },
    deleteForm() {
      console.log(this.selectId)
      for (var i = 0, len = this.selectId.length; i < len; i++) {
        deleteUpload(this.selectId[i]).then(response => {
          delete this.selectId[i]
        })
      }
      setTimeout(this.fetchData, 1000)
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
</style>
