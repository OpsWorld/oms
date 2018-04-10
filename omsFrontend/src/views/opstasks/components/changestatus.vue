<template>
  <el-form>
    <el-form-item :model="statusdata" label="当前状态">
      <span>{{Status[statusdata.status]}}</span>
    </el-form-item>
    <el-form-item :model="statusdata" label="状态修改">
      <el-select v-model="statusdata.status" placeholder="请选择状态">
        <el-option v-for="(item,index) in Status" :key="item.id" :label="item" :value="index"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item>
      <el-button @click="submitForm" type="primary" icon="el-icon-check">提交</el-button>
    </el-form-item>
  </el-form>
</template>
<script>
export default {
  components: {},
  props: ['Status', 'statusdata'],
  data() {
    return {}
  },
  created() {
  },
  methods: {
    submitForm(formName) {
      this.$emit('formdata', this.statusdata)
    }
  }
}
</script>
