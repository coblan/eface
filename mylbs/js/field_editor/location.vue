<template>
    <div :class="['com-field-location',head.class]">
        <span class="readonly-info" v-if='head.readonly' v-text='row[head.name]'></span>
        <div  v-else  class="form-inline">
            <el-input v-model="row[head.name]" size="small" :placeholder="head.placeholder"
                      :id="'id_'+head.name" :name="head.name"
                      :maxlength="head.maxlength">
                <template slot="prepend" >
                    <span  v-if="head.prefix" v-html="head.prefix"></span>
                </template>
                <template slot="append">
                    <span  v-if="head.suffix" v-html="head.suffix"></span>
                </template>
            </el-input>
            <div class="small-text">
                点击"
                <a href="https://lbs.qq.com/getPoint/" target="_blank">腾讯坐标拾取器</a>"获取坐标
            </div>
            <!--<div @click="open_select">打开拾取</div>-->
        </div>
    </div>
</template>
<script>
    export default {
        props:['row','head'],
        mounted(){
            if(this.head.css){
                ex.append_css(this.head.css)
            }
            var mounted_express = this.head.mounted_express || this.head.on_mounted
            if(mounted_express){
                ex.eval(mounted_express,{vc:this})
            }
        },
        methods:{
//            open_select(){
//                cfg.pop_vue_com('com-location-select',{})
//            }
        }
    }
</script>
<style scoped lang="scss">
    .small-text{
        margin: 5px 0;
        font-size: 50%;
        color: gray;
    }
</style>