// import * as gaode_map from './gaode_map.js'

import location from './field_editor/location.vue'
//import location_select from './field_editor/location_select.vue'

Vue.component('com-field-location',location)

//Vue.component('com-location-select', function (resolve, reject) {
//   ex.load_js(js_config.js_lib.gaode).then(()=>{
//       resolve(location_select)
//   })
//})

import gaode_map from './gaode_map.vue'
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