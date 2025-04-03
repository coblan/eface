# encoding:utf-8
from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from django.conf import settings
from eface.wechat.models import WxInfo
from django.contrib.auth.models import User
import json
from django.test import Client


class Command(BaseCommand):
    """
    """ 
    def handle(self, *args, **options):
        client = Client(enforce_csrf_checks=True)
        client.login( username='18280413452', password='123456')    
        #info = {'errMsg': 'getPhoneNumber:ok', 
                #'encryptedData': 'n4I6iuPf5LWdz/xJufAs5p6iI3bXYt/w6EmNGh0hVHvLq6Ko7la20qt8hP5iJErMuZTRNLPKcUORe2vfAwH7H1Yxrlq2FVTz5cMdQMy9Izzn0N/GGH+ASJyKcO3fC3upDGqvz9IYkXU/xq/S077uEwFYUuYLMKXLozwHna2beCZLMLb98IzOlJM1AZmdlcrghCQUbOd84SRLa3kLdF2B9Q==', 
                #'iv': 'QrDNPfQONhss//OHSUv1/A==', 'code': 'b5abb219fe52452be90ebf32ab8179b351b2fdf89c147b9d1aab98cb4b6cace0'}
        
        info = {'errMsg': 'getPhoneNumber:ok', 'encryptedData': 'H8XoW5gW1dDp/JNMF6Y2DK0mFinoVml+yqUfmCCFuF32Mvxfs0a7zUYlOQsHQFwRq1Dvdx61k90eevc1RXdPnW5+MNeSP0xAjdrI16rJ+uyvtEru2FqKoTpwADuTtmWUdQ20SK2plN8iMFlLwBlTvJ7MTL9Jwtvn3yV1wkR/3Yq8UXRzufLPD27HW+6E/xKzSnwhcYV3qeCCpHqM2vUA6Q==', 'iv': 'N9ttSzZjHsQkwqjLmoN66w==', 'code': 'e74226dc277f4ec0b0102ed5536676129d68c835ab63d1127d9c705d5ad7252f'}

        
        resp = client.post('/dapi/wxmin/phone',data=json.dumps({'info':info}),content_type="application/json")
        print(resp)
    