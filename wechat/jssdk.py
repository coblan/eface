from django.conf import settings
import requests
import json

def get_config_parameter(url):
    access_token = _get_signature(url)
    
    
def _get_signature(url):
    dc ={
        'APPID':settings.WX_APPID,
        'APPSECRET':settings.WX_APPSECRET
    }
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%(APPID)s&secret=%(APPSECRET)s'%dc
    rt = requests.get(url)
    dc = json.loads(rt.text)
    print(dc.get(k))
    return dc.get('access_token')
    