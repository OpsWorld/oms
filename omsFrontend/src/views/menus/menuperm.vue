<template>
  <div class="components-container" style='height:100vh'>
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card>
          <el-tree
            :data="firstData"
            :props="props"
            :load="fetchSecondData"
            :accordion="true"
            lazy
            show-checkbox
            @check-change="handleCheckChange">
          </el-tree>
        </el-card>
      </el-col>
      <el-col :span="16">
        <el-card>
          <div class="grid-content bg-purple"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { getFirstmenus, getSecondmenus } from '@/api/menu'

export default {
  data() {
    return {
      firstData: [],
      props: {
        label: 'name',
        children: ''
      },
      count: 1
    }
  },
  created() {
    this.fetchFirstData()
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
        parent__name: node.data.name
      }
      getSecondmenus(parmas).then(response => {
        const data = response.data.results
        setTimeout(() => {
          resolve(data)
        }, 500)
      })
    },
    handleCheckChange(data, checked, indeterminate) {
      console.log(data, checked, indeterminate)
    },
    handleNodeClick(data) {
      console.log(data)
    },
    loadNode(node, resolve) {
      if (node.level === 0) {
        return resolve([{ name: 'region1' }, { name: 'region2' }])
      }
      if (node.level > 3) return resolve([])

      var hasChild
      if (node.data.name === 'region1') {
        hasChild = true
      } else if (node.data.name === 'region2') {
        hasChild = false
      } else {
        hasChild = Math.random() > 0.5
      }

      setTimeout(() => {
        var data
        if (hasChild) {
          data = [{
            name: 'zone' + this.count++
          }, {
            name: 'zone' + this.count++
          }]
        } else {
          data = []
        }

        resolve(data)
      }, 500)
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
