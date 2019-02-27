export function wx_jsapi_ready(api_list){
    return new Promise(function(resolve,reject){
         new Promise(function(resolve1,reject1){
            var post_data={
                url:location.href
            }
            ex.director_call('wx_jssdk_config_parameter',post_data,function(resp){
                ex.load_js('https://res.wx.qq.com/open/js/jweixin-1.4.0.js',function(){
                    resolve1(resp)
                })
            })
        }).then(function(jssdk_config){

                wx.config({
                    debug: false, // 开启调试模式,调用的所有api的返回值会在客户端alert出来，若要查看传入的参数，可以在pc端打开，参数信息会通过log打出，仅在pc端时才会打印。
                    appId: jssdk_config.appId, // 必填，公众号的唯一标识
                    timestamp: jssdk_config.timestamp, // 必填，生成签名的时间戳
                    nonceStr: jssdk_config.noncestr, // 必填，生成签名的随机串
                    signature: jssdk_config.signature,// 必填，签名
                    jsApiList: api_list // 必填，需要使用的JS接口列表
                });
                wx.ready(function(){
                    resolve()
                })
            })
    })

}
