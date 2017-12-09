<template>
  <div class="components-container" style='height:100vh'>
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card>
          <div slot="header">
            <span class="card-title">用户组列表</span>
            <el-button-group>
              <el-button type="success" plain size="mini" icon="plus" @click="addForm=true">
                添加
              </el-button>
              <el-button type="primary" plain size="mini" icon="edit">
                编辑
              </el-button>
              <el-button type="danger" plain size="mini" icon="delete">
                删除
              </el-button>
            </el-button-group>
          </div>
          <el-tree
            :data="routerData"
            :props="routerprops"
            accordion
            @node-click="handleNodeClick">
          </el-tree>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <div slot="header">
            <span class="card-title">菜单列表</span>
          </div>
          <el-tree
            :data="firstData"
            :props="menuprops"
            node-key="name"
            default-expand-all
            ref="menutree"
            :load="fetchSecondData"
            lazy
            show-checkbox
            @check-change="handleCheckChange">
          </el-tree>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <div slot="header">
            <span class="card-title">资源列表</span>
          </div>
          <el-tree
            :data="firstData"
            :props="menuprops"
            node-key="name"
            default-expand-all
            ref="menutree"
            :load="fetchSecondData"
            lazy
            show-checkbox
            @check-change="handleCheckChange">
          </el-tree>
        </el-card>
      </el-col>
    </el-row>
    <el-dialog :visible.sync="addForm">
      <add-menuperm :treedata="firstData" :groupdata="groups"></add-menuperm>
    </el-dialog>
  </div>
</template>

<script>
import { getFirstmenus, getSecondmenus } from '@/api/menu'
import { getMenuPerm } from '@/api/perm'
import { getGroup } from '@/api/user'
import addMenuperm from './addmenuperm.vue'

export default {
  components: { addMenuperm },
  data() {
    return {
      firstData: [],
      secondData: [],
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
      addForm: false
    }
  },
  created() {
    this.fetchFirstData()
    this.fetchRouterData()
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
    fetchRouterData() {
      getMenuPerm().then(response => {
        this.routerData = response.data.results
      })
    },
    handleCheckChange(data, checked, indeterminate) {
    },
    handleNodeClick(data) {
      this.$refs.menutree.setCheckedKeys([])
      this.$refs.menutree.setCheckedKeys(data.secondmenus)
    },
    addFormSubmit(Form) {

    },
    getGroups() {
      getGroup().then(response => {
        this.groups = response.data.results
      })
    }
  }
}
</script>

<style>
  .card-title {
    padding-right: 30px;
  }
</style>
