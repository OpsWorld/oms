<template>
  <div class="menu-wrapper">
    <template v-for="item in routes" v-if="!item.hidden&&item.children.length>0">

      <router-link v-if="item.children.length===1 && !item.children[0].children && item.children[0].icon == 'dashboard'"
                   :to="item.path+'/'+item.children[0].path" :key="item.children[0].name">
        <el-menu-item :index="item.path+'/'+item.children[0].path" class='submenu-title-noDropdown'>
          <icon v-if='item.children[0].icon' :name="item.children[0].icon" :scale="iconsize" class="wscn-icon"></icon>
          <span v-if="item.children[0]&&item.children[0].name">{{item.children[0].name}}</span>
        </el-menu-item>
      </router-link>

      <el-submenu v-else :index="item.name||item.path" :key="item.name">
        <template slot="title">
          <icon v-if='item.icon' :name="item.icon" :scale="iconsize" class="wscn-icon"></icon>
          <span v-if="item&&item.name">{{item.name}}</span>
        </template>

        <template v-for="child in item.children" v-if="!child.hidden">
          <sidebar-item class="nest-menu" v-if="child.children&&child.children.length>0" :routes="[child]"
                        :key="child.path"></sidebar-item>
          <router-link v-else :to="item.path+'/'+child.path" :key="child.name">
            <el-menu-item :index="item.path+'/'+child.path">
              <icon name="diamond" scale="1" class="child-icon"></icon>
              <span v-if="child&&child.name">{{child.name}}</span>
            </el-menu-item>
          </router-link>
        </template>
      </el-submenu>

    </template>
  </div>
</template>

<script>
export default {
  name: 'SidebarItem',
  props: {
    routes: {
      type: Array
    }
  },
  data() {
    return {
      iconsize: 1.4
    }
  },
  methods: {
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
  .wscn-icon {
    margin-right: 10px;
    min-width: 25px;
  }

  .child-icon {
    color: rgba(88, 255, 40, 0.38);
    margin-right: 10px;
  }

  .hideSidebar .menu-indent {
    display: block;
    text-indent: 10px;
  }
</style>
