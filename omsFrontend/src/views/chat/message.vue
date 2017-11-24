<template>
    <div class="message" v-scroll-bottom="session.messages">
        <ul v-if="session">
            <li v-for="item in session.messages">
                <p class="time">
                    <span>{{ item.date }}</span>
                </p>
                <div class="main" :class="{ self: item.self }">
                    <img class="avatar" width="30" height="30" :src="item.self ? user.img : session.user.img"/>
                    <div class="text">{{ item.content }}</div>
                </div>
            </li>
        </ul>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                session: {
                    messages: [
                        {date: "2016年12月3日", content: "你好，我是马云，今晚我在301等你！"}
                    ],
                    user: {name: "aaa", img: "http://obbqb7m24.bkt.clouddn.com/avatar.jpg"}
                }
            }
        },

        methods: {
            onKeyup (e) {
                console.log(e);
            }
        }
    };
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    .message {
        padding: 10px 15px;
        overflow-y: scroll;
        li {
            margin-bottom: 15px;
            list-style-type: none;
            margin-left: -40px;
        }
        .time {
            margin: 7px 0;
            text-align: center;
            > span {
                display: inline-block;
                padding: 0 18px;
                font-size: 12px;
                color: #fff;
                border-radius: 2px;
                background-color: #dcdcdc;
            }
        }
        .avatar {
            float: left;
            margin: 0 10px 0 0;
            border-radius: 3px;
        }
        .text {
            display: inline-block;
            position: relative;
            padding: 0 10px;
            max-width: calc(100% - 40px);
            min-height: 30px;
            line-height: 2.5;
            font-size: 12px;
            text-align: left;
            word-break: break-all;
            background-color: #fafafa;
            border-radius: 4px;
            &:before {
                content: " ";
                position: absolute;
                top: 9px;
                right: 100%;
                border: 6px solid transparent;
                border-right-color: #fafafa;
            }
        }
        .self {
            text-align: right;
            .avatar {
                float: right;
                margin: 0 0 0 10px;
            }
            .text {
                background-color: #b2e281;
                &:before {
                    right: inherit;
                    left: 100%;
                    border-right-color: transparent;
                    border-left-color: #b2e281;
                }
            }
        }
    }
</style>