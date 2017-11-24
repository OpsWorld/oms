<template>
    <div class="text">
        <textarea placeholder="按 Ctrl + Enter 发送" v-model="content" @keyup="onKeyup"></textarea>
    </div>
</template>

<script>
    export default {
        data () {
            return {
                content: ''
            };
        },
        methods: {
            onKeyup (e) {
                if (e.ctrlKey && e.keyCode === 13 && this.content.length) {
                    console.log(this.content);
                    this.content = '';
                }
            }
        }
    };
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    .text {
        height: 160px;
        border: solid 1px #ddd;
        textarea {
            padding: 10px;
            height: 100%;
            width: 100%;
            border: none;
            outline: none;
            font-family: "Micrsofot Yahei";
            resize: none;
        }
    }
</style>