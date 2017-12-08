<template>
    <div class="navbar">
        <hamburger class="hamburger-container" :toggleClick="toggleSideBar" :isActive="sidebar.opened"></hamburger>
        <el-breadcrumb class="app-levelbar" separator="/">
            <el-breadcrumb-item v-for="(item,index)  in levelList" :key="item.id">
                <router-link v-if='item.redirect==="noredirect"||index==levelList.length-1' to="" class="no-redirect">
                    {{item.name}}
                </router-link>
                <router-link v-else :to="item.path">
                    <icon v-show="item.name==='首页'" name="home" class="wscn-icon"></icon>
                    {{item.name}}
                </router-link>
            </el-breadcrumb-item>
        </el-breadcrumb>
        <screenfull class='screenfull'></screenfull>
    </div>

</template>

<script>
    import Hamburger from 'components/Hamburger';
    import Screenfull from 'components/Screenfull';
    import {mapGetters} from 'vuex';

    export default {
        components: {
            Hamburger,
            Screenfull,
        },
        created() {
            this.getBreadcrumb()
        },
        data() {
            return {
                levelList: null
            }
        },
        computed: {
            ...mapGetters([
                'sidebar',
            ]),
        },
        methods: {
            toggleSideBar() {
                this.$store.dispatch('ToggleSideBar')
            },
            getBreadcrumb() {
                let matched = this.$route.matched.filter(item => item.name);
                const first = matched[0];
                if (first && (first.name !== '首页' || first.path !== '')) {
                    matched = [{name: '首页', path: '/'}].concat(matched)
                }
                this.levelList = matched;
            }
        },
        watch: {
            $route() {
                this.getBreadcrumb();
            }
        }
    }
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    .navbar {
        height: 50px;
        line-height: 50px;
        .hamburger-container {
            line-height: 58px;
            height: 50px;
            float: left;
            padding: 0 10px;
        }
        .app-levelbar.el-breadcrumb {
            display: inline-block;
            font-size: 14px;
            line-height: 50px;
            margin-left: 10px;
            .no-redirect {
                color: #97a8be;
                cursor: text;
            }
        }
        .screenfull {
            position: absolute;
            right: 10px;
            top: 70px;
        }
    }

</style>
