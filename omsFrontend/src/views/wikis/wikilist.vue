<template>
  <div class="components-container" style='height:100vh'>
    <el-card class="wiki">
      <div class="wiki-header">
        <H2>OMS文档知识库</H2>
        <div class="wiki-search">
          <el-input placeholder="标题或内容" v-model="listQuery.search" class="input-with-select">
            <el-select v-model="selectdata" slot="prepend" placeholder="请选择类型" size="small" @change="selectClick">
              <el-option v-for="item in types" :key="item.id" :value="item.name"></el-option>
            </el-select>
            <el-button slot="append" icon="el-icon-search" @click="searchClick"></el-button>
          </el-input>
        </div>
        <hr class="heng"/>
      </div>
      <div class="wiki-content">
        <div v-for="item in tableData" :key="item.id">
            <router-link :to="'viewwiki/' + item.id">
              <a class="title">{{item.title}}</a>
            </router-link>
            <div class="meta">
              <el-button type="danger" plain size="mini">{{item.type}}</el-button>
              <a class="author">
                <i class="fa fa-user"></i>{{item.create_user}}
              </a>
              <a class="create_time">
                <i class="fa fa-calendar"></i>{{item.create_time | formatTime}}
              </a>
            </div>
            <hr class="heng"/>
        </div>
        <div class="table-pagination">
          <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page.sync="currentPage"
            :page-size="listQuery.limit"
            layout="prev, pager, next"
            :total="tabletotal">
          </el-pagination>
        </div>
      </div>
    </el-card>
  </div>
</template>
<script>
import { getWiki } from 'api/wiki'
import { LIMIT } from '@/config'
import VueMarkdown from 'vue-markdown' // 前端显示
import { getTickettype } from 'api/workticket'

export default {
  components: {
    VueMarkdown
  },
  data() {
    return {
      selectdata: '',
      types: [{ id: 999, name: '全部' }],
      tableData: [],
      tabletotal: 0,
      currentPage: 1,
      listQuery: {
        limit: LIMIT,
        offset: '',
        type__name: '',
        search: ''
      }
    }
  },
  created() {
    this.fetchData()
    this.getTicketType()
  },
  methods: {
    fetchData() {
      getWiki(this.listQuery).then(response => {
        this.tableData = response.data.results
        this.tabletotal = response.data.count
      })
    },
    searchClick() {
      this.fetchData()
    },
    selectClick(e) {
      if (e === '全部') {
        this.listQuery.type__name = ''
      } else {
        this.listQuery.type__name = e
      }
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
    getTicketType() {
      getTickettype().then(response => {
        this.types = this.types.concat(response.data)
      })
    }
  }
}
</script>

<style lang='scss'>
  .wiki {
    width: 80%;
    text-align: center;
    .wiki-search {
      margin: 0 auto;
      width: 500px;
      .el-select .el-input {
        width: 120px;
      }
      .input-with-select .el-input-group__prepend {
        background-color: #fff;
      }
    }
    .wiki-content {
      text-align: left;
      margin: 10px 20%;
      .title {
        margin: -7px 0 4px;
        display: inherit;
        font-size: 18px;
        line-height: 1.5;
        color: #000000;
        &:hover {
          text-decoration: underline;
          color: #2f0aff;
        }
      }
      .meta {
        margin-top: 5px;
        font-size: 12px;
        font-weight: 400;
        line-height: 20px;
        color: rgba(128, 128, 128, 0.82);
        a {
          padding: 0 10px;
          i {
            padding-right: 5px;
          }
          &:hover {
            color: rgb(75, 75, 75);
          }
        }
      }
      .abstract {
        max-height: 100px;
      }
    }
  }
</style>
