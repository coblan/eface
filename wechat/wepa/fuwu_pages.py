# encoding:utf-8

from __future__ import unicode_literals
import requests
from django.shortcuts import redirect
import json
from django.contrib.auth.models import User
from django.contrib import auth 
from ..models import WxInfo
import urllib
import random
from django.conf import settings
from ..base_data import wechat_page_dc
from helpers.func.random_str import short_uuid
import urllib
from helpers.director.decorator import get_request_cache
import base64
from django.shortcuts import render
from .funs import get_access_token
import logging
general_log = logging.getLogger('general_log')

proxy = getattr(settings,'INTERNET_PROXY',{})

class FuWuHaoLogin(object):
    """
    在使用时，如果判断用户没有登录，则
    url = FuWuHao.regist_or_login_url()
    redirect(url)
    这样会利用openid登录用户，然后跳转到settings.WX_REDIRECT_URL这个地址
    
    微信的起始触发地址为：
    https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx7018edf138c754f4&redirect_uri=http://port.enjoyst.com/wx/login&response_type=code&scope=snsapi_userinfo&state=123#wechat_redirect
    """
    
    APPID= settings.WX_APPID  #'wx7080c32bd10defb0'
    APPSECRET=settings.WX_APPSECRET #'d4624c36b6795d1d99dcf0547af5443d'
    need_login=False
    def __init__(self, request,engin):
        self.request=request
        
    @classmethod
    def regist_or_login_url(cls,next_url):
        """
        """
        url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%(appid)s&redirect_uri=%(redirect_url)s&response_type=code&scope=snsapi_userinfo&state=123#wechat_redirect'
        self_engin_url = urllib.parse.urljoin(settings.SELF_DOMAIN, '/wx/regist_then_login')
        if next_url:
            redirect_url = self_engin_url + '?next=' +next_url
        else:
            redirect_url = self_engin_url
        kws={
            'appid':cls.APPID,
            'redirect_url':redirect_url,
        }
        return url%kws
    
    def get_context(self):
        token_dc = self.get_auth_data_dict()
        token = token_dc.get('access_token')
        openid = token_dc.get('openid')
        userinfo= self.get_userinfo(token, openid)
        user = self.update_or_create_user(userinfo)
        self.login(user)
        return self.after_login(user)

        
    def after_login(self,user):
        """
        这里用于重载，当微信公众号登录后，跳转的页面
        """
        request = get_request_cache()['request']
        path = request.get_full_path()
        query = urllib.parse.urlparse(path).query
        if query:
            dc = urllib.parse.parse_qs(query)
            if dc.get('next'):
                return redirect(dc.get('next')[0])
        return redirect(settings.WX_REDIRECT_URL)

    
    
    def get_auth_data_dict(self):
        """
        通过code ，去wechat获取access_token
        
        {'access_token': '17_Li-WdwRI67v1LpqaUrkUjcMclT-PjsJrvCvRofT91m2gkSH-QJ_hx-HYKuQWUn6iM9cGsFX2PThXIRBFHHf6RCMLjLRB2t9exNTQCHulfP0', 
        'expires_in': 7200, 
        'refresh_token': '17_T-8jAYKfurKnWkGjwTqgmnCV9kQpZLps0IaYFQ7Zb4_vn1uezNW87_6NmVgelctihiXgoLjuX1ezhA4HoP8v3KllERqOHKlMK0KJSRVFlyk', 
        'openid': 'oIvmdwrcmoseQW298jvtUa1U1udM', 
        'scope': 'snsapi_userinfo', 
        'unionid': 'oyelCwmIiDGa3x4wxEbX3_LJ7y3o'}

        """
        code=self.request.GET.get('code')
        url='https://api.weixin.qq.com/sns/oauth2/access_token?appid=%(appid)s&secret=%(secret)s&code=%(code)s&grant_type=authorization_code'\
            %{'appid':self.APPID,'secret':self.APPSECRET,'code':code}
        
        general_log.debug('微信用户登录 代理: %(proxy)s ; code=%(code)s'%{'proxy':json.dumps(proxy),'code':code} )
        resp=requests.get(url,proxies=proxy)
        general_log.debug('返回结果: %s'%resp.text)
        dc = json.loads(resp.text)
        return dc
     
    def get_userinfo(self,token,openid):
        """
        通过access_token获取用户的具体信息
        
        {'openid': 'oIvmdwrcmoseQW298jvtUa1U1udM', 
        'nickname': '秋风扫落叶', 
        'sex': 1, 
        'language': 'zh_CN', 
        'city': '眉山', 
        'province': '四川', 
        'country': '中国', 
        'headimgurl': 'http://thirdwx.qlogo.cn/mmopen/vi_32/nzMS6zZhJEiaMMBXzaWHk970m4A32TAAD29B1yKMaeiamibj9H0yz1sdYPFMHKiboleZ6m3el9MaOB1XvUTboxHmBw/132', 
        'privilege': [], 
        'unionid': 'oyelCwmIiDGa3x4wxEbX3_LJ7y3o'}

        """
        
        url='https://api.weixin.qq.com/sns/userinfo?access_token=%(access_token)s&openid=%(openid)s&lang=zh_CN'\
            %{'access_token':token,'openid':openid}
        
        general_log.debug('微信请求用户信息url = %s'%url)
        resp=requests.get(url,proxies=proxy)
        resp.encoding ='utf-8'
        general_log.debug('返回结果%s'%resp.text)
        dc= json.loads(resp.text)
        if dc.get('errcode'):
            raise UserWarning('微信获取用户信息错误:%s'%resp.text)
        return dc
    
    def update_or_create_user(self,userinfo):
        openid=userinfo.get('openid')
        wxinfo,c = WxInfo.objects.get_or_create(openid=openid)
        wxinfo.head=userinfo['headimgurl']
        wxinfo.sex=userinfo['sex']
        wxinfo.nickname= userinfo['nickname'] 
        wxinfo.province=userinfo['province']
        wxinfo.city=userinfo['city']
        wxinfo.country=userinfo['country']
        #wxinfo.save()
        if not wxinfo.user:
            tmp= short_uuid() #random.randint(0,99999999)
            wxinfo.user=User.objects.create(username=tmp,first_name = wxinfo.nickname)
            #weinfo.user.username='_uid_%s'%weinfo.user.id
            #weinfo.user.save()
        wxinfo.save()   
        return wxinfo.user
    
            
    def login(self,user):
        """
        """
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        auth.login(self.request,user)

class SubscribeProb(object):
    """废弃了"""
    def __init__(self,request,engin):
        self.request = request
    
    def get_context(self):
        return render(self.request,'wxfront/subscribe.html')

        
def is_subscribe(openid):
    accesstoken = get_access_token()
    args = {
        'accesstoken':accesstoken,
        'openid':openid,
    }
    url ="https://api.weixin.qq.com/cgi-bin/user/info?access_token=%(accesstoken)s&openid=%(openid)s&lang=zh_CN"
    url =url%args
    rt = requests.get(url,proxies=proxy)
    dc = json.loads(rt.text)
    return dc['subscribe'] ==1
    

wechat_page_dc.update({
    'regist_then_login':FuWuHaoLogin,
    'subscribe':SubscribeProb,
})

#class FuWuHao_old(object):
    #"""
    #先重定向，获取到code
    #再调用code获取token和openid，
    #如果是第一次登陆，会再利用token获取用户信息，并且保存下来。
    #"""
    #APPID='wx7080c32bd10defb0'
    #APPSECRET='d4624c36b6795d1d99dcf0547af5443d'
    ##WxInfo=WxInfo
    #scheme='http'
    #next_url='/_wechat/print_username'
    #def get_redirect_url(self,request):
        #"""
        #生成的url，直接放到公众号的菜单里面，可以跳转到 recieve_url,携带参数code
        #"""
        #red_url=self.get_recieve_url(request)
        #red_url=urllib.quote(red_url)
        #url="https://open.weixin.qq.com/connect/oauth2/authorize?appid=%(appid)s&redirect_uri=%(redirect_url)s&response_type=code&scope=%(scope)s&state=123#wechat_redirect"\
            #%{'appid':self.APPID,'redirect_url':red_url,'scope':'snsapi_userinfo'}
        #return url
    
    #def get_recieve_url(self,request):
        #host=request.META['HTTP_HOST']
        #red_url=self.scheme+'://'+host+'/_wechat/rec_code'
        #return red_url
    
    #def rec_code(self,request):
        #code=request.GET.get('code')
        #print('code is %s'%code)
        #url='https://api.weixin.qq.com/sns/oauth2/access_token?appid=%(appid)s&secret=%(secret)s&code=%(code)s&grant_type=authorization_code'\
            #%{'appid':self.APPID,'secret':self.APPSECRET,'code':code}
        #resp=requests.get(url)
        #dc = json.loads(resp.content)
        #openid = dc['openid']
        #token=dc['access_token']
        #wxinfo,c = WxInfo.objects.get_or_create(openid=openid)
        #print('save ok')
        #if c:
            #dc = self.get_info(token,openid)
            #wxinfo.head=dc['headimgurl']
            #wxinfo.sex=dc['sex']
            #wxinfo.nickname=dc['nickname']
            #wxinfo.province=dc['province']
            #wxinfo.city=dc['city']
            #wxinfo.country=dc['country']
            #wxinfo.save()
            
        #self.on_login(request,wxinfo)
        
    
    #def get_info(self,token,openid):
        #url='https://api.weixin.qq.com/sns/userinfo?access_token=%(access_token)s&openid=%(openid)s&lang=zh_CN'\
            #%{'access_token':token,'openid':openid}
        #resp=requests.get(url)
        #return json.loads(resp.content)

    #def on_login(self,request,weinfo):
        #if not weinfo.user:
            #tmp=random.randint(0,99999999)
            #weinfo.user=User.objects.create(username='_tmp_%s'%tmp)
            #weinfo.user.username='_uid_%s'%weinfo.user.id
            #weinfo.user.save()
            #weinfo.save()
        #weinfo.user.backend = 'django.contrib.auth.backends.ModelBackend'
        #auth.login(request, weinfo.user)
        #print('log in ok')
        


