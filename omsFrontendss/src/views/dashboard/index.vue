<template>
    <div class="dashboard-editor-container">
        <el-row class="btn-group">
            <el-col :span="4" class='text-center'>
                <router-link class="pan-btn violet-btn" to="/components/index">Components</router-link>
            </el-col>
            <el-col :span="4" class='text-center'>
                <router-link class="pan-btn blue-btn" to="/charts/index">Charts</router-link>
            </el-col>
            <el-col :span="4" class='text-center'>
                <router-link class="pan-btn pink-btn" to="/excel/download">Excel</router-link>
            </el-col>
            <el-col :span="4" class='text-center'>
                <router-link class="pan-btn green-btn" to="/example/table/table">Table</router-link>
            </el-col>
            <el-col :span="4" class='text-center'>
                <router-link class="pan-btn tiffany-btn" to="/example/form/edit">Form</router-link>
            </el-col>
            <el-col :span="4" class='text-center'>
                <router-link class="pan-btn yellow-btn" to="/example/form/edit">Theme</router-link>
            </el-col>
        </el-row>

        <el-row>
            <el-col :span="6">
                <el-card class="box-card">
                    <div slot="header" class="box-card-header">
                        <p>Admin</p>
                        <p>超级管理员</p>
                        <p>性别：不详</p>
                    </div>
                    <div class="info-item">
                    </div>
                    <div class="info-item">
                    </div>
                </el-card>
            </el-col>

            <el-col :span="8">
                <pie-chart></pie-chart>
            </el-col>

            <el-col :span="10">
                <bar-chart></bar-chart>
            </el-col>
        </el-row>

        <el-row :gutter="20">
            <el-col :span="15">
                <line-chart></line-chart>
            </el-col>
            <el-col :span="9">
                <todo-list></todo-list>
            </el-col>
        </el-row>

    </div>
</template>

<script>
    import pieChart from './pieChart';
    import barChart from './barChart';
    import lineChart from './lineChart';
    import countTo from 'vue-count-to';
    import todoList from 'components/TodoList';
    export default {
        name: 'dashboard',
        components: {countTo, pieChart, lineChart, barChart, todoList},
        data() {
            return {
                }
            }
    }
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    .dashboard-editor-container {
        margin: 30px;
        .btn-group {
            margin-bottom: 60px;
        }
        .box-card-header {
            position: relative;
            height: 160px;
        }
        .info-item {
            display: inline-block;
            margin-top: 10px;
            font-size: 14px;
            &:last-of-type {
                margin-left: 15px;
            }
        }
    }
</style>
