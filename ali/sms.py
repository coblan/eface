from ._sms import send_sms
from django.conf import settings
import json 
import uuid
from helpers.func.random_str import get_random_number
from helpers.director.shortcut import director_view
from helpers.director.network.myredis import redis_conn
import re

code_template_id = settings.ALI_SMS.get('code_template_id') 



@director_view('ali.phonecode')
def get_phonecode(mobile,**kws):
    last_minits=5
    code = get_random_number()
    #key =  mobile # get_str()  #  直接用mobile作为key  发送到前端的key
    redis_conn.set('sms:code:%s'%mobile,code,ex=60*5) # 5分钟过期
    
    if not re.search('\d{11}',mobile):
        raise UserWarning('not valid mobile number')
    
    params = {"code":code}
    __business_id = uuid.uuid1()
    rt = send_sms(__business_id, mobile, '企鹅洗车', code_template_id,params)
    
    print(rt)
    
    return  {
            'success':True,
        }

@director_view('ali.validate_phonecode')
def Validate_phonecode(mobile,ans,**kws):

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

