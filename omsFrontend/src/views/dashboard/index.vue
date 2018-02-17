<template>
  <div class="components-container" style='height:100vh'>
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="box-card-component" style="margin-left:8px;">
          <div slot="header" class="box-card-header">
            <img src='https://wpimg.wallstcn.com/e7d23d71-cf19-4b90-a1cc-f56af8c0903d.png' width="340">
            <div class="title">
              <pan-thumb class="panThumb" :image="img">
                <span style="color: #fa43ff">TB</span>
              </pan-thumb>
              <mallki className='mallki-text' text='OA协同办公系统'></mallki>
            </div>
          </div>

          <div>

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
                <el-progress :percentage="100"></el-progress>
              </div>
              <div class='progress-item'>
                <span>文档系统</span>
                <el-progress :percentage="100"></el-progress>
              </div>
              <div class='progress-item'>
                <span>发布系统</span>
                <el-progress :percentage="100"></el-progress>
              </div>
              <div class='progress-item'>
                <span>cmdb</span>
                <el-progress :percentage="100"></el-progress>
              </div>
              <div class='progress-item'>
                <span>研发管理</span>
                <el-progress :percentage="80"></el-progress>
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
            </el-card>
          </div>
        </el-card>
      </el-col>
      <el-col :span="18">
        <el-card>
          <div>
            <p style="font-size: 24px">欢迎你，{{username}}!</p>
            <p style="font-size: 18px">&#160;&#160;&#160;&#160;&#160;&#160;本系统目的是为了简化和改进目前日常工作中的一些重复和琐碎的事情，希望此系统能给大家带来方便和快捷！本系统还有很多功能和地方需要完善，希望大家多提提意见。</p>
          </div>
        </el-card>
        <el-card class="duty">
          <el-tabs v-model="activeName">
            <el-tab-pane label="运维值班表" name="opsduty">
              <calendar :addbtn="role==='super'"></calendar>
            </el-tab-pane>
            <el-tab-pane label="技术值班表" name="techduty">
              <h3 class="title">基础架构</h3>
              <el-table :data="opsdutyData" border style="width: 100%">
                <el-table-column prop="duty" label="职责" :width="150"></el-table-column>
                <el-table-column prop="master" label="主负责人" :width="80"></el-table-column>
                <el-table-column prop="m_tel" label="电话" :width="120"></el-table-column>
                <el-table-column prop="slave" label="备负责人" :width="80"></el-table-column>
                <el-table-column prop="s_tel" label="电话" :width="120"></el-table-column>
                <el-table-column prop="desc" label="说明"></el-table-column>
              </el-table>
              <h3 class="title">应用系统</h3>
              <el-table :data="techdutyData" border style="width: 100%">
                <el-table-column prop="duty" label="职责" :width="150"></el-table-column>
                <el-table-column prop="master" label="主负责人" :width="80"></el-table-column>
                <el-table-column prop="m_tel" label="电话" :width="120"></el-table-column>
                <el-table-column prop="slave" label="备负责人" :width="80"></el-table-column>
                <el-table-column prop="s_tel" label="电话" :width="120"></el-table-column>
                <el-table-column prop="desc" label="说明"></el-table-column>
              </el-table>
              <div>
                <p class="tips"> 1. 以上仅限在0点至8点时间内，影响范围广且急迫性高的问题处理</p>
                <p class="tips"> 2. 其它非紧急且影响小的问题直接上工单系统提交问题，待技术白天上班后处理</p>
                <p class="tips"> 3. 出现紧急重大问题时，请优先电话联系上表中对应的主负责人，当主负责人联系不上时，可以联系备份负责人</p>
              </div>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import PanThumb from '@/components/PanThumb'
import Calendar from './components/calendar.vue'
import Mallki from '@/components/TextHoverEffect/Mallki'

export default {
  components: {
    PanThumb, Calendar, Mallki
  },

  data() {
    return {
      'img': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
      activeName: 'opsduty',
      opsdutyData: [
        {
          duty: '办公室网络,电话系统，sharepoint',
          master: 'Jimmy',
          m_tel: '09055126361',
          slave: 'Larry',
          s_tel: '09055594786',
          desc: '比如：财务或客服办公室网络断网，电话无法打入打出，sharepoint无法登陆等'
        },
        {
          duty: '网站安全防御，线上系统',
          master: 'Larry',
          m_tel: '09055594786',
          slave: 'Jimmy',
          s_tel: '09055126361',
          desc: '比如：PC和H5网站打不开，VPN使用后仍然无法打开，户内转账大批量掉单，第三方游戏平台API网络连接超时等;比如：第三方支付出现大量掉单，已联系过第三方业务确定不是他们的问题，且没有其它可用的第三方通道了'
        }],
      techdutyData: [
        {
          duty: '自动提款软件、流水采集程序',
          master: 'Jason',
          m_tel: '09566618209',
          slave: 'Omar',
          s_tel: '09164340595',
          desc: '比如：自动提款软件有重大bug，或流水采集长时间延迟'
        },
        {
          duty: '支付宝银行、绿通采集软件',
          master: 'Ken',
          m_tel: '09166834689',
          slave: 'Omar',
          s_tel: '09164340595',
          desc: '比如：采集器软件有重大bug，或运行时出现错误提示，如果不马上处理会严重影响工作时'
        },
        {
          duty: '前台程序',
          master: 'Omar',
          m_tel: '09164340595',
          slave: 'Ken',
          s_tel: '09166834689',
          desc: '比如：前台网站程序出现重大业务逻辑bug，如果不马上处理会导致大量玩家流失或公司有重大损失'
        },
        {
          duty: '后台程序',
          master: 'Omar',
          m_tel: '09164340595',
          slave: 'Jason',
          s_tel: '09566618209',
          desc: '比如：后台网站程序出现重大业务逻辑bug且严重影响工作时'
        },
        {
          duty: 'H5移动端',
          master: 'Omar',
          m_tel: '09164340595',
          slave: 'Ken',
          s_tel: '09166834689',
          desc: '比如：H5网站程序出现重大业务逻辑bug，如果不马上处理会导致大量玩家流失或公司有重大损失'
        }
      ]
    }
  },
  computed: {
    ...mapGetters([
      'username',
      'role'
    ])
  },
  methods: {}
}
</script>

<style lang="scss" scoped>
  .duty {
    min-height: 900px;
    .title {
      color: #d36cff;
    }
  }

  .box-card-component {
    height: 100%;
    .box-card-header {
      position: relative;
      height: 220px;
      img {
        width: 100%;
        height: 100%;
        transition: all 0.3s linear;
        &:hover {
          transform: scale(1.12, 1.16); // 控制图片放大长宽
          filter: contrast(150%);
        }
      }
      .title {
        position: relative;
        .mallki-text {
          position: absolute;
          top: 0;
          right: 0;
          font-size: 26px;
          font-weight: bold;
        }
        .panThumb {
          z-index: 100;
          height: 70px !important;
          width: 70px !important;
          position: absolute !important;
          top: -20px;
          left: 0;
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
  }
</style>
