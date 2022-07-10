import requests
from helpers.func.random_str import get_str
from django.conf import settings
import time
import hashlib
import json
from .base_data import ten_page_dc
from django.http import HttpResponse,JsonResponse
import random
import re
from helpers.director.network.myredis import redis_conn
from helpers.director.shortcut import director_view

import logging
general_log = logging.getLogger('general_log')

@director_view('tencent.phonecode')
def get_phonecode(mobile,**kws):
    phonecode=PhoneCode()
    return phonecode.get_context(mobile)
    



class PhoneCode(object):
    """
    获取验证码
    """
    sdkappid= settings.TENCENT.get('SdkAppId')
    appkey=settings.TENCENT.get('AppKey')
    template_id = settings.TENCENT.get('validate_temp') 
    
    
    def get_context(self,mobile):
        last_minits=5
        code = self.gen_code()
        
        #key =  mobile # get_str()  #  直接用mobile作为key  发送到前端的key
        redis_conn.set('sms:code:%s'%mobile,code,ex=60*5) # 5分钟过期
        
        #mobile = self.request.GET.get('mobile','')
        if not re.search('\d{11}',mobile):
            raise UserWarning('not valid mobile number')
           
        strRand = get_str(10)
        time_now =  int(time.time())

        args = {
            'sdkappid': self.sdkappid,
            'strRand': strRand,
            'appkey': self.appkey,
            "time": time_now,
            'mobile': mobile,
        }
        
        api_url = 'https://yun.tim.qq.com/v5/tlssmssvr/sendsms?sdkappid=%(sdkappid)s&random=%(strRand)s' % args
        
        sig_str = 'appkey=%(appkey)s&random=%(strRand)s&time=%(time)s&mobile=%(mobile)s' % args
        
        hash = hashlib.sha256()
        hash.update(sig_str.encode('utf-8'))
        siged = hash.hexdigest()   
        
        dc = {
            "ext": "",
                "extend": "",
                "params": [
                    code,
                    last_minits
                ],
                "sig": siged,
                #"sign": "测试短信",
                "tel": {
                    "mobile": mobile,
                    "nationcode": "86"
                },
                "time": time_now,
                "tpl_id": self.template_id  
        }
        general_log.info('手机号码：%(mobile)s 发送验证码%(code)s' % {'mobile': mobile, 'code': code,})
        rt = requests.post(api_url, json.dumps(dc) )
        general_log.info( rt.text )
  
        #print(rt.text)
        """ '{"result":0,"errmsg":"OK","ext":"","sid":"18:89980144e3b04b0bbc2282504069c1ea","fee":1}' """
        #rt_dc = json.loads(rt.text)
        dc={
            'success':True,
            #'key':key,
        }
        return dc
        #return JsonResponse(dc)
    
    def gen_code(self):
        choice='1234567890'
        return ''.join([random.choice(choice) for i in range(6)])
    
@director_view('tencent.validate_phonecode')
def Validate_phonecode(mobile,ans,**kws):
    #key = request.GET.get('code_key')
    #ans =request.GET.get('ans')
    code = redis_conn.get('sms:code:%s'%mobile)
    if code and str(code.decode('utf-8'))==str(ans):
        #redis_conn.delete('sms:code:%s'%mobile) # 没必要删除，已经证明该手机号码属于 该人 ，就算再次输入该code 也可以起作用
        dc={
            'success':True,
        }
    else:
        raise UserWarning('验证错误，或者已经过期!')
        #dc={
            #'success':False,
            #'msg':'验证错误，或者已经过期!'
        #}
    return dc
    #return HttpResponse(json.dumps(dc),content_type="application/json")



    

    
#def send_validate_code(phone,  code , last_minits = 3): 
    #strRand = get_str(10)
    #time_now =  int(time.time())
    #validate_temp = settings.TENCENT.get('validate_temp')
    #args = {
        #'sdkappid': settings.TENCENT.get('SdkAppId'),
        #'strRand': strRand,
        #'appkey': settings.TENCENT.get('AppKey'),
        #"time": time_now,
        #'phone': phone,
    #}
    
    
    #api_url = 'https://yun.tim.qq.com/v5/tlssmssvr/sendsms?sdkappid=%(sdkappid)s&random=%(strRand)s' % args
    
    #sig_str = 'appkey=%(appkey)s&random=%(strRand)s&time=%(time)s&mobile=%(phone)s' % args
    
    #hash = hashlib.sha256()
    #hash.update(sig_str.encode('utf-8'))
    #siged = hash.hexdigest()   
    
    #dc = {
        #"ext": "",
            #"extend": "",
            #"params": [
                #code,
                #last_minits
            #],
            #"sig": siged,
            #"sign": "腾讯云",
            #"tel": {
                #"mobile": phone,
                #"nationcode": "86"
            #},
            #"time": time_now,
            #"tpl_id": validate_temp  
    #}
    #general_log.info('手机号码：%(phone)s 发送验证码%(code)s' % {'phone': phone, 'code': code,})
    #rt = requests.post(api_url, json.dumps(dc) )
    #general_log.info( rt.text )
    ##print(rt.text)
    #""" '{"result":0,"errmsg":"OK","ext":"","sid":"18:89980144e3b04b0bbc2282504069c1ea","fee":1}' """
    ##rt_dc = json.loads(rt.text)
