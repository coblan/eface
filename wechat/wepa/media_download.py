import requests
from .funs import get_access_token
from django.conf import settings
import os

def download_media(media_id):
    access_token = get_access_token()
    url = 'http://file.api.weixin.qq.com/cgi-bin/media/get?access_token=%(access_token)s&media_id=%(media_id)s'\
        %{'access_token':access_token,'media_id':media_id}
    rt = requests.get(url)
    if rt.status_code !=200:
        raise UserWarning('下载微信媒体文件发生错误')
    path = os.path.join(settings.MEDIA_ROOT,'wechat')
    try:
        os.makedirs(path)
    except:
        pass
    sufix = rt.headers.get('Content-Type').split('/')[1]
    fl_path = os.path.join(path,media_id+'.'+sufix)
    with open(fl_path,'wb') as f:
        f.write(rt.content)
    
    return '/media/wechat/%(fl_name)s'%{'fl_name':media_id+'.'+sufix}
