<template>
    <section class="app-main">
        <levelbar></levelbar>
        <router-view :key="key"></router-view>
    </section>
</template>

<script>
    import Levelbar from './Levelbar';
    export default {
        name: 'AppMain',

        components: {Levelbar,},
        computed: {
            key() {
                return this.$route.name !== undefined ? this.$route.name + +new Date() : this.$route + +new Date()
            }
        }
    }
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    .app-main {
        padding-top: 55px;
    }
</style>