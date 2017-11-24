<template>
    <div>
        <el-card>
            <div class="head-lavel">
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
                <el-table :data="tableData" border style="width: 100%">
                    <el-table-column prop='username' label='用户名' sortable='custom'></el-table-column>
                    <el-table-column prop='name' label='姓名' sortable='custom'></el-table-column>
                    <el-table-column prop='roles' label='角色' sortable='custom'></el-table-column>
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
    </div>
</template>

<script>
    import {getUserList} from 'api/user'
    import {LIMIT} from '@/config'

    export default {
        props: ['groupName'],
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
                rowdata: {}
            }
        },

        created() {
            this.fetchData();
        },

        methods: {
            fetchData() {
                const parms = {
                    limit: this.limit,
                    offset: this.offset,
                    group__name: this.groupName,
                    username__contains: this.searchdata
                };
                getUserList(parms).then(response => {
                    this.tableData = response.data.results;
                    this.tabletotal = response.data.count;
                })
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