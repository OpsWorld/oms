<template xmlns="http://www.w3.org/1999/html">
    <div class="addticket">
        <el-card>
            <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
                <el-form-item label="标题" prop="title">
                    <el-input v-model="ruleForm.title"></el-input>
                </el-form-item>
                <el-form-item label="工单类型" prop="type">
                    <el-select v-model="ruleForm.type" placeholder="请选择工单类型">
                        <el-option v-for="item in tickettypes" :key="item.name" :value="item.name"></el-option>
                    </el-select>
                    <el-tooltip class="item" effect="dark" content="添加新工单类型" placement="right">
                        <el-button type="success" icon="plus" @click="addForm=true"></el-button>
                    </el-tooltip>
                </el-form-item>
                <el-form-item label="工单内容" prop="content">
                    <mavon-editor default_open='edit' v-model="ruleForm.content" code_style="monokai"
                                  :toolbars="toolbars" @imgAdd="imgAdd" ref="md"></mavon-editor>
                </el-form-item>
                <el-form-item label="工单等级" prop="level">
                    <el-rate
                            v-model="ruleForm.level"
                            :colors="['#99A9BF', '#F7BA2A', '#ff1425']"
                            show-text
                            :texts="['E', 'D', 'C', 'B', 'A']">
                    </el-rate>
                    <div>
                        <hr class="heng"/>
                        <el-upload
                                class="upload-demo"
                                ref="upload"
                                action="https://jsonplaceholder.typicode.com/posts/"
                                :on-success="handleSuccess"
                                :file-list="fileList"
                                :disabled="count>0?true:false">
                            <el-button slot="trigger" size="small" type="primary" :disabled="count>0?true:false">
                                上传文件
                            </el-button>
                            (可以不用上传)
                            <div slot="tip" class="el-upload__tip">
                                <p>上传文件不超过500kb，<a style="color: red">添加工单页面只能上传1个文件</a></p>
                            </div>
                        </el-upload>
                        <hr class="heng"/>
                    </div>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="postForm('ruleForm')">提交</el-button>
                    <el-button type="danger" @click="resetForm('ruleForm')">清空</el-button>
                </el-form-item>
            </el-form>
            <el-dialog :visible.sync="addForm">
                <add-group @formdata="addGroupSubmit" @DialogStatus="getDialogStatus"></add-group>
            </el-dialog>
        </el-card>
    </div>
</template>
<script>
    import {postWorkticket, getTickettype, postTickettype, postTicketenclosure} from 'api/workticket'
    import ElButton from "../../../node_modules/element-ui/packages/button/src/button";
    import addGroup from '../components/addgroup.vue'
    import {postUpload} from 'api/tool'

    export default {
        components: {ElButton, addGroup},

        data() {
            return {
                route_path: this.$route.path.split('/'),
                ruleForm: {
                    title: '',
                    type: '',
                    content: '',
                    create_user: localStorage.getItem('username'),
                    level: null,
                    action_user: '',
                    create_group: ''
                },
                rules: {
                    title: [
                        {required: true, message: '请输入工单标题', trigger: 'blur'},
                    ],
                    type: [
                        {required: true, message: '请选择工单类型', trigger: 'change'}
                    ],
                    content: [
                        {required: true, message: '请输入工单内容', trigger: 'blur'}
                    ],
                    level: [
                        {required: true, type: 'number', message: '请确认工单等级', trigger: 'blur'},
                    ],
                },
                tickettypes: [],
                addForm: false,
                fileList: [],
                count: 0,
                enclosureFile: null,
                enclosureForm: {
                    ticket: '',
                    create_user: localStorage.getItem('username'),
                    file: '',
                    create_group: ''
                },
                toolbars: {
                    preview: true, // 预览
                    bold: true, // 粗体
                    italic: true, // 斜体
                    header: true, // 标题
                    underline: true, // 下划线
                    strikethrough: true, // 中划线
                    ol: true, // 有序列表
                    fullscreen: true, // 全屏编辑
                    help: true,
                },
                img_file: {},
                formDataList: [],
            };
        },

        created() {
            this.getTickettypes();
        },
        methods: {
            postForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        postWorkticket(this.ruleForm).then(response => {
                            if (response.statusText = 'ok') {
                                this.$message({
                                    type: 'success',
                                    message: '恭喜你，新建成功'
                                });
                            }
                            if (this.enclosureFile) {
                                this.enclosureForm.file = this.enclosureFile;
                                this.enclosureForm.ticket = response.data.id;
                                postTicketenclosure(this.enclosureForm);
                            }
                            let ticket_id = response.data.id;
                            this.$router.push('/worktickets/editworkticket/' + ticket_id);
                        });
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            getDialogStatus(data) {
                this.addForm = data;
            },
            resetForm(formName) {
                this.$refs[formName].resetFields();
            },
            getTickettypes() {
                getTickettype().then(response => {
                    this.tickettypes = response.data.results;
                })
            },
            addGroupSubmit(formdata) {
                postTickettype(formdata).then(response => {
                    this.$message({
                        message: '恭喜你，添加成功',
                        type: 'success'
                    });
                    setTimeout(this.getTickettypes, 1000);
                    this.addForm = false
                }).catch(error => {
                    this.$message.error('添加失败');
                    console.log(error);
                });
            },
            handleSuccess(file, fileList) {
                let formData = this.afterFileUpload(fileList);
                postUpload(formData).then(response => {
                    this.enclosureFile = response.data.filepath;
                    if (response.statusText = 'ok') {
                        this.count += 1;
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
            imgAdd(pos, file){
                var md = this.$refs.md;
                let formData = new FormData();
                formData.append('username', this.enclosureForm.create_user);
                formData.append('file', file);
                formData.append('create_time', this.afterFileUpload(file));
                formData.append('type', file.type);
                formData.append('archive', this.route_path[1]);
                postUpload(formData).then(response => {
                    md.$imglst2Url([[pos, response.data.file]]);
                });
            },
//            imgDel(pos){
//                delete this.img_file[pos];
//            },
//            uploadimg(){
//                let formData = new FormData();
//                for (var _img in this.img_file) {
//                    formData.append('username', this.enclosureForm.create_user);
//                    formData.append('file', this.img_file[_img]);
//                    formData.append('create_time', this.afterFileUpload(this.img_file[_img]));
//                    formData.append('type', this.img_file[_img].type);
//                    formData.append('archive', this.route_path[1]);
//                    postUpload(formData).then(response => {
//                        console.log(response.data.file)
//                    });
//                }
//            },
            afterFileUpload(file){
                let date = new Date(file.lastModified);
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
    .heng {
        margin: 20px 0;
        height: 1px;
        border: 0px;
        background-color: rgba(174, 127, 255, 0.38);
        color: #29e11c;
    }

    .addticket {
        margin: 50px;
        width: 800px;
    }
</style>