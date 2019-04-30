
from django.core.urlresolvers import reverse
import hashlib
import requests
import xmltodict
import random
import time
from django.conf import settings
from .page_jsapi import WePayJsapi
proxy = getattr(settings,'INTERNET_PROXY',{})

class WePayH5api(WePayJsapi):
    """
    生成订单
    ==========
    make_order函数，生成订单
    
    为了引入自定义逻辑，重载:
        def order_create(self,wxorder)
    
    响应微信服务器
    ==============
    reply函数，响应微信服务器
    
    为了自定义逻辑，重载:
        def order_confirmed(self,wxorder):
    """
    trade_type = 'MWEB'
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
            'out_trade_no':'wxorder_%s'% wxorder.pk,
            'fee_type':'CNY',
            'total_fee' : wxorder.total_fee,
            'spbill_create_ip' : self.ip,
            'notify_url':self.reply_full_url,
            'trade_type':wxorder.trade_type,
            'scene_info':'{"h5_info": {"type":"Wap","wap_url": "https://uacar.com.cn","wap_name": "企鹅洗车"}}',
          
        }
        return param  

    