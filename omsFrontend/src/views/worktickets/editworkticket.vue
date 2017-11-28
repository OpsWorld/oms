<template xmlns="http://www.w3.org/1999/html">
    <div class="editticket">
        <el-card>
            <div class="workticket">
                <el-card>
                    <div slot="header" class="clearfix">
                        <a class="title">{{ticketData.title}}</a>
                        <div class="appendInfo">
                            <a class="ticketinfo create_user"><span class="han">
                                工单创建时间：</span>{{ticketData.create_time | parseDate}}</a>
                            <a class="ticketinfo create_user"><span class="han">
                                工单发起人：</span>{{ticketData.create_user}}</a>
                            <a class="ticketinfo action_user"><span class="han">
                                当前处理人：</span>{{rowdata.action_user ? rowdata.action_user : ticketData.action_user}}</a>
                        </div>
                    </div>
                    <vue-markdown :source="ticketData.content"></vue-markdown>
                </el-card>
            </div>

            <el-form v-if="ticketData.ticket_status!=2" :model="commentForm" :rules="rules" ref="ruleForm"
                     label-width="80px" class="demo-ruleForm">
                <hr class="heng"/>
                <el-form-item label="问题回复" prop="content">
                    <el-tooltip class="item" effect="dark" content="先接收工单才能回复处理过程"
                                :disabled="ticketData.ticket_status==0?false:true" placement="right">
                        <el-input v-model="commentForm.content" type="textarea"
                                  :disabled="ticketData.ticket_status==0?true:false"
                                  :autosize="{ minRows: 3, maxRows: 5}"></el-input>
                    </el-tooltip>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submitForm('ruleForm')" style="float: right">提交</el-button>
                </el-form-item>
                <hr class="heng"/>
            </el-form>
            <div>
                <el-upload
                        class="upload-demo"
                        ref="upload"
                        action="https://jsonplaceholder.typicode.com/posts/"
                        :on-success="handleSuccess"
                        :show-file-list="false"
                        :disabled="count>2?true:false">
                    <el-button slot="trigger" size="small" type="info" icon="upload2" :disabled="count>2?true:false">
                        上传文件
                    </el-button>
                    <div slot="tip" class="el-upload__tip">
                        <p>上传文件不超过500kb，<a style="color: red">最多只能上传3个文件</a></p>
                    </div>
                </el-upload>
                <hr class="heng"/>
            </div>
            <div v-if='enclosureData.length>0' class="ticketenclosure">
                <ul>
                    <li v-for="item in enclosureData" :key="item.id" v-if="item.file">
                        <a :href="apiurl + '/upload/' +item.file" download="item.id">{{item.file}}</a>
                        <el-button type="text" size="small" @click="deleteEnclosure(item.id)">删除</el-button>
                    </li>
                </ul>
            </div>
            <div class="ticketcomment" v-for="item in commentData" :key="item.id">
                处理过程：
                <hr class="heng"/>
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
            <div v-if="ticketData.ticket_status!=2">
                <hr class="heng"/>
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
    import {
        getWorkticket,
        patchWorkticket,
        getTicketcomment,
        postTicketcomment,
        postTicketenclosure,
        getTicketenclosure,
        deleteTicketenclosure,
    } from 'api/workticket'
    import {postUpload} from 'api/tool'
    import {apiUrl} from '@/config'
    import VueMarkdown from 'vue-markdown'   //前端显示

    export default {
        components: {VueMarkdown},

        data() {
            return {
                route_path: this.$route.path.split('/'),
                ticket_id: '',
                ticketData: {},
                ticket__title: '',
                commentData: {},
                enclosureData: {},
                apiurl: apiUrl,
                commentForm: {
                    ticket: '',
                    create_user: localStorage.getItem('username'),
                    content: '',
                    create_group: ''
                },
                enclosureForm: {
                    ticket: '',
                    create_user: localStorage.getItem('username'),
                    file: '',
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
                count: 0,
            };
        },

        created() {
            this.ticket_id = this.route_path[this.route_path.length - 1];
            this.fetchData();
            this.CommentData();
            this.EnclosureData();
        },
        methods: {
            fetchData() {
                const parms = null;
                getWorkticket(this.ticket_id, parms).then(response => {
                    this.ticketData = response.data;
                });
            },
            CommentData() {
                const parms = {
                    ticket__id: this.ticket_id
                };
                getTicketcomment(parms).then(response => {
                    this.commentData = response.data.results;
                    this.rowdata.action_user = this.commentData.length == 0 ? null : this.commentData[this.commentData.length - 1].create_user;
                })
            },
            EnclosureData() {
                const parms = {
                    ticket__id: this.ticket_id
                };
                getTicketenclosure(parms).then(response => {
                    this.enclosureData = response.data.results;
                    this.count = response.data.count;
                })
            },
            deleteEnclosure(id) {
                deleteTicketenclosure(id);
                setTimeout(this.EnclosureData, 1000);
            },
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        this.commentForm.ticket = this.ticket_id;
                        postTicketcomment(this.commentForm);
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
            },
            handleSuccess(file, fileList) {
                let formData = new FormData();
                formData.append('username', this.enclosureForm.create_user);
                formData.append('file', fileList.raw);
                formData.append('create_time', this.afterFileUpload(fileList));
                formData.append('type', fileList.raw.type);
                formData.append('archive', this.route_path[1]);
                postUpload(formData).then(response => {
                    this.enclosureForm.file = response.data.filepath;
                    this.enclosureForm.ticket = this.ticket_id;
                    postTicketenclosure(this.enclosureForm);
                    setTimeout(this.EnclosureData, 1000);
                    if (response.statusText = 'ok') {
                        this.$message({
                            type: 'success',
                            message: '恭喜你，上传成功'
                        });
                    }
                }).catch(error => {
                    this.$message.error('上传失败');
                    this.$refs.upload.clearFiles();
                    console.log(error);
                });
            },
            afterFileUpload(fileList){
                let date = new Date(fileList.row.uid);
                let Y = date.getFullYear().toString();
                let M = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1);
                let D = date.getDate();
                let h = date.getHours();
                let m = date.getMinutes();
                let s = date.getSeconds();
                let ctime = Y + M + D + h + m + s;
                return ctime
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