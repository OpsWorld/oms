<template>
    <div>
        <button @click="uploadimg">upload</button>
        <mavon-editor @imgAdd="imgAdd" @imgDel="imgDel"></mavon-editor>
    </div>
</template>

<script>
    export default {
        data(){
            return {
                img_file: {}
            }
        },
        methods: {
            imgAdd(pos, $file){
                this.img_file[pos] = $file;
            },
            imgDel(pos){
                delete this.img_file[pos];
            },
            uploadimg(e){
                console.log(this.img_file);
                var formdata = new FormData();
                for (var _img in this.img_file) {
                    formdata.append(_img, this.img_file[_img]);
                }
                axios({
                    url: 'http://127.0.0.1/index.php',
                    method: 'post',
                    data: formdata,
                    headers: {'Content-Type': 'multipart/form-data'},
                }).then((res) => {
                    console.log(res);
                })
            }
        }
    }
</script>

<style lang="scss">
    #app {
        width: 100vw;
        height: 100vh;
    }
</style>