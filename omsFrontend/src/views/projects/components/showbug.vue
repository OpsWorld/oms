<template>
  <el-card>
    <div slot="header" class="clearfix">
      <a>{{ruleForm.name}}</a>
    </div>
    <el-form label-position="left" inline class="table-expand">
      <el-form-item label="严重程度" prop="degree">
        <el-rate
          v-model="ruleForm.degree"
          :colors="['#99A9BF', '#F7BA2A', '#ff1425']"
          disabled>
        </el-rate>
      </el-form-item>
      <el-form-item label="优先级" prop="nice">
        <span>{{ Bug_Nice[ruleForm.nice] }}</span>
      </el-form-item>
      <el-form-item label="状态" prop="status">
        <span>{{ Bug_Status[ruleForm.status] }}</span>
      </el-form-item>
      <el-form-item label="开发" prop="action_user">
        <span>{{ ruleForm.action_user }}</span>
      </el-form-item>
      <el-form-item label="测试时间" prop="test_time">
        <span>{{ ruleForm.test_time }}</span>
      </el-form-item>
      <el-form-item label="关闭时间" prop="end_time">
        <span>{{ ruleForm.end_time }}</span>
      </el-form-item>
      <el-form-item label="描述" prop="desc">
        <vue-markdown :source="ruleForm.desc"></vue-markdown>
      </el-form-item>
    </el-form>
  </el-card>
</template>
<script>
import VueMarkdown from 'vue-markdown' // 前端解析markdown

export default {
  components: { VueMarkdown },
  props: ['ruleForm'],
  data() {
    return {
      Bug_Nice: {
        0: '低',
        1: '中',
        2: '高'
      },
      Bug_Status: {
        0: '新建',
        1: '打开',
        2: '关闭',
        3: '已修复',
        4: '暂不处理',
        5: '重新打开'
      }
    }
  },
  created() {
  },
  methods: {}
}
</script>
