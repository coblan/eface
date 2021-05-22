from helpers.director.shortcut import director_view,get_request_cache
import json
import requests
from .models import WxInfo
from django.contrib import auth
from django.contrib.auth.models import User
from django.conf import settings
from helpers.func.random_str import short_uuid

@director_view('wxmin/login')
def wxmin_login(code,appid):
    """
    @code:073msr0w3LngiW2yfc0w3JESdu4msr0q
    """
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=%(appid)s&secret=%(secret)s&js_code=%(code)s&grant_type=authorization_code'
    
    mini_dc = settings.WXMINI_APP.get(appid)
    appid = mini_dc.get('appid')
    secret = mini_dc.get('secret')
    code = code
    url = url%{'appid':appid,'secret':secret,'code':code}
    rt = requests.get(url)
    
    # {'session_key': 'nsNSutlsXJqFkPPY0sLBPw==', 'openid': 'ox2GhwBBqrux0MAEJmPWoPLMj3Os'}
    dc = rt.json()
    if not dc.get('openid'):
        raise UserWarning('获取Openid报错,errors=%s'%dc)
    user = _create_user(dc.get('openid'),appid)
    request = _login(user)
    return {
        'token':request.session._get_or_create_session_key(),
        'head':user.wxinfo.head,
        'nickname':user.wxinfo.nickname,
        }

@director_view('wxmin/userinfo')
def wxmin_userinfo(info):
    ''''{"nickName":"秋风扫落叶","gender":1,"language":"zh_CN","city":"Meishan","province":"Sichuan","country":"China","avatarUrl":"https://thirdwx.qlogo.cn/mmopen/vi_32/Ns7ia1ibrF722h0wNorJcM3s80ibK0NibvYENa80jBAxqQZmc0uPibma6YANT6zNAkCHnMU6jlv5FNFHPKr4TribyKYw/132"}'
    '''
    if isinstance(info,dict):
        dc = info
    else:
        dc = json.loads(info)
    request = get_request_cache()['request']
    info = WxInfo.objects.get(user=request.user)
    info.nickname= dc.get('nickName')
    info.sex=dc.get('gender')
    info.city= dc.get('city')
    info.province=dc.get('province')
    info.country=dc.get('country')
    info.head= dc.get('avatarUrl')
    info.save()
    info.user.first_name=info.nickname
    info.user.save()
    

def _create_user(openid,appid):
    #openid=userinfo.get('openid')
    wxinfo,c = WxInfo.objects.get_or_create(openid=openid,appid=appid)
    #wxinfo.head=userinfo['headimgurl']
    #wxinfo.sex=userinfo['sex']
    #wxinfo.nickname= userinfo['nickname'] 
    #wxinfo.province=userinfo['province']
    #wxinfo.city=userinfo['city']
    #wxinfo.country=userinfo['country']
    #wxinfo.save()
    if not wxinfo.user:
        #tmp=  openid #short_uuid() #random.randint(0,99999999)
        tmp = '%s%s'%(short_uuid(),wxinfo.pk)
        wxinfo.user=User.objects.create(username=tmp,first_name = '')
        #wxinfo.user.username='_uid_%s'%weinfo.user.id
        wxinfo.user.save()
    wxinfo.save()   
    return wxinfo.user

def _login(user):
    """
    """
    request = get_request_cache()['request']
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    auth.login(request,user)
    return request
