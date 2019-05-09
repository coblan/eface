# encoding:utf-8
from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from django.conf import settings
from helpers.director.base_data import site_cfg
from helpers.director.models import PermitModel
import base64
import binascii
from eface.wechat.models import WxInfo
from django.db import transaction

class Command(BaseCommand):
    """
    相互转换
    -s base64;hex;str
    -d ...
    """
    def add_arguments(self, parser):
        parser.add_argument('-s', nargs='?', type=str)
        parser.add_argument('-d', nargs='?', type=str)
        
    def handle(self, *args, **options):
        src = options.get('s')
        dst = options.get('d')
        with transaction.atomic():
            for info in WxInfo.objects.all():
                if src =='base64':
                    nick_byt = base64.b64decode(info.nickname.encode('utf-8'))
                elif src == 'hex':
                    nick_byt = binascii.a2b_hex(info.nickname.encode('utf-8'))
                else:
                    nick_byt = info.nickname.encode('utf-8')
                
                if dst =='base64':
                    info.nickname = base64.b64encode(nick_byt).decode('utf-8')
                elif dst=='hex':
                    info.nickname = binascii.b2a_hex(nick_byt).decode('utf-8')
                else:
                    info.nickname = nick_byt.decode('utf-8')
                info.save()
        print('转换完成')
    
