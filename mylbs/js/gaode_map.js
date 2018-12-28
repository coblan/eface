var gaode_map={
    props:['option'],
    template:`<div style="width: 100%;height: 100%"></div>`,
    mounted:function(){
        var def_option = {
            resizeEnable: true,
            center: [116.403322, 39.900255],//地图中心点
            zoom: 13, //地图显示的缩放级别
            viewMode:'3D'//使用3D视图
        }
        if (this.option){
            ex.assign(def_option,this.option)
        }
        var map = new AMap.Map(this.$el, def_option);
        //if(this.on_init_call){
        //    this.on_init_call()
        //}
        //this._load_finish=true
        //this.map.setMapStyle('amap://styles/light');
    }

}


Vue.component('com-gaode-map',function(resolve,reject){

    //ex.load_css(cfg.js_lib.gaode_css)
    ex.load_js(js_config.js_lib.gaode).
    then(function(){
        resolve(gaode_map)
    })
    //ex.load_js(cfg.js_lib.gaode_js,function(){
    //    ex.load_js(cfg.js_lib.gaode_addtoolbar_js,function(){
    //        resolve(map_com)
    //    })
    //})

})