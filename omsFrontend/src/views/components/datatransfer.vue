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
      </el-transfer>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    selectdata: Array,
    alldata: Array
  },
  data() {
    return {
      value: this.selecthost,
      changedata: false
    }
  },

  created() {
  },

  methods: {

    handleChange(value, direction, movedKeys) {
      this.$emit('getdatas', value)
    }
  }
}
</script>

<style>
</style>
