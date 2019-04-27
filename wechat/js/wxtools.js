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
    jsapi_pay:function(url,callback){
        cfg.show_load()
        ex.get(url,function(resp){
            var args = resp.order_args
            cfg.hide_load()
            function onBridgeReady(){
                WeixinJSBridge.invoke(
                    //'getBrandWCPayRequest', {
                    //    "appId":"wx2421b1c4370ec43b",     //公众号名称，由商户传入
                    //    "timeStamp":"1395712654",         //时间戳，自1970年以来的秒数
                    //    "nonceStr":"e61463f8efa94090b1f366cccfbbb444", //随机串
                    //    "package":"prepay_id=u802345jgfjsdfgsdg888",
                    //    "signType":"MD5",         //微信签名方式：
                    //    "paySign":"70EA570631E4BB79628FBCA90534C63FF7FADD89" //微信签名
                    //},
                    'getBrandWCPayRequest',{
                        "appId":args.appId,     //公众号名称，由商户传入
                        "timeStamp":args.timeStamp+'',         //时间戳，自1970年以来的秒数
                        "nonceStr":args.nonceStr, //随机串
                        "package":args.package,
                        "signType":args.signType,         //微信签名方式：
                        "paySign":args.paySign //微信签名
                    },
                    function(res){
                        if(res.err_msg == "get_brand_wcpay_request:ok" ){
                            // 使用以上方式判断前端返回,微信团队郑重提示：
                            //res.err_msg将在用户支付成功后返回ok，但并不保证它绝对可靠。
                            callback()
                        }else{
                            if(res.err_msg =='get_brand_wcpay_request:cancel'){
                                cfg.showError('用户取消支付！')
                            }else{
                                //cfg.showError(res.err_code + "--" + res.err_desc + "--" + res.err_msg);
                                cfg.showError(res.err_desc);
                            }
                        }
                    });
            }
            if (typeof WeixinJSBridge == "undefined"){
                if( document.addEventListener ){
                    document.addEventListener('WeixinJSBridgeReady', onBridgeReady, false);
                }else if (document.attachEvent){
                    document.attachEvent('WeixinJSBridgeReady', onBridgeReady);
                    document.attachEvent('onWeixinJSBridgeReady', onBridgeReady);
                }
            }else{
                onBridgeReady();
            }

        })
    }
}

window.wxtool=wxtool