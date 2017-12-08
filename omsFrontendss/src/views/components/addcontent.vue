<template>
    <mavon-editor :default_open='rawdata' v-model="content" code_style="monokai"
                  :toolbars="toolbars" @imgAdd="imgAdd" ref="md"></mavon-editor>
</template>
<script>
    import {postUpload} from 'api/tool'
    export default {
        props: ['rawdata'],
        data() {
            return {
                content: '',
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
        methods: {
            imgAdd(pos, file){
                var md = this.$refs.md;
                let formData = new FormData();
                formData.append('username', localStorage.getItem('username'));
                formData.append('file', file);
                formData.append('create_time', this.afterFileUpload(file));
                formData.append('type', file.type);
                formData.append('archive', this.route_path[1]);
                postUpload(formData).then(response => {
                    md.$imglst2Url([[pos, response.data.file]]);
                });
            },
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