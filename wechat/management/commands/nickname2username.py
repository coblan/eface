# encoding:utf-8
from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from django.conf import settings
from helpers.director.base_data import site_cfg
from helpers.director.models import PermitModel
from eface.wechat.models import WxInfo
from django.db import transaction
from django.contrib.auth.models import User

class Command(BaseCommand):
    """
    """ 
    def handle(self, *args, **options):
        for wxinfo in WxInfo.objects.all():
            if not wxinfo.user.first_name:
                print(wxinfo.user.username)
                wxinfo.user.first_name = wxinfo.nickname
                wxinfo.user.save()
        print('转换完成')
    
