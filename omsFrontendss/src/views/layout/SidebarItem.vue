<template>
    <div>
        <template v-for="item in routes">
            <router-link v-if="!item.hidden&&item.noDropdown&&item.children.length>0"
                         :to="item.path+'/'+item.children[0].path">
                <el-menu-item :index="item.path+'/'+item.children[0].path" class="icon-title">
                    <icon v-if='item.icon' :name="item.icon" :scale="iconsize" class="wscn-icon"></icon>
                    {{item.children[0].name}}
                </el-menu-item>
            </router-link>
            <el-submenu :index="item.name" v-if="!item.noDropdown&&!item.hidden">
                <template slot="title">
                    <icon v-if='item.icon' :name="item.icon" :scale="iconsize" class="wscn-icon"></icon>
                    {{item.name}}
                </template>
                <template v-for="child in item.children" v-if='!child.hidden'>
                    <sidebar-item class='menu-indent' v-if='child.children&&child.children.length>0'
                                  :routes='[child]'></sidebar-item>
                    <router-link v-else class="menu-indent" :to="item.path+'/'+child.path">
                        <el-menu-item :index="item.path+'/'+child.path">
                            <icon name="dot-circle-o" scale="1" class="child-icon"></icon>
                            {{child.name}}
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
        data () {
            return {
                iconsize: 1.6
            }
        }
    }
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    .wscn-icon {
        margin-right: 10px;
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

