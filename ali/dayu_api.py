from .dayu import SMS
from .base_data import ali_page_dc
import re
from django.http import HttpResponse
import json
from helpers.director.network.myredis import redis_conn

#def get_code(request):
   
    # mobile= request.GET.get('mobile')
    # send_type = request.GET.get('type','1')
    #kw=arg.get_argument(request)
    
class AliPhoneCode(object):
    """通过短信发验证码"""
    def __init__(self, request,engin):
        self.request=request
        
    def get_context(self):
        try:
            mobile = self.request.GET.get('mobile','')
            if not re.search('\d{11}',mobile):
                raise UserWarning('not valid mobile number')
            mesenger = SMS()
            code = mesenger.send(mobile)
            key =str(int(time.time()))+ get_random_word()
            redis_conn.set(key,code,ex=60*2) # 2分钟过期
            
            dc={
                'status':'success',
                'code_key':key
            }
        except UserWarning as e:
            dc={
                'status':'fail',
                'msg':str(e)
            }
        return HttpResponse(json.dumps(dc),content_type="application/json")

class AliPhoneValidate(object):
    def __init__(self, request,engin):
        self.request=request
        
    #@csrf_exempt
    def get_context(self):
        key = self.request.GET.get('code_key')
        ans =request.GET.get('ans')
        code = redis_conn.get(key)
        if str(code)==str(ans):
            redis_conn.delete(key)
            dc={
                'status':'success',
            }
        else:
            dc={
                'status':'fail'
            }
        # if request.method=='POST':
            # dc =get_argument(request)    
            # mobile=dc.get('mobile')
            # vcode=dc.get('vcode')
            # send_type=int(dc.get('type',1))
            # dc={}
            # if mobile and vcode:
                # dc['ret']= 1  # 1好像是代表成功
        return HttpResponse(json.dumps(dc),content_type="application/json")


ali_page_dc.update({
    'phonecode':AliPhoneCode,
    'phonecode_validate':AliPhoneValidate,
})
