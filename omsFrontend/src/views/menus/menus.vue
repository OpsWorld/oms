<template>
  <div class="components-container" style='height:100vh'>
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card>
          <div class="filter-container">
            <el-button-group>
              <el-button type="success" plain size="mini" v-if="menuManager_btn_add" icon="plus" @click="handlerAdd">
                添加
              </el-button>
              <el-button type="primary" plain size="mini" v-if="menuManager_btn_edit" icon="edit" @click="handlerEdit">
                编辑
              </el-button>
              <el-button type="danger" plain size="mini" v-if="menuManager_btn_del" icon="delete" @click="handleDelete">
                删除
              </el-button>
            </el-button-group>
          </div>
        </el-card>
        <el-card>
          <el-tree
            :data="firstData"
            :props="props"
            :load="fetchSecondData"
            :accordion="true"
            lazy
            @check-change="handleCheckChange">
          </el-tree>
        </el-card>
      </el-col>
      <el-col :span="16">
        <el-card class="box-card">
          <el-tabs v-model="tabactive" type="card" @tab-click="handleClick">
            <el-tab-pane label="一级菜单" name="first">
              <el-form :label-position="labelPosition" label-width="80px" :model="firstform" ref="firstform">
                <el-form-item label="菜单编码" prop="title">
                  <el-input v-model="firstform.title" :disabled="formEdit" placeholder="请输入路径编码"></el-input>
                </el-form-item>
                <el-form-item label="菜单标题" prop="name">
                  <el-input v-model="firstform.name" :disabled="formEdit" placeholder="请输入标题"></el-input>
                </el-form-item>
                <el-form-item label="url路径" prop="path">
                  <el-input v-model="firstform.path" :disabled="formEdit" placeholder="请选择父级菜单" readonly></el-input>
                </el-form-item>
                <el-form-item label="前端组件" prop="component">
                  <el-input v-model="firstform.component" :disabled="formEdit" placeholder="请输入描述"></el-input>
                </el-form-item>
                <el-form-item label="图标" prop="icon">
                  <el-input v-model="firstform.icon" :disabled="formEdit" placeholder="请输入图标"></el-input>
                </el-form-item>
                <el-form-item label="redirect" prop="redirect">
                  <el-input v-model="firstform.redirect" :disabled="formEdit" placeholder="请输入redirect"></el-input>
                </el-form-item>
                <el-form-item label="是否隐藏" prop="hidden">
                  <el-switch v-model="firstform.hidden" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
                </el-form-item>
                <el-form-item v-if="formStatus == 'update'">
                  <el-button type="primary" @click="update">更新</el-button>
                  <el-button @click="onCancel">取消</el-button>
                </el-form-item>
                <el-form-item v-if="formStatus == 'create'">
                  <el-button type="primary" @click="create">保存</el-button>
                  <el-button @click="onCancel">取消</el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>
            <el-tab-pane label="二级菜单" name="second">
              <el-form :label-position="labelPosition" label-width="80px" :model="secondform" ref="secondform">
                <el-form-item label="父级菜单" prop="parent">
                  <el-input v-model="secondform.parent" :disabled="formEdit" placeholder="请输选择父级菜单"></el-input>
                </el-form-item>
                <el-form-item label="菜单编码" prop="title">
                  <el-input v-model="secondform.title" :disabled="formEdit" placeholder="请输入路径编码"></el-input>
                </el-form-item>
                <el-form-item label="菜单标题" prop="name">
                  <el-input v-model="secondform.name" :disabled="formEdit" placeholder="请输入标题"></el-input>
                </el-form-item>
                <el-form-item label="url路径" prop="path">
                  <el-input v-model="secondform.path" :disabled="formEdit" placeholder="请选择父级菜单" readonly></el-input>
                </el-form-item>
                <el-form-item label="前端组件" prop="component">
                  <el-input v-model="secondform.component" :disabled="formEdit" placeholder="请输入描述"></el-input>
                </el-form-item>
                <el-form-item label="是否隐藏" prop="hidden">
                  <el-switch v-model="secondform.hidden" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
                </el-form-item>
                <el-form-item v-if="formStatus == 'update'">
                  <el-button type="primary" @click="update">更新</el-button>
                  <el-button @click="onCancel">取消</el-button>
                </el-form-item>
                <el-form-item v-if="formStatus == 'create'">
                  <el-button type="primary" @click="create">保存</el-button>
                  <el-button @click="onCancel">取消</el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>
          </el-tabs>
        </el-card>
        <el-card v-if="tabactive==='second'" class="box-card">
          <span>按钮或资源</span>
          <!--<menu-element :menuId='currentId' ref="menuElement"></menu-element>-->
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { getFirstmenus, getSecondmenus } from '@/api/menu'
import { mapGetters } from 'vuex'
// import menuElement from './element.vue'

export default {
//  components: {
//    menuElement
//  },
  data() {
    return {
      firstData: [],
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
      currentId: -1,
      labelPosition: 'right',
      firstform: {
        title: undefined,
        name: undefined,
        path: undefined,
        component: undefined,
        icon: undefined,
        redirect: undefined,
        hidden: undefined
      },
      secondform: {
        parent: undefined,
        title: undefined,
        name: undefined,
        path: undefined,
        component: undefined,
        hidden: undefined
      },
      tabactive: 'first'
    }
  },
  computed: {
    ...mapGetters([
      'elements'
    ])
  },
  created() {
    this.fetchFirstData()
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
    handleCheckChange(data, checked, indeterminate) {
      console.log(data, checked, indeterminate)
    },
    handleNodeClick(data) {
      console.log(data)
    },
    handlerEdit() {
      if (this.firstform.id) {
        this.formEdit = false
        this.formStatus = 'update'
      }
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
