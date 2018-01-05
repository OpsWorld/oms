<template>
  <div class="components-container" style='height:100vh'>
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card class="box-card-component" style="margin-left:8px;">
          <div slot="header" class="box-card-header">
            <img src='https://wpimg.wallstcn.com/e7d23d71-cf19-4b90-a1cc-f56af8c0903d.png'>
            <div class="title">
              <pan-thumb class="panThumb" :image="img">
                <span style="color: #f10df5;font-weight: 600">TB</span>
              </pan-thumb>
              <mallki className='mallki-text' text='OMS运维管理系统'></mallki>
            </div>
          </div>

          <div style="position:relative;">

            <el-card class="box-card-card">
              <div slot="header" class="clearfix">
                <span>已开发功能</span>
              </div>
              <div class='progress-item'>
                <span>工单系统</span>
                <el-progress :percentage="100"></el-progress>
              </div>
              <div class='progress-item'>
                <span>第三支付对接</span>
                <el-progress :percentage="99"></el-progress>
              </div>
              <div class='progress-item'>
                <span>文档系统</span>
                <el-progress :percentage="88"></el-progress>
              </div>
            </el-card>
            <el-card class="box-card-card">
              <div slot="header" class="clearfix">
                <span>待开发功能</span>
              </div>
              <div class='progress-item'>
                <span>工作流系统</span>
                <el-progress :percentage="0"></el-progress>
              </div>
              <div class='progress-item'>
                <span>cmdb</span>
                <el-progress :percentage="0"></el-progress>
              </div>
              <div class='progress-item'>
                <span>发布系统</span>
                <el-progress :percentage="0"></el-progress>
              </div>

            </el-card>

          </div>
        </el-card>
      </el-col>
      <el-col :span="16">
        <el-card>
          <div>
            <p style="font-size: 36px">欢迎你，{{username}}!</p>
            <p style="font-size: 20px">&#160;&#160;&#160;&#160;&#160;&#160;本系统目的是为了简化和改进目前日常工作中的一些重复和琐碎的事情，希望此系统能给大家带来方便和快捷！本系统还有很多功能和地方需要完善，希望大家多提提意见;</p>
            <p style="font-size: 20px">
              &#160;&#160;&#160;&#160;&#160;&#160;下面会将是一些系统数据的展示，目前是测试数据;分别点击T、B、O、P，图片会发生变化</p>
          </div>
        </el-card>
        <panel-group @handleSetLineChartData="handleSetLineChartData"></panel-group>

        <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
          <line-chart :chart-data="lineChartData"></line-chart>
        </el-row>
        <!--<el-row :gutter="20">-->
        <!--<el-col :span="12">-->
        <!--<div class="chart-wrapper">-->
        <!--<raddar-chart></raddar-chart>-->
        <!--</div>-->
        <!--</el-col>-->
        <!--<el-col :span="12">-->
        <!--<div class="chart-wrapper">-->
        <!--<pie-chart></pie-chart>-->
        <!--</div>-->
        <!--</el-col>-->
        <!--</el-row>-->
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import PanThumb from '@/components/PanThumb'
import Mallki from '@/components/TextHoverEffect/Mallki'
import RaddarChart from './components/RaddarChart'
import PieChart from './components/PieChart'
import BarChart from './components/BarChart'
import PanelGroup from './components/PanelGroup'
import LineChart from './components/LineChart'

const lineChartData = {
  newVisitis: {
    expectedData: [90, 130, 90, 130, 90, 130, 90],
    actualData: [60, 100, 60, 100, 60, 100, 60]
  },
  messages: {
    expectedData: [90, 150, 90, 60, 90, 150, 90],
    actualData: [90, 60, 90, 150, 90, 60, 90]
  },
  purchases: {
    expectedData: [0, 30, 60, 90, 120, 150, 180],
    actualData: [180, 150, 120, 90, 60, 30, 0]
  },
  shoppings: {
    expectedData: [180, 130, 80, 30, 80, 130, 180],
    actualData: [0, 50, 100, 200, 100, 50, 0]
  }
}

export default {
  components: {
    PanThumb, Mallki, RaddarChart, PieChart, BarChart, PanelGroup, LineChart
  },

  data() {
    return {
      'img': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
      statisticsData: {
        article_count: 1024,
        pageviews_count: 1024
      },
      lineChartData: lineChartData.newVisitis
    }
  },
  computed: {
    ...mapGetters([
      'username',
      'groups'
    ])
  },
  methods: {
    handleSetLineChartData(type) {
      this.lineChartData = lineChartData[type]
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
  .box-card-component {
    height: 100%;
    .box-card-header {
      position: relative;
      height: 220px;
      img {
        width: 100%;
        height: 100%;
        transition: all 0.2s linear;
        &:hover {
          transform: scale(1.1, 1.1);
          filter: contrast(130%);
        }
      }
      .title {
        position: relative;
        .mallki-text {
          position: absolute;
          top: 0px;
          right: 0px;
          font-size: 30px;
          font-weight: bold;
        }
        .panThumb {
          z-index: 100;
          height: 70px !important;
          width: 70px !important;
          position: absolute !important;
          top: -45px;
          left: 0px;
          border: 5px solid #ffffff;
          background-color: #fff;
          margin: auto;
          box-shadow: none !important;
          /deep/ .pan-info {
            box-shadow: none !important;
          }
        }
      }
      .progress-item {
        margin-bottom: 10px;
        font-size: 14px;
      }
      @media only screen and (max-width: 1510px) {
        .mallki-text {
          display: none;
        }
      }
    }
    .box-card-card {
      margin-top: 50px;
      .clearfix {
        color: #3a8ee6;
        font-size: 24px;
        font-weight: 600;
      }
    }
    .welcome {
      font-size: 36px;
    }
  }
</style>
