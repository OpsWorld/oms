<template>
  <div class="components-container" style='height:100vh'>
    <el-card class="viewwiki">
      <div class="viewwiki-content">
        <h1>{{rowdata.title}}</h1>
        <div class="meta">
          <el-button type="danger" plain size="mini">{{rowdata.type}}</el-button>
          <a class="author">
            <i class="fa fa-user"></i>{{rowdata.create_user}}
          </a>
          <a class="create_time">
            <i class="fa fa-calendar"></i>{{rowdata.create_time | formatTime}}
          </a>
        </div>
        <hr class="heng"/>
        <p class="abstract">
          <vue-markdown :source="rowdata.content"></vue-markdown>
        </p>
      </div>
    </el-card>
  </div>
</template>
<script>
import { getWiki } from 'api/wiki'
import VueMarkdown from 'vue-markdown' // 前端显示

export default {
  components: {
    VueMarkdown
  },
  data() {
    return {
      rowdata: {},
      route_path: this.$route.path.split('/'),
      wikiid: this.$route.params.wikiid
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      const parms = null
      getWiki(parms, this.wikiid).then(response => {
        this.rowdata = response.data
      })
    }
  }
}
</script>

<style lang='scss'>
  .viewwiki {
    text-align: center;
    .viewwiki-content {
      .meta {
        font-size: 12px;
        font-weight: 400;
        line-height: 20px;
        color: rgba(128, 128, 128, 0.82);
        a {
          padding: 0 10px;
          i {
            padding-right: 5px;
          }
          &:hover {
            color: rgb(75, 75, 75);
          }
        }
      }
      .abstract {
        text-align: left;
        margin: 10px 10%;
      }
    }
  }
</style>
