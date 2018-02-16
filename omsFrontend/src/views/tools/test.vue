<template>
  <div>
    <el-popover
      ref="popover5"
      placement="top"
      width="160"
      v-model="visible2">
      <p>这是一段内容这是一段内容确定删除吗？</p>
      <div style="text-align: right; margin: 0">
        <el-button size="mini" type="text" @click="visible2 = false">取消</el-button>
        <el-button type="primary" size="mini" @click="visible2 = false">确定</el-button>
      </div>
    </el-popover>
    <el-button v-popover:popover5>删除</el-button>
  </div>
</template>

<script>
export default {
  components: {},
  data() {
    return {
      visible2: false
    }
  },
  created() {
  },

  methods: {}
}
</script>

<style lang="scss">
</style>
