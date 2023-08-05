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

import logging
general_log = logging.getLogger('general_log')


class WxPay(WePayJsapi):
    """
    WXPAY={

    }
    """
    APPID=  read_dict_path(settings,'WXMINI_APP.appid') # settings.WXMINI_APP['appid']  # 如果接通的公众号，这里就是公众号id
    APPSECRET= read_dict_path(settings,'WXMINI_APP.secret') 
    
    @need_login
    def info(self):
        dc = self.make_order(self.request)
        dc['orderid']=self.wxorder.pk
        return dc
        #return JsonResponse(data=dc)
    
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



director.update({
    'wepay':WxPay
})


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

wechat_page_dc.update({
    'wepay_jsapi':FeibaoPay,
    'wepay_jsapi_reply':FeibaoReply
})