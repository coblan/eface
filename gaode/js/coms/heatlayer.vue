<template>
    <div :class="ctx.class" style="position: relative">
        <div  class="svg-container">
        </div>
        <div class="info" style="width: 300px;position: absolute;right: 20px;top:10px;background-color: white;">

            <p>当前区域：<span  v-text="crt_name">--</span></p>
            <p>当前值：<span  v-text="crt_data">--</span></p>
        </div>
    </div>

</template>
<script>
    export default {
        props:['ctx'],
        data(){
            return {
                crt_data:0,
                crt_name:'',
            }
        },
        computed:{

        },
        mounted(){

            if(this.ctx.css){
                ex.append_css(this.ctx.css)
            }

//            setTimeout(()=>{

            this.map = new AMap.Map($(this.$el).find('.svg-container')[0], {
//                viewMode: '3D',
//               pitch: 50,
                resizeEnable: true,
//                mapStyle: 'amap://styles/db9efe6a1745ac24b7269b862f359536',
                center: [104.061615,30.666313],
                zoom: 11,

//                mapStyle: 'amap://styles/db9efe6a1745ac24b7269b862f359536',
               // viewMode: '3D',
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
            init(){


            },
            setData(heatdata){
                var self =this
//                var layer = new Loca.GridLayer({
                const layer = new Loca.HexagonLayer({
                    map: this.map,
                    eventSupport: true
                });

                layer.setData(heatdata, {
                    lnglat: 'lnglat',
//                    value: 'count',
                });

                layer.setOptions({
                    unit: 'px',
                    mode: 'mean',  // 聚合模式，可选值: sum(值求和)、max(最大值)、min(最小值)、mean(平均值)、median(中位数)、count(个数)
                    style: {
                        // 网格热力半径，单位：米
                        radius: 8,
                        opacity: 0.6, //[0.8, 0.8],
//                        height: [10000, 50000],
                        // 热力聚合模式，count 为点数量加和

                        // 颜色范围
//                        height: [0, 40000],
//                        color: {
//                            scale: 'quantize',
//                            value:['rgb(255,237,160)', 'rgb(254,217,118)', 'rgb(254,178,76)', 'rgb(253,141,60)', 'rgb(252,78,42)', 'rgb(227,26,28)', 'rgb(189,0,38)', ]
//                        },
                       // color:['#4575b4', '#99d594', '#e6f598', '#ffffbf', '#fee08b', '#fee08b', '#d53e4f'],
//                        color:['#FF0000','#FF9900','#FFFF00','#66CC00','#66FF00','#3300CC','#3366CC','#33CCCC'],
//                        color: [ '#FE2A02','#fc9f02','#cbfa04','#83f902','#1efa5a','#35fabe','#1afcf4','#2d7fff','#3636fc','#8e37fe'].reverse(),
                        color:{
                            scale:'quantize',//'quantile',// 'quantize', Quantile, Quantize
                            value:[  'rgb(255,0,0)','rgba(255, 90, 52, 0.8)','rgba(255, 199, 23, 0.8)','rgb(255,255,0,.8)','rgba(190, 255, 8, 0.8)','rgba(3, 255, 150, 0.6)','rgb(0,255,60,.6)','rgb(0,255,0,.6)','rgb(0,255,0)','rgba(0,50,190,.8)','rgb(0,0,255,.6)','rgba(95, 109, 240, 0.6)',].reverse()
                        },
//                                [
//                            '#f0f9e8',
//                            '#bae4bc',
//                            '#7bccc4',
//                            '#43a2ca',
//                            '#0868ac',
//                        ],

//                        text: {
//                            content: function(v){
//                                debugger;
//                                console.log(v)
//                                return v.value;
//                            },  // 文字内容
//                            direction: 'center',  // 文字方位
////                            offset: [10, -10],  // 偏移大小
//                            fontSize: 12,  // 文字大小
////                            fillColor: '#E67E22',  //文字颜色
//                            strokeColor: "rgba(255,255,255,0.85)",  // 文字描边颜色
//                            strokeWidth: 1,  // 文字描边宽度
//                        }
                    }
                });

//                layer.on('click', function (ev) {
////                    console.log(ev)
//                    alert( ev.value)
//                });
                    // mousemove
                layer.on('click', function (ev) {
                    self.crt_data= parseFloat( ev.value).toFixed(2)  //  Math.round(  ev.value,2 )
                    var bb=[]
                    for(var i=0;i<7&&i<ev.rawData.length;i++){
                        if(i==6){
                            bb.push('...')

                        }else{
                            var item= ev.rawData[i]
                            bb.push(item.name)
                        }

                    }
//                    var bb= ex.map(ev.rawData,item=>{
//                                return item.name
//                            })
                    self.crt_name =bb.join(';')
                });

                layer.render();
            }
        }
    }
</script>
<style scoped lang="scss">
    /*#container{*/
    /*height: 500px;*/
    /*}*/
    .svg-container{
        height: 100%;
        width: 100%;
    }
    .info{
        padding: 5px;
        border: 1px solid #bebebe;
        margin: 1px;
        font-size: 12px;
        /*color: rgba(0,50,190,.8);*/
        /*color: rgba(95, 109, 240, 0.6);*/
        /*color: rgb(0,0,255,.6);*/
        /*color: rgba(190, 255, 8, 0.8);*/
        /*color: #c1f99e;*/
        /*color: #66fad6;*/
        /*color: #00e285;*/
        /*color: #9dd1fc;*/
        /*color: #75b9ff;*/
        /*color: #2868fc;*/


    }
</style>