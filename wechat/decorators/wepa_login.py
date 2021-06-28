from eface.wechat.wepa.fuwu_pages import FuWuHaoLogin
from helpers.director.decorator import get_request_cache
from django.shortcuts import redirect
from functools import wraps
from django.core.exceptions import PermissionDenied
from helpers.director.exceptions.unauth401 import UnAuth401Exception

def need_wx_login(fun):
    """用在公众号页面上，如果未登录，则跳转服务号登录页面。
    """
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


def need_wx_user_login(fun):
    """微信用户接口调用装饰器，需要登录的Api都需要用该装饰器
    
    """
    @wraps(fun)
    def _fun(*args,**kw):
        request = get_request_cache().get('request')
        if request.user.is_authenticated():
            if not getattr( request.user,'wxinfo',None):
                raise PermissionDenied('Login with Wechat User')
            return fun(*args,**kw)
        else:
            raise UnAuth401Exception('Unauthorized')
            #return HttpResponse('Unauthorized', status=401)
            #raise PermissionDenied('Need login !')
        
    return _fun    