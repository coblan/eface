# encoding:utf-8
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
import hashlib
import requests
import xmltodict
import random
import time
from ..base_data import wechat_page_dc
from ..models import TWXOrder
from django.conf import settings
from django.http import JsonResponse,HttpResponse

# proxy = {'https': '127.0.0.1:8087'} 


class WePayJsapi(object):
    """
    在公众号内支付，称为jsapi，
    帮助文件：
    https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_1
    
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

    APPID=settings.WX_APPID
    APPSECRET=settings.WX_APPSECRET
    MACHID=settings.WX_MACHID
    MACHSECERT=settings.WX_MACHSECERT
    
    replay_url= '/wx/wepay_jsapi_reply' #reverse('wepay_relay')
    trade_type='JSAPI'
    def __init__(self,request,engin):
        self.request=request
        self.ip=request.META['REMOTE_ADDR']
        self.openid=request.GET['openid']
    
    def get_context(self):
        dc = self.make_order(self.request)
        return JsonResponse(data=dc)
    
    def setup_model(self):
        """
        从self.request里面获取必要信息，将wxorder的信息填写完整
        @必须添加的项
        wxorder.total_fee = 100 # 单位分
  
        """
        wxorder = TWXOrder.objects.create(trade_type='JSAPI',openid=self.openid)
        wxorder.trade_type = 'JSAPI' 
        wxorder.save()
        return wxorder
    
    def make_order(self,request):
        """
        rt_dc = {'msg': 'OK', 'order_args': {'appId': 'wx7018edf138c754f4', 'package': 'prepay_id=wx09170611946682a346b0be861090939790', 'nonceStr': 'ZZKolfzBSQmTBeo', 'timeStamp': '1547024783', 'signType': 'MD5', 'paySign': 'DC76B4049A521B532C5A6B1630546AEC'}}
        """
        self.reply_full_url=r'%(host)s/%(path)s'%({'host':settings.SELF_DOMAIN,'path':self.replay_url})
        
        params= self.make_param()
        resp =self.unify_order(params)
        rt_dc =self.fetch_order_args(resp)
        return rt_dc
        
    
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
            'openid':wxorder.openid,
        }
        return param    
    def unify_order(self,params):
        if not 'sign' in params.keys():
            params['sign'] = self.params_sign(params)
        postdata='<xml>'
        for k,v in params.items():
            if v:
                postdata+='<{key}>{value}</{key}>\n'.format(key=k,value=v)
        postdata+='</xml>'
        
        resp = requests.post('https://api.mch.weixin.qq.com/pay/unifiedorder',data=postdata.encode('utf-8'))
        
        #ToDo 判断是否是正确的XML，如果是，才继续解析
        resp =xmltodict.parse(resp.content).get('xml')
        return resp
    
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
                'appId' : self.APPID,
                'package' : 'prepay_id=%s'%resp.get('prepay_id'),
                'nonceStr' : self.get_nonce_str(),
                'timeStamp' : str(int(time.time())),
                'signType':'MD5',
            }
            order_args['paySign']=self.params_sign(order_args)
            ret={
                'order_args': order_args
            }    
        return ret
    
    #def order_confirmed(self,wxorder):
        #"""
        #根据 wxorder的信息，填写其他相关的数据表，然后保存这些信息。
        #"""
        #pass
    
    #def reply(self,request):
        #""""""
        #self.request=request
        
        #notify_data = xmltodict.parse( request.body).get('xml')
        #sign=notify_data.pop('sign')
        #local_sign=self.params_sign(notify_data)
        #ret={
            #'return_code':'FAIL',
            #'return_msg':'参数错误或缺少参数！'
        #}
        #if local_sign!=sign:
            #ret={
                #'return_code':'FAIL',
                #'return_msg':'签名失败'
            #}            
        #elif notify_data.get('return_code')=='SUCCESS':
            #self.makesure_order(notify_data)
            #ret={
                #'return_code':'SUCCESS',
                #'return_msg':'OK'
            #}
        #xml_str='<xml>'
        #for k,v in ret.items():
            #xml_str+='<{key}><![CDATA[{value}]]></{key}>'.format(key=k,value=v)
        #xml_str+='</xml>'
        #return xml_str
    

    
    def get_nonce_str(self,length=15):
        a='abcdefghijklmnopqrstuvwxyz'
        a+=a.upper()
        return ''.join([random.choice(a) for i in range(length)])
        
    
    def params_sign(self,params):
        sign_str = ''
        for k,v in sorted(params.items(),key=lambda p:p[0]):
            if v:
                sign_str += '{key}={value}&'.format(key=k,value=v)
        sign_str = sign_str + 'key=' + self.MACHSECERT
        return hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()    
        
class WePayReplay(object):
    need_login=False
    
    APPID=settings.WX_APPID
    APPSECRET=settings.WX_APPSECRET
    MACHID=settings.WX_MACHID
    MACHSECERT=settings.WX_MACHSECERT
    
    def __init__(self, request,engin):
        self.request=request
    
    def makesure_order(self,notify_data):
        """
        需要重载
        """
        pass
    
    def get_context(self):
        notify_data = xmltodict.parse( self.request.body).get('xml')
        sign=notify_data.pop('sign')
        local_sign=self.params_sign(notify_data)
        ret={
            'return_code':'FAIL',
            'return_msg':'参数错误或缺少参数！'
        }
        if local_sign!=sign:
            ret={
                'return_code':'FAIL',
                'return_msg':'签名失败'
            }            
        elif notify_data.get('return_code')=='SUCCESS':
            self.makesure_order(notify_data)
            ret={
                'return_code':'SUCCESS',
                'return_msg':'OK'
            }
        xml_str='<xml>'
        for k,v in ret.items():
            xml_str+='<{key}><![CDATA[{value}]]></{key}>'.format(key=k,value=v)
        xml_str+='</xml>'
        return HttpResponse(xml_str,content_type="text/xml")
    
    def params_sign(self,params):
        sign_str = ''
        for k,v in sorted(params.items(),key=lambda p:p[0]):
            if v:
                sign_str += '{key}={value}&'.format(key=k,value=v)
        sign_str = sign_str + 'key=' + self.MACHSECERT
        return hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()        

wechat_page_dc.update({
    'wepay_jsapi':WePayJsapi,
    'wepay_jsapi_reply':WePayReplay
})