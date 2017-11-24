<template>
    <div id="chat">
        <div class="sidebar">
            <chat-card></chat-card>
            <chat-list></chat-list>
        </div>
        <div class="main">
            <chat-message></chat-message>
            <chat-text></chat-text>
        </div>
    </div>
</template>

<script>
    import chatCard from './card';
    import chatList from './list';
    import chatText from './text';
    import chatMessage from './message';
    export default {
        components: {chatCard, chatList, chatText, chatMessage},
        data () {
            return {}
        }
    }
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    #chat {
        margin: 20px auto;
        width: 800px;
        height: 600px;
        overflow: hidden;
        border-radius: 3px;
        .sidebar, .main {
            height: 100%;
        }
        .sidebar {
            float: left;
            width: 200px;
            color: #f4f4f4;
            background-color: #2e3238;
        }
        .main {
            position: relative;
            overflow: hidden;
            background-color: #eee;
        }
        .text {
            position: absolute;
            width: 100%;
            bottom: 0;
            left: 0;
        }
        .message {
            height: calc(100% - 160px);
        }
    }
</style>