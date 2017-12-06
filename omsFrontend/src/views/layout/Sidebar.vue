<template>
    <div class="sidebar">
        <el-menu mode="vertical" background-color="#000" text-color="#fff" :default-active="$route.path"
                 :unique-opened="true">
            <sidebar-item :routes='permission_routers'></sidebar-item>
        </el-menu>
    </div>
</template>

<script>
    import SidebarItem from './SidebarItem'
    import {mapGetters} from 'vuex'


    export default {
        components: {SidebarItem},
        created() {
            //console.log(this.permission_routers)
        },
        computed: {
            ...mapGetters([
                'permission_routers'
            ]),
        },
    }
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    .el-menu {
        min-height: 100%;
    }

    .sidebar {
        padding-top: 55px;
    }
</style>
