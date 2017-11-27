<template>
    <div class="sidebar">
        <el-menu mode="vertical" theme="dark" :default-active="$route.path" :unique-opened="true">
            <sidebar-item :routes='$router.options.routes'></sidebar-item>
        </el-menu>
    </div>
</template>

<script>
    import SidebarItem from './SidebarItem';
    export default {
        components: {SidebarItem},
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
