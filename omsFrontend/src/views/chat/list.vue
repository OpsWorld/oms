<template>
    <div class="list">
        <ul>
            <li v-for="item in users" :class="{ active: item.id === currentId }" @click="selectSession(item.id)">
                <img class="avatar" width="30" height="30" :alt="item.user.name" :src="item.user.img">
                <p class="name">{{item.user.name}}</p>
            </li>
        </ul>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                currentId: '',
                users: [
                    {
                        id: 1, user: {
                        name: "ddd",
                        img: "http://obbqb7m24.bkt.clouddn.com/avatar.jpg"
                    }
                    },
                    {
                        id: 2, user: {
                        name: "bbb",
                        img: "http://obbqb7m24.bkt.clouddn.com/avatar.jpg"
                    }
                    },
                ]
            }
        },
        methods: {
            selectSession(id) {
                this.currentId = id
            }
        }
    }
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    .list {
        li {
            list-style-type: none;
            margin-left: -40px;
            padding: 12px 15px;
            border-bottom: 1px solid #292C33;
            cursor: pointer;
            transition: background-color .1s;
            &:hover {
                background-color: rgba(255, 255, 255, 0.03);
            }
            &.active {
                background-color: rgba(255, 255, 255, 0.1);
            }
        }
        .avatar, .name {
            vertical-align: middle;
        }
        .avatar {
            border-radius: 2px;
        }
        .name {
            display: inline-block;
            margin: 0 0 0 15px;
        }
    }
</style>