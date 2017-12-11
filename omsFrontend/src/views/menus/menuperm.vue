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
          </div>
          <div class="head-lavel">
            <div class="table-search">
              <el-select v-model="select_menu" placeholder="请选择二级菜单">
                <el-option v-for="item in secondData" :key="item.id" :value="item.title"></el-option>
              </el-select>
            </div>
          </div>
          <div>
            <el-table :data="elementData" border style="width: 100%">
              <el-table-column prop='name' label='资源名' sortable='custom'></el-table-column>
              <el-table-column prop='code' label='资源代码'></el-table-column>
              <el-table-column label="操作">
                <template slot-scope="scope">
                  <el-button type="success" plain size="mini">添加</el-button>
                  <el-button type="danger" plain size="mini">删除</el-button>
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
              :page-size="limit"
              layout="prev, pager, next, sizes"
              :total="tabletotal">
            </el-pagination>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-dialog :visible.sync="add_menu">
      <el-form :model="menuform" :rules="ruleaddfrom" ref="addform" label-width="100px">
        <el-form-item label="用户组" prop="group">
          <el-select v-model="menuform.group" placeholder="请选择用户分组">
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

export default {
  components: {
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
      ruleaddfrom: {
        group: [
          { required: true, message: '请选择用户组', trigger: 'change' }
        ]
      },
      select_menu: '',
      firstmenus: []
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
      console.log(data, checked, indeterminate)
      if (checked) {
        if (data.parent) {
          this.menuform.secondmenus.push(data.title)
        } else {
          this.menuform.firstmenus.push(data.title)
        }
      } else {
        this.menuform.secondmenus.remove(data.title)
      }
      this.menuform.firstmenus = [...new Set(this.menuform.firstmenus)]
    },
    handleGroupClick(data) {
      this.select_group = true
      this.menuform = data
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
        this.fetchRouterData()
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

  .table-search {
    float: right;
  }

  .table-pagination {
    padding: 10px 0;
    float: right;
  }
</style>
