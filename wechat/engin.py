from helpers.director.engine import BaseEngine
from .base_data import wechat_page_dc

class WechatEngine(BaseEngine):
    need_login=False
    access_from_internet=True

WechatEngine.add_pages(wechat_page_dc)