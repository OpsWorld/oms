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
    import router from '@/router'
    import store from '@/store'

    export default {
        components: {SidebarItem},
        created() {
            this.GetMyRouters()
        },
        computed: {
            ...mapGetters([
                'permission_routers'
            ]),
        },
        methods: {
            GetMyRouters() {
                const username = localStorage.getItem('username');
                store.dispatch('GenerateRoutes', { username }).then(() => { // 生成可访问的路由表
                router.addRoutes(store.getters.addRouters); // 动态添加可访问路由表
                next({ ...to }) // hack方法 确保addRoutes已完成
            })
            }
        }
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
