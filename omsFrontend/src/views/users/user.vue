<template>
    <div>
        <el-card>
            <div class="head-lavel">
                <div class="table-button">
                    <el-button type="info" icon="plus" @click="addForm=true">新建用户</el-button>
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
                <el-table :data="tableData" @selection-change="handleSelectionChange" border style="width: 100%">
                    <el-table-column type="selection"></el-table-column>
                    <el-table-column prop='username' label='用户名' sortable>
                        <template scope="scope">
                            <div slot="reference" class="name-wrapper" style="text-align: center">
                                <el-button type="text" @click="handleEdit(scope.row)">{{ scope.row.username }}
                                </el-button>
                            </div>
                        </template>
                    </el-table-column>
                    <el-table-column prop='name' label='姓名' sortable></el-table-column>
                    <el-table-column prop='email' label='邮箱'></el-table-column>
                    <el-table-column prop='group' label='所在组' sortable></el-table-column>
                    <el-table-column prop='roles' label='角色' sortable></el-table-column>
                    <el-table-column prop='avatar' label='头像'>
                        <template scope="scope">
                            <div slot="reference" class="name-wrapper" style="text-align: center">
                                <img :src="'upload' + scope.row.avatar" height="50"/>
                            </div>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
            <div class="table-footer">
                <div class="table-button">
                    <el-button type="danger" icon="delete" :disabled="butstatus" @click="deleteForm">删除用户</el-button>
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
            </div>
        </el-card>
        <el-dialog :visible.sync="addForm" size="small">
            <add-user @DialogStatus="getDialogStatus"></add-user>
        </el-dialog>
        <el-dialog :visible.sync="editForm" size="small">
            <edit-user :rowdata="rowdata" @DialogStatus="getDialogStatus"></edit-user>
        </el-dialog>
    </div>
</template>

<script>
    import {getUserList, deleteUser, getGroupList} from 'api/user'
    import {LIMIT} from '@/config'
    import addUser from './adduser.vue'
    import editUser from './edituser.vue'

    export default {
        components: {addUser, editUser},
        data() {
            return {
                tableData: [],
                tabletotal: 0,
                searchdata: '',
                currentPage: 1,
                limit: LIMIT,
                offset: '',
                pagesize: [10, 25, 50, 100],
                addForm: false,
                editForm: false,
                rowdata: {},
                selectId: [],
                butstatus: true,
            }
        },

        created() {
            this.fetchData();
        },

        methods: {
            fetchData() {
                const parms = {
                    id__gt: 1,   //排除admin用户
                    limit: this.limit,
                    offset: this.offset,
                    username__contains: this.searchdata
                };
                getUserList(parms).then(response => {
                    this.tableData = response.data.results;
                    this.tabletotal = response.data.count;
                })
            },

            getDialogStatus(data) {
                this.editForm = data;
                this.addForm = data;
                this.fetchData();
            },

            handleSelectionChange(val) {
                this.selectId = [];
                for (var i = 0, len = val.length; i < len; i++) {
                    this.selectId.push(val[i].id);
                }
                if (this.selectId.length > 0) {
                    this.butstatus = false
                } else {
                    this.butstatus = true
                }
            },

            handleCreate() {
                this.reseRowdata();
                this.addForm = true;
                setTimeout(this.fetchData, 1000);
            },
            handleEdit(row) {
                this.editForm = true;
                this.rowdata = row;
                setTimeout(this.fetchData, 1000);
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
            deleteForm() {
                for (var i = 0, len = this.selectId.length; i < len; i++) {
                    deleteUser(this.selectId[i]).then(response => {
                        delete this.selectId[i]
                    })
                }
                setTimeout(this.fetchData, 3000);
            },
            reseRowdata() {
                this.rowdata = {
                    username: '',
                    email: '',
                    name: '',
                    is_active: '',
                    group: '',
                    roles: '',
                    password: '',
                }
            },
        }
    }
</script>

<style lang='scss'>
    .head-lavel {
        padding-bottom: 50px;
    }

    .table-button {
        padding: 10px 0;
        float: left;
    }

    .table-search {
        float: right;
        padding: 10px 0;
    }

    .table-pagination {
        padding: 10px 0;
        float: right;
    }
</style>