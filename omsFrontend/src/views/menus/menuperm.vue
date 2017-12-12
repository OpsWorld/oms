<template>
  <div class="components-container" style='height:100vh'>
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card>
          <div slot="header">
            <span class="card-title">用户组列表</span>
            <el-button-group>
              <el-button type="success" plain size="mini" @click="add_menu=true">
                添加
              </el-button>
              <el-button type="primary" plain size="mini" v-if="select_group&&edit_menu" @click="edit_menu=false">
                编辑
              </el-button>
              <el-button type="primary" plain size="mini" v-if="select_group&&!edit_menu"
                         @click="putFormSubmit(menuform.id)">
                保存
              </el-button>
            </el-button-group>
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
          </div>
          <el-tree
            :data="firstData"
            :props="menuprops"
            node-key="title"
            default-expand-all
            ref="grouptree"
            :load="fetchNodeData"
            lazy
            show-checkbox
            @check-change="handleCheckChange"
            @node-click="handleNodeClick">
          </el-tree>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card v-if="select_group">
          <div slot="header">
            <span class="card-title">已有按钮列表</span>
          </div>
          <ul>
            <li class="has_element" v-for="item in menuform.elements" :key="item.id">{{item}}</li>
          </ul>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card v-if="selent_menu&&select_group">
          <div slot="header">
            <span class="card-title">资源按钮列表</span>
          </div>
          <div class="head-lavel">
          </div>
          <div>
            <el-table :data="elementData" border style="width: 100%">
              <el-table-column prop='name' label='资源名' sortable='custom'></el-table-column>
              <el-table-column label="操作" v-if="!edit_menu">
                <template slot-scope="scope">
                  <el-button v-if="menuform.elements.indexOf(scope.row.name)<0" type="success" plain size="mini"
                             @click="menuform.elements.push(scope.row.name)">添加
                  </el-button>
                  <el-button v-if="menuform.elements.indexOf(scope.row.name)>-1" type="danger" plain size="mini"
                             @click="menuform.elements.remove(scope.row.name)">移除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-dialog :visible.sync="add_menu" style="z-index: 1024">
      <el-form :model="menuform" ref="addform" label-width="100px">
        <el-form-item label="用户组" prop="group">
          <el-select v-model="menuform.group" filterable placeholder="请选择用户分组">
            <el-option v-for="item in groups" :key="item.name" :value="item.name"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="addFormSubmit('addform')">立即创建</el-button>
          <el-button @click="resetForm('addform')">重置</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import { getFirstmenus, getSecondmenus, getMenumetas } from '@/api/menu'
import { getMenuPerm, postMenuPerm, putMenuPerm } from '@/api/perm'
import { getGroup } from '@/api/user'
import ElButton from '../../../node_modules/element-ui/packages/button/src/button.vue'
import { LIMIT } from '@/config'
import ElDialog from '../../../node_modules/element-ui/packages/dialog/src/component.vue'
import ElCol from 'element-ui/packages/col/src/col'

export default {
  components: {
    ElCol,
    ElDialog,
    ElButton
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
      edit_menu: true,
      add_menu: false,
      menuform: {
        group: '',
        firstmenus: [],
        secondmenus: [],
        elements: []
      },
      firstmenus: [],
      second_title: undefined,
      selent_menu: false
    }
  },
  created() {
    this.fetchFirstData()
    this.fetchSecondData()
    this.fetchRouterData()
    this.getGroups()
  },
  methods: {
    fetchFirstData() {
      getFirstmenus().then(response => {
        this.firstData = response.data
        // 对象map用法
        this.firstData.map(function(data) {
          const parmas = {
            parent__title: data.title
          }
          getSecondmenus(parmas).then(response => {
            data['children'] = response.data
          })
        })
      })
    },
    fetchNodeData(node, resolve) {
      if (node.level === 0) {
        return resolve([{ name: 'region' }])
      }
      if (node.level > 1) return resolve([])

      const parmas = {
        parent__title: node.data.title
      }
      getSecondmenus(parmas).then(response => {
        const data = response.data
        resolve(data)
      })
    },
    fetchSecondData() {
      getSecondmenus().then(response => {
        this.secondData = response.data
      })
    },
    fetchRouterData(group) {
      const parmas = {
        group: group
      }
      getMenuPerm(parmas).then(response => {
        this.routerData = response.data
      })
    },
    fetchElementData() {
      const parmas = {
        limit: this.limit,
        parent__title: this.second_title
      }
      getMenumetas(parmas).then(response => {
        this.elementData = response.data.results
        console.log(this.elementData)
      })
    },
    handleCheckChange(data, checked) {
      if (checked) {
        if (data.parent) {
          this.getIndeterminate()
          this.menuform.secondmenus.push(data.title)
        } else {
          this.menuform.firstmenus.push(data.title)
          this.menuform.firstmenus = [...new Set(this.menuform.firstmenus)]
        }
      } else {
        this.menuform.firstmenus.remove(data.title)
        this.menuform.secondmenus.remove(data.title)
      }
    },
    getIndeterminate() {
      const nodesDOM = this.$refs.grouptree.$el.querySelectorAll('.el-tree-node')
      const nodesVue = [].map.call(nodesDOM, node => node.__vue__)
      const first = nodesVue.filter(item => item.indeterminate === true)
      if (first.length > 0) {
        for (const item of first) {
          this.menuform.firstmenus.push(item.node.data.title)
          this.menuform.firstmenus = [...new Set(this.menuform.firstmenus)]
        }
      }
    },
    handleGroupClick(data) {
      this.select_group = true
      this.menuform = data
      this.menuform.elements = data.elements
      this.$refs.grouptree.setCheckedKeys([])
      this.$refs.grouptree.setCheckedKeys(data.secondmenus)
    },
    handleNodeClick(data) {
      this.second_title = data.title
      this.selent_menu = true
      this.fetchElementData()
    },
    getGroups() {
      getGroup().then(response => {
        this.groups = response.data
      })
    },
    handleSizeChange(val) {
      this.limit = val
      this.fetchElementData()
    },
    handleCurrentChange(val) {
      this.offset = val - 1
      this.fetchElementData()
    },
    addFormSubmit(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          postMenuPerm(this.menuform).then(response => {
            this.$message({
              message: '恭喜你，添加成功',
              type: 'success'
            })
            this.fetchRouterData()
            this.menuform = {
              group: '',
              firstmenus: [],
              secondmenus: [],
              elements: []
            }
            this.add_menu = false
          }).catch(error => {
            this.$message.error('添加失败')
            console.log(error)
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    putFormSubmit(id) {
      putMenuPerm(id, this.menuform).then(response => {
        this.$message({
          message: '恭喜你，更新成功',
          type: 'success'
        })
        this.edit_menu = true
      }).catch(error => {
        this.$message.error('更新失败')
        console.log(error)
      })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
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

  .has_element {
    color: #3aa41d;
    list-style: none;
  }
</style>
