from eface.wechat.wepa.fuwu_pages import FuWuHaoLogin
from helpers.director.decorator import get_request_cache
from django.shortcuts import redirect

def need_wx_login(fun):
    def _fun(*args,**kws):
        request = get_request_cache().get('request')
        user = request.user
        if not user.is_authenticated:
            
            # 如果没有登录，则通过微信登录
            url = FuWuHaoLogin.regist_or_login_url(next_url=request.get_full_path())
            return redirect(url)
        else:
            return fun(*args,**kws)
    return _fun