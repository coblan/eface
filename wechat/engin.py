from helpers.director.engine import BaseEngine
from .base_data import wechat_page_dc
from helpers.director.base_data import site_cfg

class WechatEngine(BaseEngine):
    need_login=False
    access_from_internet=True

WechatEngine.add_pages(wechat_page_dc)
site_cfg['inspect_dict']['wechat_page_dc'] = wechat_page_dc