from ..base_data import wechat_page_dc
from django.conf import settings
from django.shortcuts import redirect
import requests
import json

"""
该模块暂时无用
"""

class MakeSubscribe(object):
    APPID=settings.WX_APPID
    APPSECRET=settings.WX_APPSECRET
    MACHID=settings.WX_MACHID
    MACHSECERT=settings.WX_MACHSECERT 
    def __init__(self, request):
        self.request = request
        self.next_url = request.GET.get('next')
        
    def get_context(self):
        redict_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%(appid)s&redirect_uri=%(self_domain)s/wx/makesubscribe_callback?next=%(next)s&response_type=code&scope=snsapi_base&state=123#wechat_redirect'
        redict_url = redict_url %{
            'self_domain':settings.SELF_DOMAIN,
            'appid':self.APPID,
            'next':self.next_url
            
        }
        return redirect(redict_url)
    

    
class MakeSubscribeCallback(object):
    APPID=settings.WX_APPID
    APPSECRET=settings.WX_APPSECRET
    MACHID=settings.WX_MACHID
    MACHSECERT=settings.WX_MACHSECERT
    def __init__(self,request):
        self.request = request
        self.next_url = request.GET.get('next')
        
    def get_context(self):
        access_token = self.get_access_token()
        
    
    def get_access_token(self):
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
        resp=requests.get(url)
        dc = json.loads(resp.text)
        return dc
    
    def check_issubscribe(self,accesstoken,openid):
        args = {
            'accesstoken':accesstoken,
            'openid':openid,
        }
        url ="https://api.weixin.qq.com/cgi-bin/user/info?access_token=%(accesstoken)s&openid=%(openid)s&lang=zh_CN"
        url =url%args
        rt = requests.get(url)
        dc = json.loads(rt.text)
        print(dc)
    
    


wechat_page_dc.update({
    'makesubscribe':MakeSubscribe,
    'makesubscribe_callback':MakeSubscribeCallback
})

#def direct_wash_view(request):
    #redict_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx7018edf138c754f4&redirect_uri=%(self_domain)s/wx/directwash&response_type=code&scope=snsapi_base&state=123#wechat_redirect'
    #redict_url = redict_url %{
        #'self_domain':settings.SELF_DOMAIN
    #}
    #return redirect(redict_url)


#class DirectWash(object):
    #APPID=settings.WX_APPID
    #APPSECRET=settings.WX_APPSECRET
    #MACHID=settings.WX_MACHID
    #MACHSECERT=settings.WX_MACHSECERT
    
    #def __init__(self, request, engin):
        #self.crt_user = request.user
        #self.request=request
    
    #def get_template(self,prefer=None):
        #return 'wxfront/direct_wash.html'
    
    #def get_context(self):
        #token_dc = self.get_access_token()
        #token = token_dc.get('access_token')
        #openid = token_dc.get('openid')        
        #return {
            #'openid':openid
        #}
    
