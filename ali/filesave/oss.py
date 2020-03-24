import oss2
from helpers.director.views import GeneralUpload
from django.conf import settings
import os
import urllib

#{
    #'access_key_id':'',
    #'access_key_secret':'',
    #'endpoint':'http://oss-cn-chengdu.aliyuncs.com',
#}

class AliOssUpload(GeneralUpload):
    "接收media文件"
    def procFile(self,file_data,fl):
        par_dir = self.getParDir() + '/'
        file_name = self.getFileName(file_data,fl)
        file_path = urllib.parse.urljoin(par_dir,file_name)
        
        #absolut_par_path = os.path.join( settings.MEDIA_ROOT, par_dir)
        #try:
            #os.makedirs(absolut_par_path)
        #except os.error as e:
            #print(e)   
        
        #absolut_file_path =os.path.join(absolut_par_path,file_name)
        
        auth = oss2.Auth(settings.MEDIA_SAVER.get('access_key_id'), settings.MEDIA_SAVER.get('access_key_secret'))
        bucket = oss2.Bucket(auth,settings.MEDIA_SAVER.get('endpoint') , settings.MEDIA_SAVER.get('bucket'))
        rt = bucket.put_object(file_path,file_data)
        if rt.status == 200:
            return self.getFileUrl(file_path)
        else:
            raise UserWarning('上传阿里云出错')

    def getFileUrl(self, file_path):
        file_url = file_path.replace('\\', '/')
        absolute_file_url=urljoin(settings.MEDIA_SAVER.get('media_url'), file_url)
        return  absolute_file_url   


def put_file(local_path,remote_url):
    "利用MEDIA_SAVER设置,上传文件到oss，一般用于手动转移media"
    auth = oss2.Auth(settings.MEDIA_SAVER.get('access_key_id'), settings.MEDIA_SAVER.get('access_key_secret'))
    bucket = oss2.Bucket(auth,settings.MEDIA_SAVER.get('endpoint') , settings.MEDIA_SAVER.get('bucket'))
    rt = bucket.put_object_from_file(remote_url,local_path)
    if rt.status == 200:
        return urljoin(settings.MEDIA_SAVER.get('media_url'), remote_url)
    else:
        raise UserWarning('上传阿里云出错')
    