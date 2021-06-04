from helpers.director.shortcut import director_view,get_request_cache
import json
import requests
from .models import WxInfo
from django.contrib import auth
from django.contrib.auth.models import User
from django.conf import settings
from helpers.func.random_str import short_uuid
from . de_crypt.WXBizDataCrypt import WXBizDataCrypt
import logging
general_log = logging.getLogger('general_log')

@director_view('wxmin/login')
def wxmin_login(code,appid):
    """微信小程序登录
    
    小程序端获取到code,将code和appid一起发送给后端。
    后端与微信服务器通信，获取用户openid。
    
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
    general_log.debug('获取微信小程序code返回:%s'%dc)
    if not dc.get('openid'):
        raise UserWarning('获取Openid报错,errors=%s'%dc)
    user = _create_user(dc.get('openid'),appid)
    user.wxinfo.session_key = dc.get('session_key')
    user.wxinfo.save()
    
    request = _login(user)
    return {
        'token':request.session._get_or_create_session_key(),
        'head':user.wxinfo.head,
        'nickname':user.wxinfo.nickname,
        'phone':user.wxinfo.phone,
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
    
@director_view("wxmin/phone")
def upload_phone(info={}):
    """
    info = {
        "encryptedData": "eVzUS4jH/S1a1yP7z1GCO7FGY3SLr2/ms4K1TN93cSGxkKj8Oxt3V3ls5uLRRymoF4t2ju0O3JjkB35FANnkJFc5px0SCUdAjeKSxEtDoGJidtnjkVwB7EB1KnzW8ZsnX4VseVJUmJUtZ21CAD8V2ILxJfjQ/Qx9RWaB/ABlvmV9zWL3x3RooLTOZrBYKk3t5XJgm17pceTjrsqsGvcfgg==",
        "iv": "o3+82NEPr7nZXmMfceuCig==",
    }
    """
    if isinstance(info,dict):
        info_dc = info
    else:
        info_dc = json.loads(info)    
    general_log.debug('解密参数:%s'%info_dc)
    user = get_request_cache()['request'].user
    pc = WXBizDataCrypt(user.wxinfo.appid, user.wxinfo.session_key)
    dc = pc.decrypt(info_dc.get('encryptedData') , info_dc.get('iv') )
    #dc = {'phoneNumber': '1834xxxx', 'purePhoneNumber': '1834xxxx', 'countryCode': '86', 'watermark': {'timestamp': 1621871633, 'appid': 'wx12748118a5b22116'}}
    general_log.debug('解密结果:%s'%dc)
    user.wxinfo.phone=dc.get('phoneNumber')
    user.wxinfo.save()
    

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
