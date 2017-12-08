<template>
  <div class="errPage-container">
    <el-button @click="back" icon='arrow-left' class="pan-back-btn">返回</el-button>
    <el-row>
      <el-col :span="12">
        <h1 class="text-jumbo text-ginormous">Oops!</h1>
        <h2 style="color: #ffffff">龙母 说没有权限去该页面</h2>
        <h6 style="color: #dedede">如有不满请联系雪诺</h6>
        <ul class="list-unstyled">
          <li style="color: #58ff28">或者你可以去:</li>
          <li class="link-type">
            <router-link to="/dashboard">回首页</router-link>
          </li>
          <li class="link-type"><a href="https://www.taobao.com/">随便看看</a></li>
          <li><a @click.prevent="dialogVisible=true" href="#">点我看图</a></li>
        </ul>
      </el-col>
      <el-col :span="12">
        <img :src="longmu" height="428" alt="龙母壮骨颗粒">
      </el-col>
    </el-row>

    <el-dialog title="随便看" :visible.sync="dialogVisible" size="large">
      <img class="pan-img" :src="ewizardClap">
    </el-dialog>
  </div>
</template>

<script>
    import errGif from 'assets/401.gif';
    import longmu from 'assets/long.png';
    export default {
      data() {
        return {
          longmu: longmu + '?' + +new Date(),
          ewizardClap: 'https://wpimg.wallstcn.com/007ef517-bafd-4066-aae4-6883632d9646',
          dialogVisible: false
        }
      },
      methods: {
        back() {
          if (this.$route.query.noGoBack) {
            this.$router.push({ path: '/dashboard' });
          } else {
            this.$router.go(-1);
          }
        }
      }
    };
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
  .errPage-container {
    width: 800px;
    margin: 100px auto;
    .pan-back-btn {
      background: #008489;
      color: #fff;
    }
    .pan-gif {
      margin: 0 auto;
      display: block;
    }
    .pan-img {
      display: block;
      margin: 0 auto;
    }
    .text-jumbo {
      font-size: 60px;
      font-weight: 700;
      color: #ff1324;
    }
    .list-unstyled {
      font-size: 14px;
      li {
        padding-bottom: 5px;
      }
      a {
        color: #008489;
        text-decoration: none;
        &:hover {
          text-decoration: underline;
        }
      }
    }
  }
</style>
