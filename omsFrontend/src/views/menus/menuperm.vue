<template>
  <div class="components-container" style='height:100vh'>
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card>
          <div slot="header" class="clearfix">
            <span>菜单列表</span>
          </div>
          <el-tree
            :data="firstData"
            :props="menuprops"
            :load="fetchSecondData"
            :accordion="true"
            lazy
            show-checkbox
            @check-change="handleCheckChange">
          </el-tree>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <div slot="header" class="clearfix">
            <span>用户组列表</span>
            <el-button-group>
              <el-button type="success" plain size="mini" icon="plus">
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
            :load="fetchSecondData"
            :accordion="true"
            lazy
            @check-change="handleCheckChange">
          </el-tree>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { getFirstmenus, getSecondmenus } from '@/api/menu'
import { getMenuPerm } from '@/api/perm'

export default {
  data() {
    return {
      firstData: [],
      routerData: [],
      menuprops: {
        label: 'title',
        children: ''
      },
      routerprops: {
        label: 'group',
        children: ''
      },
      count: 1
    }
  },
  created() {
    this.fetchFirstData()
    this.fetchRouterData()
  },
  methods: {
    fetchFirstData() {
      getFirstmenus().then(response => {
        this.firstData = response.data.results
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
        setTimeout(() => {
          resolve(data)
        }, 500)
      })
    },
    fetchRouterData() {
      getMenuPerm().then(response => {
        this.routerData = response.data.results
      })
    },
    handleCheckChange(data, checked, indeterminate) {
      console.log(data, checked, indeterminate)
    },
    handleNodeClick(data) {
      console.log(data)
    }
  }
}
</script>

<style>
  .bg-purple {
    background: #d3dce6;
  }

  .grid-content {
    border-radius: 4px;
    min-height: 36px;
  }
</style>
