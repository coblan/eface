from . page_jsapi import WePayJsapi
from helpers.director.decorator import need_login
class MiniPayApi(WePayJsapi):
    
    @need_login
    def get_context(self):
        user = self.request.user
        if getattr(user,'wxinfo'):
            raise UserWarning('请使用微信用户登录')
        return super().get_context()