from django.conf import settings
import requests
from helpers.director.decorators.cache_redis import cache_redis
import json

@cache_redis(ex=7000)
def get_access_token():
    args = {'appid':settings.WX_APPID,'secret':settings.WX_APPSECRET}
    url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%(appid)s&secret=%(secret)s"
    url = url % args
    rt = requests.get(url)
    dc = json.loads(rt.text)
    return dc['access_token']