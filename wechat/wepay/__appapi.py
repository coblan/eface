from .page_jsapi import WePayJsapi,WePayReplay
from helpers.director.shortcut import director_view

class WePayAppapi(WePayJsapi):
    trade_type='APP'
    
    
