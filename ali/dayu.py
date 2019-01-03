# encoding:utf-8
from __future__ import unicode_literals
from django.conf import settings
from django.utils import timezone
import requests
import json
import hashlib
import random
import logging
general_log = logging.getLogger('general_log')

#import urllib

#import sys  

#reload(sys)  
#sys.setdefaultencoding('utf8') 

#from sdks.taobao import top

appkey=settings.ALI_SMS['appkey']#.encode('utf-8')
#appkey ='10'+appkey
secret=settings.ALI_SMS['appsecrect']#.encode('utf-8')

#appkey = '1023351868'
#secret = 'sandbox412bb4b5ea9a4841e00ea5f4c'
phone='17138080650'
#phone='18302867041'
code='567890'


#req=top.api.AlibabaAliqinFcSmsNumSendRequest()
#req.set_app_info(top.appinfo(appkey,secret))

#req.extend = "12345"
#req.sms_type = "normal"
#req.sms_free_sign_name = "大鱼测试"
#req.sms_param = "{code:'1234',product:'企鹅洗车'}"
#req.rec_num = "18349107170"
#req.sms_template_code = "SMS_6741313"

#try:
    #resp= req.getResponse()
    #print(resp)

#except Exception,e:
    
    #print(e)

class SMS(object):
    appkey=settings.ALI_SMS['appkey']
    secret=settings.ALI_SMS['appsecrect']
    
    def send(self,phone):
        code=self.random_code()
        params=self.build_param(phone,code)
        resp=requests.post('http://gw.api.taobao.com/router/rest',params=params)
        
        dc=json.loads(resp.text)
        if dc.get('error_response'):
            raise UserWarning(resp.text)
        # 暂时不处理 阿里大于返回的信息，只是打印出来，如果有问题，可以从log中查找到信息 
        general_log.debug('发送阿里大于短信到,返回结果为:%s'%resp.text)
        return code
        
    def random_code(self):
        choice='1234567890'
        return ''.join([random.choice(choice) for i in range(6)])
    
    def build_param(self,phone,code):
        params={
            'method':'alibaba.aliqin.fc.sms.num.send',
            'app_key':self.appkey,
            'timestamp':timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            'format':'json',
            'v':'2.0',
            'sign_method':'md5',
            'sms_type':'normal',
            'sms_free_sign_name':'注册验证' , #.encode('utf-8'),
            'rec_num':phone,
            'sms_template_code':'SMS_6741313',
            #'sms_param': ("{'code':'%s','product':'企鹅洗车'}"%code) #.encode('utf-8'),
            'sms_param': json.dumps({'code':code,'product':'企*鹅洗车'})
            }
        keys = list(params.keys())
        keys.sort()
        param=''
        for key in keys:
            param += key+params[key]
        
        sign = hashlib.md5( (secret+param+secret).encode('utf-8') ).hexdigest().upper()
        params['sign'] = sign
        return params

