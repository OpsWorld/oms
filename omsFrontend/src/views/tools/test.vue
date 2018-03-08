<template>
  <div>
    <el-button type="primary" @click="add">默认按钮</el-button>
    <el-steps :space="100" :active="active" finish-status="success">
      <el-step v-for="(item, index) in steps" :key="index" :title="item.title"></el-step>
    </el-steps>
  </div>
</template>

<script>
export default {
  data: function() {
    return {
      steps: [
        { title: '1111' },
        { title: '2222' }
      ],
      active: 0
    }
  },
  methods: {
    add: function() {
      this.steps.push({
        title: '5555'
      })
    }
  }
}
</script>
