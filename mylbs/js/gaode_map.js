var gaode_map=


Vue.component('com-gaode-map',function(resolve,reject){

    //ex.load_css(cfg.js_lib.gaode_css)
    ex.load_js(js_config.js_lib.gaode).
    then(function(){
        var count=0
        function gen_gaode_component(){
            console.log('load gaode '+count)
            count+=1
            if(window.AMap){
                resolve(gaode_map)
            }else if(count<20){
                setTimeout(gen_gaode_component,300)
            }else{
                throw 'load gaode and generate AMap object time out'
            }
        }
        gen_gaode_component()
    })
    //ex.load_js(cfg.js_lib.gaode_js,function(){
    //    ex.load_js(cfg.js_lib.gaode_addtoolbar_js,function(){
    //        resolve(map_com)
    //    })
    //})

})