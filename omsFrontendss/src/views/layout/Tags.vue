<template>
    <el-tag :closable="true" :color="color()" @close='closeViewTabs(tag,$event)'>
        {{tag.name}}
    </el-tag>
</template>

<script>
    export default {
        props: ['tag'],
        methods: {
            color() {
                return '#' + Math.floor(Math.random() * 1000000);
            },

            closeViewTabs(view, $event) {
                this.$store.dispatch('delVisitedViews', view)
                $event.preventDefault()
            }
        }
    }
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
</style>