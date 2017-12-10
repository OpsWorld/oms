<template>
  <div class="components-container" style='height:100vh'>
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card>
          <div slot="header">
            <span class="card-title">用户组列表</span>
            <el-button type="primary" plain size="mini" v-if="select_group" @click="edit_menu=true">
              编辑
            </el-button>
          </div>
          <div>
            <el-tree
              :data="routerData"
              :props="routerprops"
              accordion
              @node-click="handleGroupClick">
            </el-tree>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card>
          <div slot="header">
            <span class="card-title">菜单列表</span>
            <el-button v-if="edit_menu" type="primary" plain size="mini">
              保存
            </el-button>
          </div>
          <el-tree
            :data="firstData"
            :props="menuprops"
            node-key="name"
            default-expand-all
            ref="grouptree"
            :load="fetchSecondData"
            lazy
            show-checkbox
            @check-change="handleCheckChange"
            @node-click="handleNodeClick">
          </el-tree>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <div slot="header">
            <span class="card-title">资源按钮列表</span>
            <el-button v-if="edit_menu" type="primary" plain size="mini">
              保存
            </el-button>
          </div>
          <div class="head-lavel">
            <div class="table-search">
              <el-input
                placeholder="搜索 ..."
                v-model="searchdata"
                @keyup.enter.native="searchClick">
                <i class="el-icon-search el-input__icon" slot="suffix" @click="searchClick"></i>
              </el-input>
            </div>
          </div>
          <div>
            <el-table :data="elementData" border style="width: 100%">
              <el-table-column prop='name' label='资源名' sortable='custom'></el-table-column>
              <el-table-column prop='code' label='资源代码'></el-table-column>
            </el-table>
          </div>
          <div class="table-pagination">
            <el-pagination
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
              :current-page.sync="currentPage"
              :page-sizes="pagesize"
              :page-size="limit"
              layout="prev, pager, next, sizes"
              :total="tabletotal">
            </el-pagination>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { getFirstmenus, getSecondmenus, getMenumetas } from '@/api/menu'
import { getMenuPerm } from '@/api/perm'
import { getGroup } from '@/api/user'
import addMenuperm from './addmenuperm.vue'
import ElButton from '../../../node_modules/element-ui/packages/button/src/button.vue'
import { LIMIT } from '@/config'

export default {
  components: {
    ElButton,
    addMenuperm
  },
  data() {
    return {
      firstData: [],
      secondData: [],
      elementData: [],
      routerData: [],
      menuprops: {
        label: 'title',
        children: 'children'
      },
      routerprops: {
        label: 'group'
      },
      count: 1,
      groups: [],
      tabletotal: 0,
      searchdata: '',
      currentPage: 1,
      limit: LIMIT,
      offset: '',
      pagesize: [10, 25, 50, 100],
      select_group: false,
      edit_menu: false
    }
  },
  created() {
    this.fetchFirstData()
    this.fetchRouterData()
    this.fetchElementData()
    this.getGroups()
  },
  methods: {
    fetchFirstData() {
      getFirstmenus().then(response => {
        this.firstData = response.data.results
        // 对象map用法
        this.firstData.map(function(data) {
          const parmas = {
            parent__title: data.title
          }
          getSecondmenus(parmas).then(response => {
            data['children'] = response.data.results
          })
        })
      })
    },
    fetchSecondData(node, resolve) {
      if (node.level === 0) {
        return resolve([{ name: 'region' }])
      }
      if (node.level > 1) return resolve([])

      const parmas = {
        parent__title: node.data.title
      }
      getSecondmenus(parmas).then(response => {
        const data = response.data.results
        resolve(data)
      })
    },
    fetchRouterData(group) {
      const parmas = {
        group: group
      }
      getMenuPerm(parmas).then(response => {
        this.routerData = response.data.results
      })
    },
    fetchElementData(title) {
      const parmas = {
        parent__title: title
      }
      getMenumetas(parmas).then(response => {
        this.elementData = response.data.results
      })
    },
    handleCheckChange(data, checked, indeterminate) {
    },
    handleGroupClick(data) {
      this.select_group = true
      this.$refs.grouptree.setCheckedKeys([])
      this.$refs.grouptree.setCheckedKeys(data.secondmenus)
    },
    handleNodeClick(data) {
      this.fetchElementData(data.title)
    },
    getGroups() {
      getGroup().then(response => {
        this.groups = response.data.results
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
      this.offset = val - 1
      this.fetchData()
    }
  }
}
</script>

<style>
  .card-title {
    padding-right: 30px;
  }

  .head-lavel {
    padding-bottom: 50px;
  }

  .table-search {
    float: right;
  }

  .table-pagination {
    padding: 10px 0;
    float: right;
  }
</style>
