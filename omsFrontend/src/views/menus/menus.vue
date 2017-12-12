<template>
  <div class="components-container" style='height:100vh'>
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card>
          <div slot="header">
            <span class="card-title">菜单列表</span>
            <el-button-group>
              <el-button type="success" plain size="mini" v-if="menuManager_btn_add" icon="plus" @click="handlerAdd">
                添加
              </el-button>
              <el-button type="primary" plain size="mini" v-if="menuManager_btn_edit" icon="edit" @click="handlerEdit">
                编辑
              </el-button>
              <el-button type="danger" plain size="mini" v-if="menuManager_btn_del" icon="delete" @click="handleDelete"
                         disabled>
                删除
              </el-button>
            </el-button-group>
          </div>
          <el-tree
            :data="firstData"
            :props="props"
            :load="fetchNodeData"
            accordion
            lazy
            @node-click="handleNodeClick">
          </el-tree>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="box-card">
          <div slot="header">
            <span class="card-title">菜单表单</span>
            <el-switch
              v-model="is_second"
              active-text="子菜单"
              inactive-text="父菜单"
              @change="resetForm">
            </el-switch>
          </div>
          <el-form label-width="80px" :model="menuform" ref="menuform">
            <el-form-item v-if="is_second" label="父级菜单" prop="parent">
              <el-select v-model="menuform.parent" placeholder="请选择父级菜单">
                <el-option v-for="item in firstData" :key="item.id" :value="item.title"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="菜单标题" prop="title">
              <el-input v-model="menuform.title" :disabled="formEdit" placeholder="请输入title"></el-input>
            </el-form-item>
            <el-form-item label="菜单编码" prop="name">
              <el-input v-model="menuform.name" :disabled="formEdit" placeholder="请输入name"></el-input>
            </el-form-item>
            <el-form-item label="url路径" prop="path">
              <el-input v-model="menuform.path" :disabled="formEdit" placeholder="请输入path"></el-input>
            </el-form-item>
            <el-form-item label="前端组件" prop="component">
              <el-input v-model="menuform.component" :disabled="formEdit" placeholder="请输入component"></el-input>
            </el-form-item>
            <el-form-item v-if="!is_second" label="图标" prop="icon">
              <el-input v-model="menuform.icon" :disabled="formEdit" placeholder="请输入icon"></el-input>
            </el-form-item>
            <el-form-item v-if="!is_second" label="redirect" prop="redirect">
              <el-input v-model="menuform.redirect" :disabled="formEdit" placeholder="请输入redirect"></el-input>
            </el-form-item>
            <el-form-item label="是否隐藏" prop="hidden">
              <el-switch v-model="menuform.hidden" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
            </el-form-item>
            <el-form-item v-if="formStatus == 'update'&&!is_second">
              <el-button type="primary" @click="putFirstFormSubmit(menuform.id)">更新</el-button>
              <el-button @click="onCancel">取消</el-button>
            </el-form-item>
            <el-form-item v-if="formStatus == 'update'&&is_second">
              <el-button type="primary" @click="putSecondFormSubmit(menuform.id)">更新</el-button>
              <el-button @click="onCancel">取消</el-button>
            </el-form-item>
            <el-form-item v-if="formStatus == 'create'&&!is_second">
              <el-button type="primary" @click="postFirstFormSubmit">保存</el-button>
              <el-button @click="onCancel">取消</el-button>
            </el-form-item>
            <el-form-item v-if="formStatus == 'create'&&is_second">
              <el-button type="primary" @click="postSecondFormSubmit">保存</el-button>
              <el-button @click="onCancel">取消</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card v-if="is_second" class="box-card">
          <div slot="header">
            <span class="card-title">资源按钮列表</span>
          </div>
          <div class="head-lavel">
            <div class="table-button">
              <el-button type="primary" plain size="mini" icon="el-icon-plus" @click="add_element=true">新建</el-button>
            </div>
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
              <el-table-column label="操作">
                <template slot-scope="scope">
                  <el-button type="success" plain size="mini" icon="el-icon-edit">修改</el-button>
                  <el-button type="danger" plain size="mini" icon="el-icon-close">删除</el-button>
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

    <el-dialog :visible.sync="add_element">
      <el-form :model="elementform" ref="elementform" label-width="100px">
        <el-form-item label="二级菜单" prop="parent">
          <el-select v-model="elementform.parent" placeholder="请选择二级菜单">
            <el-option v-for="item in secondData" :key="item.name" :value="item.title"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="菜单元素" prop="name">
          <el-input v-model="elementform.name"></el-input>
        </el-form-item>
        <el-form-item label="元素code" prop="code">
          <el-input v-model="elementform.code"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="postElementFormSubmit('elementform')">立即创建</el-button>
          <el-button @click="resetElementForm('elementform')">重置</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import {
  getFirstmenus,
  getSecondmenus,
  getMenumetas,
  postFirstmenus,
  postSecondmenus,
  postMenumetas,
  putFirstmenus,
  putSecondmenus,
  putMenumetas
} from '@/api/menu'
import { mapGetters } from 'vuex'
import { LIMIT } from '@/config'

export default {
  components: {},
  data() {
    return {
      firstData: [],
      secondData: [],
      props: {
        label: 'title',
        children: ''
      },
      formEdit: true,
      formAdd: true,
      formStatus: '',
      showElement: false,
      menuManager_btn_add: true,
      menuManager_btn_edit: true,
      menuManager_btn_del: true,
      menuform: {
        parent: undefined,
        title: undefined,
        name: undefined,
        path: undefined,
        component: undefined,
        icon: undefined,
        redirect: undefined,
        hidden: undefined
      },
      is_second: true,
      tabletotal: 0,
      searchdata: '',
      currentPage: 1,
      limit: LIMIT,
      offset: '',
      pagesize: [10, 25, 50, 100],
      elementData: [],
      add_element: false,
      elementform: {
        parent: '',
        name: '',
        code: ''
      }
    }
  },
  computed: {
    ...mapGetters([
      'elements'
    ])
  },
  created() {
    this.fetchFirstData()
    this.fetchSecondData()
    this.fetchElementData()
    //    this.menuManager_btn_add = this.elements['menuManager:btn_add']
    //    this.menuManager_btn_del = this.elements['menuManager:btn_del']
    //    this.menuManager_btn_edit = this.elements['menuManager:btn_edit']
  },
  methods: {
    fetchFirstData() {
      getFirstmenus().then(response => {
        this.firstData = response.data.results
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
        const data = response.data.results
        setTimeout(() => {
          resolve(data)
        }, 500)
      })
    },
    fetchSecondData() {
      const parmas = {
        parent__title: undefined
      }
      getSecondmenus(parmas).then(response => {
        this.secondData = response.data.results
      })
    },
    fetchElementData() {
      const parmas = {
        parent__title: undefined
      }
      getMenumetas(parmas).then(response => {
        this.elementData = response.data.results
      })
    },
    handleNodeClick(data, res) {
      this.is_second = res.isLeaf
      this.formEdit = true
      this.menuform = data
    },
    handlerEdit() {
      this.formEdit = false
      this.formStatus = 'update'
    },
    handlerAdd() {
      this.resetForm()
      this.formEdit = false
      this.formStatus = 'create'
    },
    handleDelete() {
      this.resetForm()
    },
    handleClick(tab, event) {
      console.log(tab, event)
    },
    onCancel() {
      this.formEdit = true
      this.formStatus = ''
    },
    resetForm() {
      this.menuform = {
        parent: undefined,
        title: undefined,
        name: undefined,
        path: undefined,
        component: undefined,
        icon: undefined,
        redirect: undefined,
        hidden: undefined
      }
    },
    searchClick() {
      this.fetchElementData()
    },
    handleSizeChange(val) {
      this.limit = val
      this.fetchElementData()
    },
    handleCurrentChange(val) {
      this.offset = val - 1
      this.fetchElementData()
    },
    postFirstFormSubmit() {
      postFirstmenus(this.menuform).then(response => {
        this.$message({
          message: '恭喜你，添加成功',
          type: 'success'
        })
        this.fetchFirstData()
      }).catch(error => {
        this.$message.error('添加失败')
        console.log(error)
      })
    },
    putFirstFormSubmit(id) {
      putFirstmenus(id, this.menuform).then(response => {
        this.$message({
          message: '恭喜你，更新成功',
          type: 'success'
        })
        this.fetchFirstData()
      }).catch(error => {
        this.$message.error('更新失败')
        console.log(error)
      })
    },
    postSecondFormSubmit() {
      postSecondmenus(this.menuform).then(response => {
        this.$message({
          message: '恭喜你，添加成功',
          type: 'success'
        })
        this.fetchFirstData()
        this.fetchSecondData()
      }).catch(error => {
        this.$message.error('添加失败')
        console.log(error)
      })
    },
    putSecondFormSubmit(id) {
      putSecondmenus(id, this.menuform).then(response => {
        this.$message({
          message: '恭喜你，更新成功',
          type: 'success'
        })
        this.fetchFirstData()
        this.fetchSecondData()
      }).catch(error => {
        this.$message.error('更新失败')
        console.log(error)
      })
    },
    postElementFormSubmit() {
      postMenumetas(this.elementform).then(response => {
        this.$message({
          message: '恭喜你，添加成功',
          type: 'success'
        })
        this.add_element = false
        this.fetchFirstData()
        this.fetchElementData()
      }).catch(error => {
        this.$message.error('添加失败')
        console.log(error)
      })
    },
    putElementFormSubmit(id) {
      putMenumetas(id, this.elementform).then(response => {
        this.$message({
          message: '恭喜你，更新成功',
          type: 'success'
        })
        this.fetchFirstData()
        this.fetchElementData()
      }).catch(error => {
        this.$message.error('更新失败')
        console.log(error)
      })
    },
    resetElementForm(formName) {
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

  .table-button {
    float: left;
  }

  .table-search {
    float: right;
  }

  .table-pagination {
    padding: 10px 0;
    float: right;
  }
</style>
