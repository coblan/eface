<template>
    <div :class="ctx.class" >
    </div>
</template>
<script>
    export default {
        props:['ctx'],
        data(){
            return {

            }
        },
        mounted(){

            if(this.ctx.css){
                ex.append_css(this.ctx.css)
            }

//            setTimeout(()=>{
                this.map = new AMap.Map(this.$el, {
                    resizeEnable: true,
                    center: [104.061615,30.666313],
                    zoom: 11
                });
    //            ex.load_js("https://a.amap.com/jsapi_demos/static/resource/heatmapData.js").then(()=>{
    //                debugger
    //                this.setData(heatmapData)
    //            })

                if(this.ctx.mounted_express){
                    ex.eval(this.ctx.mounted_express,{vc:this,head:this.ctx})
                }
//            },50)


        },
        methods:{
            setData(heatmapData){


                //详细的参数,可以查看heatmap.js的文档 http://www.patrick-wied.at/static/heatmapjs/docs.html
                //参数说明如下:
                /* visible 热力图是否显示,默认为true
                 * opacity 热力图的透明度,分别对应heatmap.js的minOpacity和maxOpacity
                 * radius 势力图的每个点的半径大小
                 * gradient  {JSON} 热力图的渐变区间 . gradient如下所示
                 *	{
                 .2:'rgb(0, 255, 255)',
                 .5:'rgb(0, 110, 255)',
                 .8:'rgb(100, 0, 255)'
                 }
                 其中 key 表示插值的位置, 0-1
                 value 为颜色值
                 */
                this.map.plugin(["AMap.Heatmap"],  ()=> {
                    //初始化heatmap对象
                    this.heatmap = new AMap.Heatmap(this.map, {
                        radius: 12, //给定半径
                        opacity: [0.1, 0.8],
                    /*,
                     gradient:{
                     0.5: 'blue',
                     0.65: 'rgb(117,211,248)',
                     0.7: 'rgb(0, 255, 0)',
                     0.9: '#ffea00',
                     1.0: 'red'
                     }
                     */
                    });
                    /*
                     var heatmapData = [{
                     "lng": 116.191031,
                     "lat": 39.988585,
                     "count": 10
                     },]
                    * */
                    this.heatmap.setDataSet({
                        data: heatmapData,
//                        max: 100
                    });
//                    this.heatmap.show()
                });
            }
        }
    }
</script>
<style scoped lang="scss">
/*#container{*/
    /*height: 500px;*/
/*}*/
</style>