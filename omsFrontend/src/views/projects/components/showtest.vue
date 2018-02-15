<template>
  <el-card>
    <div slot="header" class="clearfix">
      <a>{{ruleForm.name}}</a>
    </div>
    <el-form label-position="left" inline class="table-expand">
      <el-form-item label="预期结果" prop="expect_result">
        <span>{{ ruleForm.expect_result }}</span>
      </el-form-item>
      <el-form-item label="实际结果" prop="actual_result">
        <span>{{ ruleForm.actual_result }}</span>
      </el-form-item>
      <el-form-item label="状态" prop="status">
        <span>{{ TEST_STATUS[ruleForm.status] }}</span>
      </el-form-item>
      <el-form-item label="开发" prop="action_user">
        <span>{{ ruleForm.action_user }}</span>
      </el-form-item>
      <el-form-item label="测试时间" prop="test_time">
        <span>{{ ruleForm.test_time }}</span>
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
      TEST_STATUS: { '0': 'Passed', '1': 'Failed', '2': 'Block', '3': 'N/A' }
    }
  },
  created() {
  },
  methods: {}
}
</script>
