from django.conf import settings
import requests
from helpers.director.decorators.cache_fun import cache_fun
import json

@cache_fun(ex=7000)
def get_access_token():
    """获取公众号的access_token,这个是api的access_token,是共用的，需要缓存"""
    args = {'appid':settings.WX_APPID,'secret':settings.WX_APPSECRET}
    url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%(appid)s&secret=%(secret)s"
    url = url % args
    proxy = getattr(settings,'INTERNET_PROXY',{})
    rt = requests.get(url,proxies=proxy)
    dc = json.loads(rt.text)
    try:
        access_token = dc['access_token']
    except:
        raise UserWarning('不能获取access_token %s'%rt.text)
    return access_token