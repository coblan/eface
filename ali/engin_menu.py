from helpers.director.engine import BaseEngine
from .base_data import ali_page_dc

class AliEngin(BaseEngine):
    need_login=False

AliEngin.add_pages(ali_page_dc)