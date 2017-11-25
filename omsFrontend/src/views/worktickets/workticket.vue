<template>
    <div>
        <el-card>
            <div class="head-lavel">
                <div class="table-button">
                    <router-link :to="'addworkticket'">
                        <el-button type="info" icon="plus">新建工单</el-button>
                    </router-link>
                </div>
                <div class="table-search">
                    <el-input
                            placeholder="搜索 ..."
                            v-model="searchdata"
                            @keyup.enter.native="searchClick">
                        <i class="el-icon-search el-input__icon" slot="suffix" @click="searchClick"></i>
                    </el-input>
                </div>
            </div>
            <div>
                <el-table :data="tableData" border style="width: 100%">
                    <el-table-column type="expand">
                        <template slot-scope="props">
                            <step></step>
                        </template>
                    </el-table-column>
                    <el-table-column prop='title' label='标题'>
                        <template scope="scope">
                            <div slot="reference" style="text-align: center; color: rgb(52,91,225)">
                                <router-link :to="'editworkticket/'+scope.row.id">{{scope.row.title}}</router-link>
                            </div>
                        </template>
                    </el-table-column>
                    <el-table-column prop='type' label='工单类型'></el-table-column>
                    <el-table-column prop='create_user' label='工单创建人'></el-table-column>
                    <el-table-column prop='level' label='工单等级' sortable>
                        <template scope="scope">
                            <div slot="reference" class="name-wrapper" style="text-align: center">
                                <el-tag :type="LEVEL[scope.row.level].color">
                                    {{LEVEL[scope.row.level].type}}
                                </el-tag>
                            </div>
                        </template>
                    </el-table-column>
                    <el-table-column prop='ticket_status' label='工单状态' sortable>
                        <template scope="scope">
                            <div slot="reference" class="name-wrapper" style="text-align: center">
                                <el-tag :color="TICKET_STATUS[scope.row.ticket_status].color">
                                    {{TICKET_STATUS[scope.row.ticket_status].type}}
                                </el-tag>
                            </div>
                        </template>
                    </el-table-column>
                    <el-table-column prop='action_user' label='当前处理人'></el-table-column>
                    <el-table-column label="操作">
                        <template scope="scope">
                            <el-button type="success" size="small">接收</el-button>
                            <el-button type="danger" size="small">关闭</el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
            <div class="table-footer">
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
    </div>
</template>

<script>
    import {getWorkticket, postWorkticket} from 'api/workticket'
    import {LIMIT} from '@/config'
    import addWorkticket from './addworkticket.vue'
    import Step from '../components/Steps.vue'

    export default {
        components: {addWorkticket, Step},
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
                rowdata: {},
                TICKET_STATUS: {
                    '0': {"type": "未接收", "color": "#37474F"},
                    '1': {"type": "正在处理", "color": "#cacb1f"},
                    '2': {"type": "未解决关闭问题", "color": "#f06292"},
                    '3': {"type": "已解决关闭问题", "color": "#17e16c"},
                },
                LEVEL: {
                    '1': {"type": 'A', "color": "danger"},
                    '2': {"type": 'B', "color": "warning"},
                    '3': {"type": 'C', "color": "success"},
                    '4': {"type": 'D', "color": "info"},
                    '5': {"type": 'E', "color": ""},
                },
            }
        },

        created() {
            this.fetchData();
        },

        methods: {
            fetchData() {
                const id = null;
                const parms = {
                    limit: this.limit,
                    offset: this.offset,
                    title__contains: this.searchdata
                };
                getWorkticket(id, parms).then(response => {
                    this.tableData = response.data.results;
                    this.tabletotal = response.data.count;
                })
            },
            handleCreate() {
                this.reseRowdata();
                this.addForm = true;
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