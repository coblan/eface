import time
import hashlib
import json
import requests
from helpers.func.random_str import get_str
from django.http import HttpResponse,JsonResponse
import random
import re

import logging
general_log = logging.getLogger('general_log')

class SmsSender(object):
    def __init__(self,sdkappid,appkey,template_id,sign):
        self.sdkappid= sdkappid
        self.appkey = appkey
        self.template_id = template_id
        self.sign=sign
    
    def send(self,mobile,params):
        """
        params:[{1},{2}]
        """
        time_now =  int(time.time())
        strRand = get_str(10)
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
                    "params":params,
                    "sig": siged,
                    #"sign": "测试短信",
                    "sign":self.sign,
                    "tel": {
                        "mobile": mobile,
                        "nationcode": "86"
                        },
                    "time": time_now,
                    "tpl_id": self.template_id  
            }
        general_log.info('向手机号码:%(mobile)s,发送短信模板:%(template_id)s,参数:%(params)s' % {'mobile': mobile,'template_id':self.template_id, 'params': params,})
        rt = requests.post(api_url, json.dumps(dc) )
        general_log.info( json.loads(  rt.text ) )