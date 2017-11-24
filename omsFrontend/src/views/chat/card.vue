<template>
    <div class="card">
        <header>
            <img class="avatar" width="40" height="40" :alt="user.name" :src="user.img">
            <p class="name">{{user.name}}</p>
        </header>
        <footer>
            <input class="search" type="text" placeholder="search user..." @keyup="onKeyup">
        </footer>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                user: {
                    name: "aaa",
                    img: "http://obbqb7m24.bkt.clouddn.com/avatar.jpg"
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
    .card {
        padding: 12px;
        border-bottom: solid 1px #24272C;
        footer {
            margin-top: 10px;
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
            font-size: 16px;
        }
        .search {
            padding: 0 10px;
            width: 100%;
            font-size: 12px;
            color: #fff;
            height: 30px;
            line-height: 30px;
            border: solid 1px #3a3a3a;
            border-radius: 4px;
            outline: none;
            background-color: #26292E;
        }
    }
</style>