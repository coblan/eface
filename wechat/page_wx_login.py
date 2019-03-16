from .base_data import wechat_page_dc
from .decorators.wepa_login import need_wx_login
from django.shortcuts import redirect

class WechatLoginPage(object):
    
    def __init__(self,request, engin):
        self.request = request
    
    @need_wx_login
    def get_context(self):
        next_url = self.request.GET.get('next')
        return redirect(next_url)
    

wechat_page_dc.update({
    'login':WechatLoginPage,
})