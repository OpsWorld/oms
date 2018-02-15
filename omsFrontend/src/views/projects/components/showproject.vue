<template>
  <el-card>
    <div slot="header" class="clearfix">
      <a>{{ruleForm.name}}</a>
    </div>
    <el-form label-position="left" inline class="table-expand">
      <el-form-item label="状态" prop="status">
        <span>{{ STATUS_TEXT[ruleForm.status] }}</span>
      </el-form-item>
      <el-form-item label="开发" prop="action_user">
        <el-tag size="mini" v-for="item in ruleForm.action_user" :key="item.id" style="margin-right: 3px">{{item}}
        </el-tag>
      </el-form-item>
      <el-form-item label="等级" prop="level">
        <span>{{ ruleForm.level }}</span>
      </el-form-item>
      <el-form-item label="关闭时间" prop="end_time">
        <span>{{ ruleForm.end_time }}</span>
      </el-form-item>
      <el-form-item label="关闭时间" prop="end_time">
        <span>{{ ruleForm.end_time }}</span>
      </el-form-item>
      <el-form-item label="任务进度" prop="task_complete">
        <span>{{ ruleForm.task_complete }}</span>
      </el-form-item>
      <el-form-item label="测试进度" prop="test_complete">
        <span>{{ ruleForm.test_complete }}</span>
      </el-form-item>
      <el-form-item label="描述" prop="desc">
        <span>{{ ruleForm.desc }}</span>
      </el-form-item>
    </el-form>
  </el-card>
</template>
<script>
export default {
  components: {},
  props: ['ruleForm'],
  data() {
    return {
      STATUS_TEXT: { '0': '未指派', '1': '已指派', '2': '处理中', '3': '待审核', '4': '已完成' }
    }
  },
  created() {
  },
  methods: {}
}
</script>
