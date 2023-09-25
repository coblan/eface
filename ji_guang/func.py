from django.conf import settings
from helpers.func.collection.mylist import split_list
import jpush
from jpush import common
import logging
general_log = logging.getLogger('general_log')
import requests

class MyJpush(jpush.JPush):
    
    def __init__(self, key, secret, timeout=30, zone='default',proxy={}):
        super().__init__(key, secret, timeout, zone)
        self.proxy = proxy
    
    def _request(self, method, body, url, content_type=None, version=None, params=None):
        
        headers = {}
        headers['user-agent'] = 'jpush-api-python-client'
        headers['connection'] = 'keep-alive'
        headers['content-type'] = 'application/json;charset:utf-8'

        general_log.debug("Making %s request to %s. Headers:\n\t%s\nBody:\n\t%s",
                     method, url, '\n\t'.join('%s: %s' % (key, value) for (key, value) in headers.items()), body)
        try:
            response = self.session.request(method, url, data=body, params=params,
                                            headers=headers, timeout=self.timeout,proxies=self.proxy )
        except requests.exceptions.ConnectTimeout:
            raise common.APIConnectionException("Connection to api.jpush.cn timed out.")
        except Exception:
            raise common.APIRequestException("Connection to api.jpush.cn error.")

        general_log.debug("Received %s response. Headers:\n\t%s\nBody:\n\t%s", response.status_code, '\n\t'.join(
                '%s: %s' % (key, value) for (key, value) in response.headers.items()), response.content)

        if response.status_code == 401:
            raise common.Unauthorized("Please check your AppKey and Master Secret")
        elif not (200 <= response.status_code < 300):
            raise common.JPushFailure.from_response(response)
        return response
    
def jiguang_push_message(uids,msg_title,msg_id) : # msg,msgid):
    """
    """
    #merchantname = inst.merchant.merchantname
    #push_cfg = settings.MERCHANT.get(merchantname).get('jpush')
    push_cfg = settings.JPUSH
    msg,msgid = msg_title,msg_id  #inst.title,inst.pk
    app_key,master_secret,proxy = push_cfg.get('app_key'),push_cfg.get('master_secret'),push_cfg.get('proxy') 
     
    for batch_uids in split_list(uids, 1000):
        _jpush = MyJpush(app_key, master_secret,proxy=proxy)
        push = _jpush.create_push()
        push.audience = jpush.audience(
                    jpush.alias(*batch_uids)
                )
        
        #push.message =  jpush.message(msg_content='',extras= {'message_id':msgid} )
        android = jpush.android(alert=msg,extras={'message_id':msgid})
        ios = jpush.ios(alert=msg,extras={'message_id':msgid},)
        push.notification = jpush.notification(alert= msg,android=android,ios=ios)
        push.options = {'apns_production':push_cfg.get('ios_production')}
        push.platform = jpush.all_
        try:
            general_log.info('发送推送命令:uids=%s'%batch_uids)
            response=push.send()
            general_log.info('推送消息:uids=%s ;返回结果: %s'%(batch_uids,response))
            #print(response)
        except jpush.common.JPushFailure as e:
            general_log.info('推送消息:uids=%s ;返回结果报错: %s'%(batch_uids,e))