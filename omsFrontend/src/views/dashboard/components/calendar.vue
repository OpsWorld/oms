<template>
  <div class="calendar"  @mouseleave="showcontent=false">
    <full-calendar :events="calenderData" first-day='1' locale="zh" @eventClick="eventClick" @changeMonth="changeMonth">
      <template slot="fc-header-left">
        <el-button v-if="addbtn" type="primary" plain size="mini" icon="el-icon-plus" @click="addEvent=true">增加事件
        </el-button>
      </template>
      <template slot="fc-body-card">
        <div id="clickcalendar" v-show="showcontent" class="calendarcontent" @mouseleave="showcontent=false">
          <a style="font-size: 16px">详细内容
            <el-tooltip v-if="addbtn" style="margin-left: 10px" effect="dark" content="删除本事件" placement="right">
              <el-button type="text" icon="el-icon-delete" @click="deleteSubmit"></el-button>
            </el-tooltip>
          </a>
          <hr class="heng"/>
          <div v-if="ruleForm.content">
            <p>开始时间：{{ruleForm.start}}</p>
            <p>结束时间：{{ruleForm.end}}</p>
            <p>内容：{{ruleForm.content}}</p>
          </div>
          <div v-else>暂无内容</div>
        </div>
      </template>
    </full-calendar>

    <el-dialog :visible.sync="addEvent">
      <el-form :model="ruleForm" ref="ruleForm" label-width="100px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="ruleForm.title"></el-input>
        </el-form-item>
        <el-form-item label="选择日期" firstDayOfWeek="1">
          <el-date-picker
            v-model="selectdate"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            @change="chooseDate"
            value-format="yyyy-MM-dd"
            :picker-options="{
              firstDayOfWeek: 1
            }">
          </el-date-picker>
        </el-form-item>
        <!--<el-form-item label="选择时间" firstDayOfWeek="1">-->
        <!--<el-time-select-->
        <!--placeholder="起始时间"-->
        <!--v-model="startTime"-->
        <!--:picker-options="{-->
        <!--start: '08:00',-->
        <!--step: '01:00',-->
        <!--end: '24:00',-->
        <!--}">-->
        <!--</el-time-select>-->
        <!--<el-time-select-->
        <!--placeholder="结束时间"-->
        <!--v-model="endTime"-->
        <!--:picker-options="{-->
        <!--start: '08:00',-->
        <!--step: '01:00',-->
        <!--end: '24:00',-->
        <!--minTime: startTime-->
        <!--}">-->
        <!--</el-time-select>-->
        <!--</el-form-item>-->
        <el-form-item label="内容" prop="content">
          <el-input v-model="ruleForm.content" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
        </el-form-item>
        <el-form-item label="显示颜色" prop="cssClass">
          <el-select v-model="ruleForm.cssClass" placeholder="请选择显示颜色">
            <el-option
              v-for="item in cssClasss"
              :key="item"
              :value="item">
            </el-option>
          </el-select>
          <!--<div :class="`${ruleForm.cssClass} showcolor`">cool</div>-->
          <i :class="`${ruleForm.cssClass} showcolor fa fa-github fa-3x `"></i>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="addSubmit('ruleForm')">立即创建</el-button>
          <el-button @click="resetForm('ruleForm')">重置</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import { getCalender, postCalender, deleteCalender } from 'api/tool'

export default {
  components: {},
  props: ['addbtn'],
  data() {
    return {
      addEvent: false,
      ruleForm: {
        id: '',
        title: '',
        start: '',
        end: '',
        content: '',
        cssClass: 'violet'
      },
      calenderData: [],
      selectdate: '',
      startTime: '',
      endTime: '',
      cssClasss: ['yellow', 'green', 'pink', 'violet', 'blue', 'red', 'tiffany'],
      listQuery: {
        start__gte: '',
        end__lte: ''
      },
      showcontent: false
    }
  },
  created() {
    this.fetchData()
  },

  methods: {
    fetchData() {
      getCalender(this.listQuery).then(response => {
        this.calenderData = response.data
      })
    },
    eventClick(event, jsEvent, pos) {
      this.showcontent = true
      this.ruleForm = event
      const obj = document.getElementById('clickcalendar')
      obj.style.left = pos.left + 'px'
      obj.style.top = pos.top + 'px'
    },
    changeMonth(start, end, current) {
      this.showcontent = false
      this.listQuery.start__gte = start
      this.listQuery.end__lte = end
      this.fetchData()
    },
    addSubmit() {
      this.showcontent = false
      postCalender(this.ruleForm).then(response => {
        this.$message({
          message: '添加成功',
          type: 'success'
        })
        this.addEvent = false
        this.fetchData()
      }).catch(error => {
        this.$message.error('添加失败')
        console.log(error)
      })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    chooseDate(res) {
      this.ruleForm.start = res[0]
      this.ruleForm.end = res[1]
    },
    deleteSubmit(formName) {
      deleteCalender(this.ruleForm.id).then(response => {
        this.$message({
          message: '删除成功',
          type: 'success'
        })
        this.fetchData()
      }).catch(error => {
        this.$message.error('删除失败')
        this.resetForm(formName)
        console.log(error)
      })
    }
  }
}
</script>

<style lang="scss">
  @import "src/styles/variables.scss";

  .calendar {
    min-height: 850px;
    .showcolor {
      position: absolute;
      color: #ffffff;
      width: 36px;
      height: 36px;
      line-height: 36px; // 文字垂直居中
      // overflow:hidden;  // 文字垂直居中
      // display: inline-block;
      // text-align:center;
      border-radius: 50%;
      margin-left: 20px;
    }

    .yellow {
      background-color: $yellow !important;
    }

    .green {
      background-color: $green !important;
    }

    .pink {
      background-color: $pink !important;
    }

    .violet {
      background-color: $violet !important;
    }

    .blue {
      background-color: $blue !important;
    }

    .red {
      background-color: $red !important;
    }

    .tiffany {
      background-color: $tiffany !important;
    }

    .calendarcontent {
      position: absolute;
      z-index: 1024;
      width: 250px;
      height: 200px;
      background-color: #ffffff;
      border-radius: 3px;
      box-shadow: 1px 1px 10px 5px #888888;
      padding: 0 5px;
    }
  }
</style>
