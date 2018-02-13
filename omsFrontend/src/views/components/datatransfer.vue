<template>
  <div>
    <div class="host-select">
      <el-transfer
        v-model="value"
        filterable
        :titles="['未选择', '已选择']"
        :button-texts="['向左走', '向右走']"
        :format="{noChecked: '${total}',hasChecked: '${checked}/${total}'}"
        @change="handleChange"
        :data="alldata">
        <el-button type="info" class="transfer-footer" slot="left-footer" size="mini" @click="getData">重置</el-button>
      </el-transfer>
    </div>
  </div>
</template>

<script>
export default {
  props: ['selectdata', 'alldata'],
  data() {
    return {
      value: this.selectdata,
      changedata: false
    }
  },

  created() {
    console.log(this.selectdata)
    this.getData()
  },

  methods: {
    getData() {
      this.value = this.selectdata
    },
    handleChange(value, direction, movedKeys) {
      this.$emit('getDatas', value)
    },
    watch: {
      // 监控rowdata值的变化，有变化立即刷新数据
      selectdata() {
        this.getData()
      }
    }
  }
}
</script>

<style>
  .transfer-footer {
    float: right;
    margin-top: 5px;
  }
</style>
