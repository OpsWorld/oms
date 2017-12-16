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
              <mallki className='mallki-text' text='OMS运维系统'></mallki>
            </div>
          </div>

          <div style="position:relative;">

            <el-card>
              <div slot="header" class="clearfix">
                <span>后端技术</span>
              </div>
              <div class='progress-item'>
                <span>Django</span>
                <el-progress :percentage="33"></el-progress>
              </div>
              <div class='progress-item'>
                <span>Django Rest Framework</span>
                <el-progress :percentage="66"></el-progress>
              </div>
              <div class='progress-item'>
                <span>Other</span>
                <el-progress :percentage="1"></el-progress>
              </div>
            </el-card>
            <el-card>
              <div slot="header" class="clearfix">
                <span>前端技术</span>
              </div>
              <div class='progress-item'>
                <span>Vue</span>
                <el-progress :percentage="70"></el-progress>
              </div>
              <div class='progress-item'>
                <span>JavaScript</span>
                <el-progress :percentage="18"></el-progress>
              </div>
              <div class='progress-item'>
                <span>Css</span>
                <el-progress :percentage="12"></el-progress>
              </div>
              <div class='progress-item'>
                <span>ESLint</span>
                <el-progress :percentage="100" status="success"></el-progress>
              </div>
            </el-card>

          </div>
        </el-card>
      </el-col>
      <el-col :span="16">
        <el-card class="welcome">
          欢迎你，{{username}}
        </el-card>
        <el-row :gutter="20">
          <el-col :span="12">
            <div class="chart-wrapper">
              <raddar-chart></raddar-chart>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="chart-wrapper">
              <pie-chart></pie-chart>
            </div>
          </el-col>
        </el-row>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import PanThumb from '@/components/PanThumb'
import Mallki from '@/components/TextHoverEffect/Mallki'
import ElRow from 'element-ui/packages/row/src/row'
import ElCard from '../../../../../omsFrontend/node_modules/element-ui/packages/card/src/main'
import RaddarChart from './components/RaddarChart'
import PieChart from './components/PieChart'
import BarChart from './components/BarChart'

export default {
  components: {
    ElCard,
    ElRow, PanThumb, Mallki,
    RaddarChart, PieChart, BarChart
  },

  data() {
    return {
      'img': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
      statisticsData: {
        article_count: 1024,
        pageviews_count: 1024
      }
    }
  },
  computed: {
    ...mapGetters([
      'username',
      'groups'
    ])
  },
  filters: {
    statusFilter(status) {
      const statusMap = {
        success: 'success',
        pending: 'danger'
      }
      return statusMap[status]
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
  .box-card-component {
    height: 800px;
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
    .welcome {
      height: 500px;
    }
  }
</style>
