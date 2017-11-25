<template>
    <div class="steps">
        <div class="doc-header">
            <el-steps :active="1" finish-status="success">
                <el-step title="未接收"></el-step>
                <el-step title="正在处理"></el-step>
                <el-step title="已完成"></el-step>
            </el-steps>
        </div>
    </div>
</template>
<script>
    export default {}
</script>

<style lang='scss'>
    .doc-header {
        background-color: white !important;
    }
</style>

