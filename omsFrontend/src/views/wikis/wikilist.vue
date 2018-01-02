<template>
  <div class="components-container" style='height:100vh'>
    <el-card class="wiki">
      <el-row :gutter="20">
        <el-col :span="4">
          <div style="margin: 15px">文档知识库</div>
        </el-col>
        <el-col :span="20">
          <el-input placeholder="search . . ." v-model="search" class="input-with-select">
            <el-button slot="append" icon="el-icon-search"></el-button>
          </el-input>
        </el-col>
      </el-row>
      <hr class="heng"/>
    </el-card>
  </div>
</template>
<script>
export default {
  data() {
    return {
      search: ''
    }
  },

  methods: {}
}
</script>

<style lang='scss'>
  .wiki {
    margin: 50px;
  }
</style>
