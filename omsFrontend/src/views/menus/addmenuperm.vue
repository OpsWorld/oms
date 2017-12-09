<template>
  <div>
    <el-form :model="addform" :rules="ruleaddfrom" ref="addform" label-width="100px">
      <el-form-item label="用户组" prop="group">
        <el-select v-model="addform.group" placeholder="请选择用户分组">
          <el-option v-for="item in groupdata" :key="item.name" :value="item.name"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="菜单列表" prop="menus">
        <el-tree
          :data="treedata"
          :props="menuprops"
          node-key="name"
          accordion
          ref="menutree"
          show-checkbox>
        </el-tree>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="addFormSubmit('addform')">立即创建</el-button>
        <el-button @click="resetForm('addform')">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>
<script>
export default {
  props: ['treedata', 'groupdata'],
  data() {
    return {
      addform: {
        group: '',
        menus: []
      },
      ruleaddfrom: {
        group: [
          { required: true, message: '请选择用户组', trigger: 'change' }
        ]
      },
      menuprops: {
        label: 'title',
        children: 'children'
      }
    }
  },
  methods: {
    addFormSubmit(formName) {
    },
    resetForm(formName) {
    }
  }
}
</script>
