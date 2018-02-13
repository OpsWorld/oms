<template>
  <div>
    <div class="host-select">
      <el-transfer
        v-model="value"
        filterable
        :titles="['未选择', '已选择']"
        :button-texts="['向左走', '向右走']"
        @change="handleChange"
        :data="allhost">
      </el-transfer>
    </div>
  </div>
</template>

<script>
import { getHost } from '@/api/host'
export default {
  props: ['selecthost'],
  data() {
    return {
      allhost: [],
      value: this.selecthost,
      changedata: false
    }
  },

  created() {
    this.hostData()
  },

  methods: {
    hostData() {
      this.allhost = []
      this.value = this.selecthost
      const parms = {
        status: 'used'
      }
      getHost(parms).then(response => {
        this.allhost = []
        const results = response.data
        for (var i = 0, len = results.length; i < len; i++) {
          this.allhost.push({
            key: results[i].hostname
          })
        }
      })
    },
    handleChange(value, direction, movedKeys) {
      this.$emit('gethosts', value)
    }
  },
  watch: {
    // 监控rowdata值的变化，有变化立即刷新数据
    selecthost() {
      this.hostData()
    }
  }
}
</script>

<style>
  .transfer-footer {
    margin-left: 20px;
    padding: 6px 5px;
  }
</style>
