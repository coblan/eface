from django.conf import settings
import requests
import json
from helpers.director.decorators.cache_fun import cache_fun
import time
from helpers.func.random_str import get_str
import hashlib
from helpers.director.shortcut import director_view
from . wepa.funs import get_access_token

@director_view('wx_jssdk_config_parameter')
def get_config_parameter(url):
    access_token = get_access_token()
    ticket = _get_ticket(access_token)
    params = {
        'noncestr':get_str(),
        'jsapi_ticket':ticket,
        'timestamp':int(time.time()),
        'url':url,
        
    }
    sign = _params_sign(params)
    return {
        'appId':settings.WX_APPID,
        'signature':sign,
        'noncestr':params['noncestr'],
        'jsapi_ticket':params['jsapi_ticket'],
        'timestamp':params['timestamp'],        
    }
    

#@cache_redis(ex=7000)
#def _get_access_token():
    #dc ={
        #'APPID':settings.WX_APPID,
        #'APPSECRET':settings.WX_APPSECRET
    #}
    #url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%(APPID)s&secret=%(APPSECRET)s'%dc
    #rt = requests.get(url)
    #dc = json.loads(rt.text)
    #return dc['access_token']

@cache_fun(ex=7000)
def _get_ticket(access_token):
    dc={
        'access_token':access_token
    }
    url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%(access_token)s&type=jsapi'%dc
    rt = requests.get(url)
    rt_dc = json.loads(rt.text)
    return rt_dc['ticket']


def _params_sign(params):
    sign_str = ''
    for k,v in sorted(params.items(),key=lambda p:p[0]):
        if v:
            sign_str += '{key}={value}&'.format(key=k,value=v)
    sign_str = sign_str.rstrip('&')
    #sign_str = sign_str + 'key=' + APISECERT
    #return hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()   
    return hashlib.sha1(sign_str.encode('utf-8')).hexdigest()