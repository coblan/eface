
from helpers.director.decorator import get_request_cache
from django.shortcuts import redirect
from ..wepa.fuwu_pages import is_subscribe

def need_subscribe(fun):
    def _fun(*args,**kws):
        request = get_request_cache().get('request')
        user = request.user
        if not is_subscribe(user.wxinfo.openid):
            return redirect('/wx/subscribe')
        else:
            return fun(*args,**kws)
    return _fun
