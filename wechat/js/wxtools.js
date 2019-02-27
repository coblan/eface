import {wx_jsapi_ready} from './wxtools/init_jsapi'
var wxtool={
    is_weixin:function () {
        var ua = navigator.userAgent.toLowerCase();
        if (ua.match(/MicroMessenger/i) == "micromessenger") {
            return true;
        } else {
            return false;
        }
    },
    show_pay_confirm:function(success,notsuccess){
        var winclose = cfg.pop_small('com-wechat-confirm-win',{},function(resp){
            if(resp=='pay:ok'){
                success()
            }else{
                notsuccess()
            }
            winclose()
        })
    },
    jsapi_ready:wx_jsapi_ready,
}

window.wxtool=wxtool