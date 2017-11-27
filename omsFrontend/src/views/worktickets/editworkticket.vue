<template xmlns="http://www.w3.org/1999/html">
    <div class="editticket">
        <el-card>
            <div class="workticket">
                <el-card>
                    <div slot="header" class="clearfix">
                        <a class="title">{{ticketData.title}}</a>
                        <div class="appendInfo">
                            <a class="ticketinfo create_user"><span
                                    class="han">工单创建时间：</span>{{ticketData.create_time | parseDate}}</a>
                            <a class="ticketinfo create_user"><span class="han">工单发起人：</span>{{ticketData.create_user}}</a>
                            <a class="ticketinfo action_user"><span
                                    class="han">当前处理人：</span>{{rowdata.action_user ? rowdata.action_user : ticketData.action_user}}</a>
                        </div>
                    </div>
                    {{ticketData.content}}
                </el-card>
            </div>

            <el-form v-if="ticketData.ticket_status!=2" :model="ruleForm" :rules="rules" ref="ruleForm"
                     label-width="80px" class="demo-ruleForm">
                <hr class="heng"/>
                <el-form-item label="问题回复" prop="content">
                    <el-tooltip class="item" effect="dark" content="先接收工单才能回复处理过程"
                                :disabled="ticketData.ticket_status==0?false:true" placement="right">
                        <el-input v-model="ruleForm.content" type="textarea"
                                  :disabled="ticketData.ticket_status==0?true:false"
                                  :autosize="{ minRows: 3, maxRows: 5}"></el-input>
                    </el-tooltip>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submitForm('ruleForm')" style="float: right">提交</el-button>
                </el-form-item>
            </el-form>
            <hr class="heng"/>
            处理过程：
            <hr class="heng"/>
            <div class="ticketcomment" v-for="item in commentData" :key="item.id">
                <el-row>
                    <el-col :span="1">
                        <el-button type="primary" plain class="commentuser">{{item.create_user}}</el-button>
                    </el-col>
                    <el-col :span="14">
                        <div class="dialog-box">
                            <span class="bot"></span>
                            <span class="top"></span>
                            <div class="comment">
                                {{item.content}}
                                <p class="commenttime">处理时间：{{item.create_time | parseDate}}</p>
                            </div>
                        </div>
                    </el-col>
                </el-row>
            </div>
            <hr class="heng"/>
            <div v-if="ticketData.ticket_status!=2">
                工单操作：
                <el-button type="success" @click="changeTicketStatus(1)"
                           :disabled="ticketData.ticket_status==0?false:true">接收
                </el-button>
                <el-button type="danger" @click="changeTicketStatus(2)"
                           :disabled="ticketData.ticket_status!=2?false:true">关闭
                </el-button>
            </div>
        </el-card>
    </div>
</template>
<script>
    import {getWorkticket, patchWorkticket, getTicketcomment, postTicketcomment} from 'api/workticket'

    export default {
        components: {},

        data() {
            return {
                route_path: this.$route.path.split('/'),
                ticket_id: '',
                ticketData: {},
                ticket__title: '',
                commentData: {},
                ruleForm: {
                    ticket: '',
                    create_user: localStorage.getItem('username'),
                    content: '',
                    create_group: ''
                },
                rules: {
                    content: [
                        {required: true, message: '赏几个字吧', trigger: 'blur'},
                    ]
                },
                rowdata: {
                    ticket_status: 1,
                    action_user: ''
                },
            };
        },

        created() {
            this.ticket_id = this.ruleForm.ticket = this.route_path[this.route_path.length - 1];
            this.fetchData();
            this.CommentData()
        },
        methods: {
            fetchData() {
                const ticket_parms = null;
                getWorkticket(this.ticket_id, ticket_parms).then(response => {
                    this.ticketData = response.data;
                });
            },
            CommentData() {
                const comment_parms = {
                    ticket__id: this.ticket_id
                };
                getTicketcomment(comment_parms).then(response => {
                    this.commentData = response.data.results;
                    this.rowdata.action_user = this.commentData[this.commentData.length - 1]['create_user'];
                })
            },
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        postTicketcomment(this.ruleForm);
                        this.patchForm(this.rowdata);
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                    setTimeout(this.CommentData, 1000);
                });
            },
            patchForm(rowdata) {
                patchWorkticket(this.ticket_id, rowdata)
            },
            changeTicketStatus(status) {
                this.rowdata.ticket_status = this.ticketData.ticket_status = status;
                patchWorkticket(this.ticket_id, this.rowdata)
            }
        }
    }
</script>

<style lang='scss'>
    .editticket {
        margin: 50px;
        width: 800px;
        .title {
            color: #feff25;
            font-size: 30px;
            padding-left: 10px;
        }
        .appendInfo {
            .ticketinfo {
                margin-left: 5px;
                .han {
                    color: rgba(43, 200, 13, 0.6);
                    font-size: 16px;
                }
            }
        }
    }

    .content {
        margin: 20px 5px;
    }

    .heng {
        margin: 20px 0;
        height: 1px;
        border: 0px;
        background-color: rgba(174, 127, 255, 0.38);
        color: #29e11c;
    }

    .ticketcomment {
        .commentuser {
        }
        .dialog-box {
            position: relative;
            left: 100px;
            margin-left: -20px;
            span {
                width: 0;
                height: 0;
                font-size: 0;
                overflow: hidden;
                position: absolute;
                &.bot {
                    border-width: 16px;
                    border-style: solid dashed dashed;
                    border-color: transparent #4cff1e transparent transparent;
                    top: 10px;
                    left: -30px;
                }
                &.top {
                    border-width: 18px;
                    border-style: solid dashed dashed;
                    border-color: transparent #fff transparent transparent;
                    top: 10px;
                    left: -30px;

                }
            }
            .comment {
                border: solid 1px rgba(255, 164, 186, 0.62);
                padding: 6px;
                margin-bottom: 10px;
                min-height: 50px;
                max-width: 600px;
                width: 50rem;
                .commenttime {
                    float: right;
                }
            }
        }

    }
</style>