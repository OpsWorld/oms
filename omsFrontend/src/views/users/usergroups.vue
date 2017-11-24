<template>
    <div>
        <el-card>
            <div class="head-lavel">
                <div class="table-button">
                    <el-button type="info" icon="plus" @click="addGroup=true">新建用户组</el-button>
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
                    <el-table-column prop='name' label='组名' sortable='custom'></el-table-column>
                    <el-table-column prop='desc' label='描述' sortable='custom'></el-table-column>
                    <el-table-column label="操作">
                        <template scope="scope">
                            <el-button @click="showGroup(scope.row.name)" type="success" size="small">查看</el-button>
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
            <add-group @formdata="addGroupSubmit"></add-group>
        </el-dialog>
        <el-dialog :visible.sync="viewGroup" size="tiny">
            <view-group :groupName="groupName"></view-group>
        </el-dialog>
    </div>
</template>

<script>
    import {getGroupList, postGroup, deleteGroup} from 'api/user';
    import {LIMIT} from '@/config'
    import addGroup from '../components/addgroup.vue'
    import viewGroup from './viewgroup.vue'

    export default {
        components: {addGroup, viewGroup},
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
                viewGroup: false,
                groupName: ''
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
                getGroupList(parms).then(response => {
                    this.tableData = response.data.results;
                    this.tabletotal = response.data.count;
                })
            },

            addGroupSubmit(formdata) {
                postGroup(formdata).then(response => {
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
            },
            deleteGroup(id){
                deleteGroup(id).then(response => {
                    this.$message({
                        message: '恭喜你，删除成功',
                        type: 'success'
                    });
                    this.fetchData();
                }).catch(error => {
                    this.$message.error('删除失败');
                    console.log(error);
                });
            },
            showGroup(groupName){
                this.viewGroup = true;
                this.groupName = groupName
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