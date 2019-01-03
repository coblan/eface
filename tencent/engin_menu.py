from helpers.director.engine import BaseEngine
from .base_data import ten_page_dc

class TencentEngin(BaseEngine):
    need_login=False

TencentEngin.add_pages(ten_page_dc)