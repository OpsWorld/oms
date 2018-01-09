<template>
  <div>
    <full-calendar :events="events" first-day='1' locale="zh" @eventClick="eventClick">
      <template slot="fc-header-left">
        <el-button type="primary" plain size="mini" icon="el-icon-plus" @click="addEvent=true">增加事件</el-button>
      </template>
      <template slot="fc-body-card">
        <el-button type="primary" plain size="mini" icon="el-icon-plus" @click="addEvent=true">增加事件</el-button>
      </template>
    </full-calendar>
    <el-dialog :visible.sync="addEvent">
      <el-form :model="ruleForm" ref="ruleForm" label-width="100px" class="demo-ruleForm">
        <el-form-item label="标题" prop="title">
          <el-input v-model="ruleForm.title"></el-input>
        </el-form-item>
        <el-form-item label="开始日期" firstDayOfWeek="1">
          <el-date-picker
            v-model="start_date"
            type="week"
            format="yyyy 第 WW 周"
            :picker-options="{
              firstDayOfWeek: 1
            }"
            placeholder="选择周">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="开始时间" firstDayOfWeek="1">
          <el-time-select
            placeholder="起始时间"
            v-model="startTime"
            :picker-options="{
              start: '08:00',
              step: '01:00',
              end: '24:00',
            }">
          </el-time-select>
          <el-time-select
            placeholder="结束时间"
            v-model="endTime"
            :picker-options="{
              start: '08:00',
              step: '01:00',
              end: '24:00',
              minTime: startTime
            }">
          </el-time-select>
        </el-form-item>
        <el-form-item label="类名" prop="cssClass">
          <el-input v-model="ruleForm.cssClass"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="addGroupSubmit('ruleForm')">立即创建</el-button>
          <el-button @click="resetForm('ruleForm')">重置</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
export default {
  components: {},
  data() {
    return {
      addEvent: false,
      ruleForm: {
        title: '',
        start: '',
        end: '',
        cssClass: 'yellow'
      },
      events: [
        {
          title: 'event1',
          start: '2018-01-22',
          cssClass: 'blue'
        },
        {
          title: 'event2',
          start: '2018-01-12',
          end: '2018-01-12',
          cssClass: 'green'
        }
      ],
      start_date: '',
      startTime: '',
      endTime: ''
    }
  },
  methods: {
    eventClick(event, jsEvent, pos) {
      console.log('eventClick', event, jsEvent, pos)
    },
    addGroupSubmit(formName) {
      console.log(formName)
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    }
  }
}
</script>
