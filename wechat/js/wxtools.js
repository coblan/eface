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
    jsapi_pay:function(url){
        return new Promise((resolve,reject)=>{
            if (typeof WeixinJSBridge == "undefined"){
                if( document.addEventListener ){
                    document.addEventListener('WeixinJSBridgeReady', resolve, false);
                }else if (document.attachEvent){
                    document.attachEvent('WeixinJSBridgeReady', resolve);
                    document.attachEvent('onWeixinJSBridgeReady', resolve);
                }
            }else{
                resolve();
            }
        }).then(()=>{
             return ex.get(url)
        }).then((resp)=>{
            var args = resp.order_args
            return new Promise((resolve,reject)=>{
                    WeixinJSBridge.invoke(
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
                                resolve({success:true})
                            }else{
                                if(res.err_msg =='get_brand_wcpay_request:cancel'){
                                    cfg.showError('用户取消支付')
                                    //resolve({success:false,msg:'用户取消支付'})
                                }else{
                                    cfg.showError(JSON.stringify(res))
                                    //resolve({success:false,msg:JSON.stringify(res)})
                                }
                            }
                        });
            })

        })
    }
}

window.wxtool=wxtool