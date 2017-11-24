<template>
    <div>
        <div class="host-select">
            <el-transfer
                    v-model="value"
                    filterable
                    :titles="['未选择', '已选择']"
                    :button-texts="['滚回来', '滚过去']"
                    :footer-format="{noChecked: '${total}',hasChecked: '${checked}/${total}'}"
                    @change="handleChange"
                    :data="allhost">
                <el-button type="info" class="transfer-footer" slot="left-footer" size="small" @click="hostData">重置数据</el-button>
            </el-transfer>
        </div>
    </div>
</template>

<script>
    import {getHostList} from 'api/asset';
    export default {
        props: ['selecthost'],
        data() {
            return {
                allhost: [],
                value: this.selecthost,
                changedata: false
            };
        },

        created() {
            this.hostData();
        },

        methods: {
            hostData() {
                this.allhost = [];
                this.value = this.selecthost;
                const parms = {
                    status: "used"
                };
                getHostList(parms).then(response => {
                    const results = response.data.results;
                    for (var i = 0, len = results.length; i < len; i++) {
                        this.allhost.push({
                            key: results[i].hostname,
                        });
                    }
                });
            },
            handleChange(value, direction, movedKeys) {
                this.$emit('gethosts', value);
            }
        }
    };
</script>

<style>
    .transfer-footer {
        margin-left: 20px;
        padding: 6px 5px;
    }
</style>