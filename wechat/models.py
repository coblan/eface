# encoding:utf-8
from django.db import models
from django.utils import timezone
import random
from django.contrib.auth.models import User
from helpers.director.model_func.cus_fields.cus_picture import PictureField
from django.conf import settings
import binascii
from helpers.director.model_func.order_key import date_shortuuid

def get_no():
    a='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return timezone.now().strftime('%Y%m%d%H%M%S')+''.join(random.choice(a) for i in range(8))

class WXOrderBase(models.Model):
    
    no = models.CharField('内部微信订单号',max_length=30,unique=True,default = date_shortuuid)
    transaction_id=models.CharField('微信支付订单号',max_length=300,blank=True)
    time_end=models.CharField('支付完成时间',max_length=300,blank=True)
    total_fee=models.CharField('总金额',max_length=300,blank=True)
    openid=models.CharField('付款人openid',max_length=300,blank=True)
    trade_type=models.CharField('交易类型',max_length=300,blank=True)
    result_code=models.CharField('业务结果',max_length=300,blank=True)
    body=models.CharField('实际商品名称',max_length=300,blank=True)
    detail=models.TextField(verbose_name='详细',blank=True)
    create_time=models.DateTimeField(verbose_name='记录创建时间',auto_now_add=True,null=True)
    last_update_time=models.DateTimeField(verbose_name='记录最后修改时间',auto_now=True,null=True)
    pay=models.CharField('支付情况',max_length=100,blank=True)
    confirmed=models.BooleanField('是否确认',default=False)
    
    #def __init__(self,*args,**kw):
        #super(WXOrderBase,self).__init__(*args,**kw)
        #if not self.no:
            #self.no= 'WX'+get_no()
    
    class Meta:
        abstract=True


class TWXOrder(models.Model):
    no = models.CharField('内部微信订单号',max_length=30,unique=True,default = date_shortuuid)
    #no = models.CharField('内部微信订单号',max_length=300,blank=True)
    transaction_id=models.CharField('微信支付订单号',max_length=300,blank=True)
    time_end=models.CharField('支付完成时间',max_length=300,blank=True)
    total_fee=models.CharField('总金额',max_length=300,blank=True)
    openid=models.CharField('付款人openid',max_length=300,blank=True)
    trade_type=models.CharField('交易类型',max_length=300,blank=True)
    result_code=models.CharField('业务结果',max_length=300,blank=True)
    body=models.CharField('实际商品名称',max_length=300,blank=True)
    detail=models.TextField(verbose_name='详细',blank=True)
    create_time=models.DateTimeField(verbose_name='记录创建时间',auto_now_add=True,null=True)
    last_update_time=models.DateTimeField(verbose_name='记录最后修改时间',auto_now=True,null=True)
    pay=models.CharField('支付情况',max_length=100,blank=True)
    confirmed=models.BooleanField('是否确认',default=False)
    err_code_des = models.CharField('错误描述',max_length=200,blank=True)
    user = models.ForeignKey(User,blank=True,null=True)
    
    def __str__(self):
        return self.transaction_id
    
    
    #def __init__(self,*args,**kw):
        #super(WXOrderBase,self).__init__(*args,**kw)
        #if not self.no:
            #self.no= 'WX'+get_no()
    


#class AccessToken(models.Model):
    #appid=models.CharField('appid',max_length=50,blank=True)
    #token=models.CharField('token',max_length=100,blank=True)
    #update_time=models.CharField('update time',max_length=50,blank=True)


SEX_OPTION=(
    (0,'未知'),
    (1,'男'),
    (2,'女'),
)

class WxInfo(models.Model):
    user=models.OneToOneField(User,verbose_name='用户账号',blank=True,null=True)
    openid=models.CharField('openid',max_length=30,null=True,blank=True)
    head=PictureField('微信头像',max_length=300,blank=True)
    nickname = models.CharField('微信昵称',max_length=200,blank=True)
    phone = models.CharField('手机号码',max_length=50,blank=True)
    sex=models.IntegerField('性别',default=0,choices=SEX_OPTION)
    province=models.CharField('省份',max_length=50,blank=True)
    city=models.CharField('城市',max_length=50,blank=True)
    country=models.CharField('国家',max_length=50,blank=True)
    appid = models.CharField('Appid',max_length=30,blank=True)
    unionid = models.CharField('openid',max_length=30,unique=True,null=True,blank=True)
    session_key = models.CharField('session_key',max_length=50,blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['openid'])
        ]
    
    @property
    def dbNickname(self):
        isbase64 = getattr(settings,'WX_NICKNAME_HEX',False)
        if isbase64:
            return binascii.a2b_hex( self.nickname ).decode('utf-8')
        else:
            return self.nickname
    
    @dbNickname.setter 
    def dbNickname(self,nickname):
        isHEX = getattr(settings,'WX_NICKNAME_HEX',False)
        if isHEX:
            self.nickname = binascii.b2a_hex( nickname.encode('utf-8') )
        else:
            self.nickname = nickname