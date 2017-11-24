<template>
    <div>
        <el-card>
            <div class="head-lavel">
                <div class="table-button">
                    <el-button type="info" icon="plus" @click="addGroup=true">新建角色对象</el-button>
                </div>
                <div class="table-search">
                    <el-input
                            placeholder="搜索 ..."
                            icon="search"
                            v-model="searchdata"
                            @keyup.enter.native="searchClick"
                            :on-icon-click="searchClick">
                    </el-input>
                </div>
            </div>
            <div>
                <el-table :data='tableData' border style="width: 100%">
                    <el-table-column prop='name' label='角色' sortable></el-table-column>
                    <el-table-column prop='cnname' label='中文名'></el-table-column>
                    <el-table-column prop='desc' label='描述'></el-table-column>
                    <el-table-column label="操作">
                        <template scope="scope">
                            <el-button @click="deleteGroup(scope.row.id)" type="danger" size="small">删除</el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
            <div class="table-pagination">
                <el-pagination
                        small
                        @size-change="handleSizeChange"
                        @current-change="handleCurrentChange"
                        :current-page.sync="currentPage"
                        :page-sizes="pagesize"
                        :page-size="limit"
                        layout="prev, pager, next, sizes"
                        :total="tabletotal">
                </el-pagination>
            </div>
        </el-card>
        <el-dialog :visible.sync="addGroup" size="tiny">
            <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
                <el-form-item label="角色名" prop="name">
                    <el-input v-model="ruleForm.name"></el-input>
                </el-form-item>
                <el-form-item label="中文名" prop="cnname">
                    <el-input v-model="ruleForm.cnname"></el-input>
                </el-form-item>
                <el-form-item label="描述" prop="desc">
                    <el-input v-model="ruleForm.desc"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="addGroupSubmit('ruleForm')">立即创建</el-button>
                    <el-button @click="resetForm('ruleForm')">重置</el-button>
                </el-form-item>
            </el-form>
        </el-dialog>
    </div>
</template>

<script>
    import {getRoleList, postRole, deleteRole} from 'api/user';
    import {LIMIT} from '@/config'

    export default {
        components: {},
        data() {
            return {
                tableData: [],
                tabletotal: 0,
                searchdata: '',
                currentPage: 1,
                limit: LIMIT,
                offset: '',
                pagesize: [10, 25, 50, 100],
                addGroup: false,
                ruleForm: {
                    name: '',
                    cnname: '',
                    desc: ''
                },
                rules: {
                    name: [
                        {required: true, message: '请输入一个风骚的角色', trigger: 'blur'},
                    ],
                    cnname: [
                        {required: true, message: '请输入一个风骚的角色中文', trigger: 'blur'},
                    ]
                }
            }
        },

        created() {
            this.fetchData();
        },

        methods: {
            /*
             * 获取数据
             */
            fetchData() {
                const parms = {
                    limit: this.limit,
                    offset: this.offset,
                    name__contains: this.searchdata
                };
                getRoleList(parms).then(response => {
                    this.tableData = response.data.results;
                    this.tabletotal = response.data.count;
                })
            },

            addGroupSubmit(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        postRole(this.ruleForm).then(response => {
                            this.$message({
                                message: '恭喜你，添加成功',
                                type: 'success'
                            });
                            this.fetchData();
                            this.addGroup = false
                        }).catch(error => {
                            this.$message.error('添加失败');
                            console.log(error);
                        });
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            deleteGroup(id){
                deleteRole(id).then(response => {
                    this.$message({
                        message: '恭喜你，删除成功',
                        type: 'success'
                    });
                }).catch(error => {
                    this.$message.error('删除失败');
                    console.log(error);
                });
            },
            searchClick() {
                this.fetchData();
            },
            handleSizeChange(val) {
                this.limit = val;
                this.fetchData();
            },
            handleCurrentChange(val) {
                this.offset = val - 1;
                this.fetchData();
            },
            resetForm(formName) {
                this.$refs[formName].resetFields();
            }
        }
    }
</script>

<style lang='scss'>
    .head-lavel {
        padding-bottom: 50px;
    }

    .table-button {
        float: left;
    }

    .table-search {
        float: right;
    }

    .table-pagination {
        padding: 10px 0;
        float: right;
    }
</style>