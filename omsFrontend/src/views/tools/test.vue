<template xmlns="http://www.w3.org/1999/html">
  <div class="components-container" style='height:100vh'>
    <el-card>
      <el-upload
        class="upload-demo"
        ref="upload"
        action="1024"
        :file-list="fileList"
        :on-success="handleAvatarSuccess"
        :before-upload="beforeAvatarUpload">
        <el-button slot="trigger" size="small" type="primary">
          上传文件
        </el-button>
        (可以不用上传)
        <div slot="tip" class="el-upload__tip">
          <p>上传文件不超过10m，<a style="color: red">最多只能上传3个文件</a></p>
        </div>
      </el-upload>
    </el-card>
  </div>
</template>
<script>
export default {
  data() {
    return {
      fileList: []
    }
  },

  methods: {
    handleAvatarSuccess(res, file) {
      this.imageUrl = URL.createObjectURL(file.raw)
    },
    beforeAvatarUpload(file) {
      console.log(file)
      const isJPG = file.type === 'image/jpeg'
      const isLt2M = file.size / 1024 / 1024 < 2

      if (!isJPG) {
        this.$message.error('上传头像图片只能是 JPG 格式!')
      }
      if (!isLt2M) {
        this.$message.error('上传头像图片大小不能超过 2MB!')
      }
      return false
    }
  }
}
</script>
