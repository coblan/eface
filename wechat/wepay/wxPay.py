from eface.wechat.wepay.page_jsapi import WePayJsapi,TWXOrder,WePayReplay
from eface.wechat.base_data import wechat_page_dc
from helpers.director.network import argument
from helpers.director.decorator import need_login
from django.http import JsonResponse
import decimal
from django.conf import settings
#from .models import MoneyLog
from helpers.director.shortcut import director
from helpers.func.dot_dict import read_dict_path
from django.utils import timezone
from helpers.func.random_str import get_str
import dicttoxml
from eface.wechat.funs import param_sign
import os
import requests

import logging
general_log = logging.getLogger('general_log')


class WxPay(object):
    """
    WXPAY={

    }
    """
    APPID=  read_dict_path(settings,'WXMINI_APP.appid') # settings.WXMINI_APP['appid']  # 如果接通的公众号，这里就是公众号id
    APPSECRET= read_dict_path(settings,'WXMINI_APP.secret') 
    replay_url= '/dapi/element/wepay/confirm'
    
    @need_login
    def info(self,*args,**kws):
        aa = FeibaoPay()
        return aa.get_context()
        #return JsonResponse(data=dc)
    
    def confirm(self):
        aa = FeibaoReply()
        dc= aa.get_context()
        return dc
    
    def payToUser(self, openid,amount):
        """在微信里，通过openid给用户发放奖励。
        参考网址:https://pay.weixin.qq.com/wiki/doc/api/tools/mch_pay.php?chapter=14_2
        双向验证参考requests:https://www.jianshu.com/p/5be07c496744
        @amount : 单位分
        微信返回xml:  <xml>\n<return_code><![CDATA[SUCCESS]]></return_code>\n<return_msg><![CDATA[]]></return_msg>\n<mch_appid><![CDATA[wx54f6cf95c7ff2c06]]></mch_appid>\n<mchid><![CDATA[1544740301]]></mchid>\n<nonce_str><![CDATA[qF2g4U9ojR9g074]]></nonce_str>\n<result_code><![CDATA[SUCCESS]]></result_code>\n<partner_trade_no><![CDATA[20210224Ce6US0Nw17j3972]]></partner_trade_no>\n<payment_no><![CDATA[10101062053222102247864627837359]]></payment_no>\n<payment_time><![CDATA[2021-02-24 22:58:44]]></payment_time>\n</xml>
        """ 
        general_log.debug(f'开始转账openid={openid};amount={amount}')
        url = 'https://api.mch.weixin.qq.com/mmpaymkttransfers/promotion/transfers'
        trad_no = timezone.now().strftime('%Y%m%d')
        trad_no+= get_str()
        dc = {
            'mch_appid': settings.WXMINI_APP['appid'],#'wx54f6cf95c7ff2c06',
            'mchid': settings.WX_MACHID , #'1544740301',
            'nonce_str':get_str(length=15),
            'partner_trade_no':trad_no,
            'openid':openid,
            'check_name':'NO_CHECK',
            'amount':int( amount),
            'desc':'提现'
        }
        syn_key = settings.WX_MACHSECERT  
        dc['sign']= param_sign(syn_key,dc)
        dc_str = dicttoxml.dicttoxml(dc)
        #pkcs_file = os.path.join(settings.BASE_DIR,'static','wechatmerchat_cert','apiclient_cert.p12')
        cert_path = os.path.join(settings.BASE_DIR,'resource','wechatmerchat_cert','apiclient_cert.pem')
        key_path = os.path.join(settings.BASE_DIR,'resource','wechatmerchat_cert','apiclient_key.pem')
        #rt = post(url,data=dc_str,  verify=False, pkcs12_filename=pkcs_file,pkcs12_password=settings.WX_MERCHANT_ID)
        rt = requests.post(url,data=dc_str,cert=(cert_path,key_path))
        return {
            'trade_no':trad_no,
            'resp':rt.text
        }    

director.update({
    'wepay':WxPay,
})

class FeibaoPay(WePayJsapi):
    APPID= settings.WXMINI_APP['appid']  # 如果接通的公众号，这里就是公众号id
    APPSECRET=  settings.WXMINI_APP['secret']
    
    @need_login
    def get_context(self):
        
        dc = self.make_order(self.request)
        dc['orderid']=self.wxorder.pk
        #return JsonResponse(data=dc)
        return dc
    
    def setup_model(self):
        """
        money=1
        """
       
        user = self.request.user
        kws = argument.get_argument(self.request,outtype='dict')
        money = kws.get('money')
        general_log.debug('发起微信支付:金额(分):%s'%money)
        
        self.wxorder = TWXOrder.objects.create(trade_type=self.trade_type,
                                          total_fee= money,
                                            openid=self.openid,
                                            body='渣渣科技',
                                              user=user)
        return self. wxorder 
    
class FeibaoReply(WePayReplay):
  
    def makesure_order(self, notify_data):
        general_log.debug('收到微信回复:%s'%notify_data)
        
        wxorder = super().makesure_order(notify_data)
        #general_log.debug("微信回复返回")
        if wxorder : #and notify_data.get('return_code') =='SUCCESS': 
            #confirm_order(order)
            #general_log.debug("进入微信订单")
            general_log.debug(wxorder.total_fee)
            money_yuan = decimal.Decimal( float( wxorder.total_fee )/100 )
            general_log.debug(f'微信支付增加用户:{wxorder.user.pk};金额:{money_yuan}')
            #wxorder.user.userprofile.money   += money_yuan
            #wxorder.user.userprofile.changeMoney(money=money_yuan,
                                                  #kind=6,
                                                  #memo='微信支付') 
            #wxorder.user.userprofile.save()
            #MoneyLog.objects.create(user=wxorder.user,
                                    #money= money_yuan,
                                    #memo ='微信支付',
                                    #kind=6)

#wechat_page_dc.update({
    #'wepay_jsapi':FeibaoPay,
    #'wepay_jsapi_reply':FeibaoReply
#})