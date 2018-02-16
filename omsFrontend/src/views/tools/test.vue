<template>
  <div>
    <el-popover
      ref="statuspopover"
      placement="top"
      width="160"
      v-model="changestatus">
      <p>这是一段内容这是一段内容确定删除吗？</p>
      <div style="text-align: right; margin: 0">
        <el-button size="mini" type="text" @click="changestatus = false">取消</el-button>
        <el-button type="primary" size="mini" @click="changestatus = false">确定</el-button>
      </div>
    </el-popover>
    <el-button v-popover:statuspopover>删除</el-button>
  </div>
</template>

<script>
export default {
  components: {},
  data() {
    return {
      changestatus: false
    }
  },
  created() {
  },

  methods: {}
}
</script>

<style lang="scss">
</style>
