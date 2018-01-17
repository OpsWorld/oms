<template>
  <div class="components-container" style='height:100vh'>
    <el-row :gutter="20">
      <el-col :span="16">
        <el-card>
          <div slot="header">
            salt-keys状态统计
          </div>
          <panel-group></panel-group>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import PanelGroup from './components/PanelGroup'
export default {
  components: {
    PanelGroup
  },

  data() {
    return {
    }
  },
  methods: {
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
  .box-card-component {
    height: 100%;
    .box-card-card {
      margin-top: 50px;
    }
  }
</style>
