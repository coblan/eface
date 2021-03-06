from django.conf import settings
import requests
import json
from helpers.director.decorators.cache_fun import cache_fun,clear_fun_cache
import time
from helpers.func.random_str import get_str
import hashlib
from helpers.director.shortcut import director_view
from . wepa.funs import get_access_token

proxy = getattr(settings,'INTERNET_PROXY',{})

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
    
@cache_fun(ex=7000)
def _get_ticket(access_token):
    dc={
        'access_token':access_token
    }
    url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%(access_token)s&type=jsapi'%dc
    rt = requests.get(url,proxies=proxy)
    rt_dc = json.loads(rt.text)
    if rt_dc.get('errcode')==40001:
        clear_fun_cache('wx:cache:access_token')
        raise UserWarning('微信缓存ACCESS TOKEN过期，请刷新重试！')
    else:
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