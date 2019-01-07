var gaode_map={
    props:['option'],
    template:`<div style="width: 100%;height: 100%"></div>`,
    mounted:function(){
        var self=this
        var def_option = {
            resizeEnable: true,
            center: [116.403322, 39.900255],//地图中心点
            zoom: 13, //地图显示的缩放级别
            viewMode:'3D'//使用3D视图
        }
        if (this.option){
            ex.assign(def_option,this.option)
        }
        self. map = new AMap.Map(this.$el, def_option);
        self.map.on('complete', function(){
            // 地图图块加载完成后触发
            self.$emit('install-over',self)
        });

        //if(this.on_init_call){
        //    this.on_init_call()
        //}
        //this._load_finish=true
        //this.map.setMapStyle('amap://styles/light');
    },
    methods:{
        geolocation:function(callback){
            var mapObj = this.map
            this.map.plugin('AMap.Geolocation', function() {
                var geolocation = new AMap.Geolocation({
                    // 是否使用高精度定位，默认：true
                    enableHighAccuracy: true,
                    // 设置定位超时时间，默认：无穷大
                    timeout: 10000,
                    // 定位按钮的停靠位置的偏移量，默认：Pixel(10, 20)
                    buttonOffset: new AMap.Pixel(10, 20),
                    //  定位成功后调整地图视野范围使定位位置及精度范围视野内可见，默认：false
                    zoomToAccuracy: true,
                    //  定位按钮的排放位置,  RB表示右下
                    buttonPosition: 'RT',
                    showButton: true,
                    showCircle:true,
                })
                mapObj.addControl(geolocation);
                geolocation.getCurrentPosition()
                AMap.event.addListener(geolocation, 'complete', onComplete)
                AMap.event.addListener(geolocation, 'error', onError)

                function onComplete (data) {
                    // data是具体的定位信息
                    callback(data)
                }

                function onError (data) {
                    // 定位出错
                    cfg.showError(data.message)
                }
            })
        }
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