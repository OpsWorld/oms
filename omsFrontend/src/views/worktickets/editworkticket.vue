<template xmlns="http://www.w3.org/1999/html">
    <el-card class="editticket">
        <div class="workticket">
            <h3 class="post-title">{{ticketData.title}}</h3>
            <hr style="margin:0px;height:1px;border:0px;background-color:#D5D5D5;color:#D5D5D5;"/>
            <p class="datetime">创建时间：{{ticketData.create_time}}</p>
            <p class="create_user">创建人：{{ticketData.create_user}}</p>
            <p class="action_user">当前处理人人：{{ticketData.action_user}}</p>
            <div class="content">详细内容：{{ticketData.content}}</div>
        </div>
        <hr style="margin:0px;height:1px;border:0px;background-color:#D5D5D5;color:#D5D5D5;"/>

        <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
            <el-form-item prop="content">
                <el-input v-model="ruleForm.content" type="textarea" :autosize="{ minRows: 10, maxRows: 30}"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="submitForm('ruleForm')" style="float: right">提交</el-button>
            </el-form-item>
        </el-form>

        <div class="ticketcomment" v-for="item in commentData" :key="item.id">
            <p class="datetime">回复时间：{{item.create_time}}</p>
            <p class="create_user">回复人：{{item.create_user}}</p>
            <div class="content">回复内容：{{item.content}}</div>
        </div>
    </el-card>
</template>
<script>
    import {getWorkticket, putWorkticket, getTicketcomment, postTicketcomment} from 'api/workticket'
    import ElCard from "../../../node_modules/element-ui/packages/card/src/main";

    export default {
        components: {ElCard},

        data() {
            return {
                ticketData: {},
                ticket__title: '',
                commentData: {},
                ruleForm: {
                    content: ''
                },
                rules: {
                    content: [
                        {required: true, message: '请陛下赏几个字吧', trigger: 'blur'},
                    ]
                }
            };
        },

        created() {
            this.fetchData()
        },
        methods: {
            fetchData() {
                const route_path = this.$route.path.split('/');
                const ticket_id = route_path[route_path.length - 1];
                const ticket_parms = null;
                getWorkticket(ticket_id, ticket_parms).then(response => {
                    this.ticketData = response.data;
                });
                const comment_parms = {
                    ticket__id: ticket_id
                };
                getTicketcomment(comment_parms).then(response => {
                    this.commentData = response.data.results;
                })
            },
        }
    }
</script>

<style lang='scss'>
    .editticket {
        margin: 20px;
        .post-title {
            text-align: center;
        }
    }
</style>