from .page_jsapi import WePayJsapi,WePayReplay
from helpers.director.shortcut import director_view
from helpers.director.decorator import need_login
from django.http import HttpResponse
import json
import time

class WePayAppapi(WePayJsapi):
    trade_type='APP'

    def get_context(self):
        """
        这里是总函数，出口为dict，让dapi去处理所有事情。app时，用户可以不用登录，通过out_trade_no定位订单。
        """
        dc = self.make_order(self.request)
        return dc['data']
        #dc['success'] = True
        #return HttpResponse(json.dumps(dc,ensure_ascii=False),content_type="application/json") 
    
    def getOpenid(self):
        return ''
    
    def make_param(self):
        """
        微信统一下单
        
        params = {
            'appid' : setting.WXPAY_APPID,
            'mch_id' : setting.WXPAY_MACHID,
            'device_info' : 'WEB',
            'nonce_str' : str(int(time.time())),
            'body' : self.meal['meal_name'],
            'detail': self.meal['meal_desc'],
            'out_trade_no' : self.orderno,
            'fee_type' : 'CNY',
            'total_fee' : int(float(self.meal['meal_nowprice'])*100),
            'spbill_create_ip' : (self.request_ip and self.request_ip) or '127.0.0.1',
            'notify_url' : setting.WXPAY_NOTIFY,
            'trade_type' : 'APP'
        }
        """ 
        wxorder = self.setup_model()
        param={
            'appid':self.APPID,
            'mch_id':self.MACHID,
            'device_info' : 'WEB',
            'nonce_str':self.get_nonce_str(),
            'body':wxorder.body,
            'detail':wxorder.detail,
            'out_trade_no':wxorder.no,
            'fee_type':'CNY',
            'total_fee' : wxorder.total_fee,
            'spbill_create_ip' : self.ip,
            'notify_url':self.reply_full_url,
            'trade_type':wxorder.trade_type,
        }
        return param  
    
    def fetch_order_args(self, resp):
        """
        从微信返回参数中提取 参数给前端，jsapi用
        """
        if resp.get('return_code')!='SUCCESS':
            ret={
                'msg':resp.get('return_msg'),
                'order_args':{}
                 }            
        else:
            order_args={
                'appid' : self.APPID,
                'partnerid':self.MACHID,
                'prepayid':resp.get('prepay_id'),
                'package' : 'Sign=WXPay',
                'noncestr' : self.get_nonce_str(),
                'timestamp' : str(int(time.time())),
            }
            order_args['sign']=self.params_sign(order_args)
            ret={
                'data': order_args
            }    
        return ret
    
    
