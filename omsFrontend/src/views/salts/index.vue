<template>
  <div class="components-container" style='height:100vh'>
    <el-row :gutter="20">
      <el-col :span="14">
        <el-card>
          <div slot="header">
            <span class="title">salt-keys 数据统计</span>
            <el-button style="padding: 3px" type="success" plain @click="getAllkeys">重新获取</el-button>
          </div>
          <el-row class="panel-group" :gutter="60">
            <el-col :span="8" class="card-panel-col">
              <div class='card-panel'>
                <div class="card-panel-icon-wrapper icon-people">
                  <a class="wenzi">已接受</a>
                </div>
                <div class="card-panel-description">
                  <div class="card-panel-text">accepted</div>
                  <p>{{allkeys.accepted}}</p>
                </div>
              </div>
            </el-col>
            <el-col :span="8" class="card-panel-col">
              <div class="card-panel">
                <div class="card-panel-icon-wrapper icon-money">
                  <a class="wenzi">未接受</a>
                </div>
                <div class="card-panel-description">
                  <div class="card-panel-text">unaccept</div>
                  <p>{{allkeys.unaccept}}</p>
                </div>
              </div>
            </el-col>
            <el-col :span="8" class="card-panel-col">
              <div class="card-panel">
                <div class="card-panel-icon-wrapper icon-shoppingCard">
                  <a class="wenzi">已拒绝</a>
                </div>
                <div class="card-panel-description">
                  <div class="card-panel-text">rejected</div>
                  <p>{{allkeys.rejected}}</p>
                </div>
              </div>
            </el-col>
          </el-row>
        </el-card>

        <el-card>
          <div slot="header">
            <span class="title">salt-minions 存活状态</span>
            <el-button style="padding: 3px" type="success" plain @click="getAllminions" v-if="getminions">重新获取
            </el-button>
            <el-button style="padding: 3px" type="success" plain :loading="!getminions" v-if="!getminions">拼命获取中
            </el-button>
          </div>
          <div class="head-lavel">
            <div class="table-button">
              <el-switch
                style="margin: 10px 0;"
                v-model="status"
                active-color="#ff4949"
                inactive-color="#13ce66"
                active-text="Down"
                inactive-text="Up"
                @change="statusChange">
              </el-switch>
            </div>
            <div class="table-search">
              <!--<el-input-->
                <!--placeholder="搜索 ..."-->
                <!--v-model="searchdata"-->
                <!--@keyup.enter.native="searchClick">-->
                <!--<i class="el-icon-search el-input__icon" slot="suffix" @click="searchClick"></i>-->
              <!--</el-input>-->
            </div>
          </div>
          <div>

            <el-table :data="tableData" style="width: 100%" border>
              <el-table-column prop="hostname" label="主机id"></el-table-column>
              <el-table-column prop="status" label="状态" v-if="!status">
                <template slot-scope="scope">
                  <el-tag :color="'13ce66'" size="small">{{scope.row.status}}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="status" label="状态" v-if="status">
                <template slot-scope="scope">
                  <el-tag :color="'13ce66'" size="small">{{scope.row.status}}</el-tag>
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
                :page-size="limit"
                layout="total, sizes, prev, pager, next, jumper"
                :total="tabletotal">
              </el-pagination>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import store from '@/store'
import { LIMIT } from '@/config'
import { mapGetters } from 'vuex'

export default {
  components: {},

  data() {
    return {
      status: true,
      tableData: [],
      tabletotal: 0,
      currentPage: 1,
      limit: LIMIT,
      offset: '',
      pagesize: [10, 25, 50, 100],
      getminions: true,
      searchdata: ''
    }
  },
  computed: {
    ...mapGetters([
      'allkeys',
      'allminions'
    ])
  },
  methods: {
    getAllkeys() {
      store.dispatch('getAllKeys')
    },
    getAllminions() {
      this.getminions = false
      store.dispatch('getAllminions').then(response => {
        this.getminions = true
        this.tableData = this.allminions.up
        this.tabletotal = this.allminions.up.length
      })
    },
    searchClick() {
      this.fetchData()
    },
    handleSizeChange(val) {
      this.limit = val
      this.fetchData()
    },
    handleCurrentChange(val) {
      this.offset = (val - 1) * LIMIT
      this.fetchData()
    },
    statusChange(val) {
      if (val) {
        this.tableData = this.allminions.down
        this.tabletotal = this.allminions.down.length
      } else {
        this.tableData = this.allminions.up
        this.tabletotal = this.allminions.up.length
      }
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
  .title {
    color: #94acff;
    font-size: 20px;
  }

  .panel-group {
    margin-top: 18px;
    .card-panel-col {
      margin-bottom: 32px;
    }
    .card-panel {
      cursor: pointer;
      font-size: 12px;
      position: relative;
      overflow: hidden;
      color: #666;
      background: #fff;
      box-shadow: 4px 4px 40px rgba(0, 0, 0, .05);
      border-color: rgba(0, 0, 0, .05);
      &:hover {
        .card-panel-icon-wrapper {
          color: #fff;
        }
        .icon-people {
          background: #40c9c6;
        }
        .icon-message {
          background: #f4516c;
        }
        .icon-money {
          background: #4b4b4b;
        }
        .icon-shoppingCard {
          background: #f4516c
        }
      }
      .icon-people {
        color: #40c9c6;
      }
      .icon-message {
        color: #f4516c;
      }
      .icon-money {
        color: #4b4b4b;
      }
      .icon-shoppingCard {
        color: #f4516c
      }
      .card-panel-icon-wrapper {
        float: left;
        margin: 14px 0 0 14px;
        padding: 14px;
        transition: all 0.5s ease-out;
        border-radius: 6px;
        border: solid 1px;
      }
      .wenzi {
        font-size: 24px;
      }
      .card-panel-description {
        float: right;
        font-weight: bold;
        margin: 26px;
        .card-panel-text {
          line-height: 18px;
          color: rgba(0, 0, 0, 0.45);
          font-size: 16px;
          margin-bottom: 12px;
        }
        .card-panel-num {
          font-size: 20px;
        }
      }
    }
  }

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
