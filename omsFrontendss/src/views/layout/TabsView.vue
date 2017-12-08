<template>
    <div class='tabs-view-container'>
        <router-link class="tabs-view" v-for="tag in Array.from(visitedViews)" :to="tag.path" :key="tag.path">
            <tag :tag="tag"></tag>
        </router-link>
    </div>
</template>

<script>
    import Tag from './Tags.vue'
    export default {
        components: {Tag},
        computed: {
            visitedViews() {
                return this.$store.state.app.visitedViews.slice(-6)
            }
        },
        methods: {
            generateRoute() {
                if (this.$route.matched[this.$route.matched.length - 1].name) {
                    return this.$route.matched[this.$route.matched.length - 1]
                }
                this.$route.matched[0].path = '/'
                return this.$route.matched[0]
            },
            addViewTabs() {
                this.$store.dispatch('addVisitedViews', this.generateRoute())
            }
        },
        watch: {
            $route() {
                this.addViewTabs()
            }
        }
    }
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    .tabs-view-container {
        display: inline-block;
        vertical-align: top;
        margin-left: 10px;
        .tabs-view {
            margin-left: 10px;
        }
    }
</style>
