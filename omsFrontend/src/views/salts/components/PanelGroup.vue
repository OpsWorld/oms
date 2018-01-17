<template>
  <el-row class="panel-group" :gutter="40">
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class='card-panel' @click="handleSetLineChartData('newVisitis')">
        <div class="card-panel-icon-wrapper icon-people">
          <a class="wenzi">已接受</a>
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">accepted</div>
          <count-to class="card-panel-num" :startVal="0" :endVal="1024" :duration="3600"></count-to>
        </div>
      </div>
    </el-col>
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel" @click="handleSetLineChartData('messages')">
        <div class="card-panel-icon-wrapper icon-message">
          <a class="wenzi">已删除</a>
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">denied</div>
          <count-to class="card-panel-num" :startVal="1024" :endVal="2048" :duration="4000"></count-to>
        </div>
      </div>
    </el-col>
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel" @click="handleSetLineChartData('purchases')">
        <div class="card-panel-icon-wrapper icon-money">
          <a class="wenzi">未接受</a>
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">unaccept</div>
          <count-to class="card-panel-num" :startVal="2048" :endVal="4096" :duration="4000"></count-to>
        </div>
      </div>
    </el-col>
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel" @click="handleSetLineChartData('shoppings')">
        <div class="card-panel-icon-wrapper icon-shoppingCard">
          <a class="wenzi">已拒绝</a>
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">rejected</div>
          <count-to class="card-panel-num" :startVal="4096" :endVal="8192" :duration="4600"></count-to>
        </div>
      </div>
    </el-col>
  </el-row>
</template>

<script>
import CountTo from 'vue-count-to'

export default {
  components: {
    CountTo
  },
  methods: {
    handleSetLineChartData(type) {
      this.$emit('handleSetLineChartData', type)
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.panel-group {
  margin-top: 18px;
  .card-panel-col{
    margin-bottom: 32px;
  }
  .card-panel {
    height: 108px;
    cursor: pointer;
    font-size: 12px;
    position: relative;
    overflow: hidden;
    color: #666;
    background: #fff;
    box-shadow: 4px 4px 40px rgba(0, 0, 0, .05);
    border-color: rgba(0, 0, 0, .05);
    &:hover {
      .card-panel-icon-wrapper {
        color: #fff;
      }
      .icon-people {
         background: #40c9c6;
      }
      .icon-message {
        background: #f4516c;
      }
      .icon-money {
        background: #4b4b4b;
      }
      .icon-shoppingCard {
        background: #f4516c
      }
    }
    .icon-people {
      color: #40c9c6;
    }
    .icon-message {
      color: #f4516c;
    }
    .icon-money {
      color: #4b4b4b;
    }
    .icon-shoppingCard {
      color: #f4516c
    }
    .card-panel-icon-wrapper {
      float: left;
      margin: 14px 0 0 14px;
      padding: 16px;
      transition: all 0.5s ease-out;
      border-radius: 6px;
      border: solid 1px;
    }
    .wenzi {
      font-size: 24px;
    }
    .card-panel-description {
      float: right;
      font-weight: bold;
      margin: 26px;
      margin-left: 0px;
      .card-panel-text {
        line-height: 18px;
        color: rgba(0, 0, 0, 0.45);
        font-size: 16px;
        margin-bottom: 12px;
      }
      .card-panel-num {
        font-size: 20px;
      }
    }
  }
}
</style>
