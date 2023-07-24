

from helpers.director.model_func.field_proc import BaseFieldProc
from django.contrib.gis.db import models
from helpers.director.base_data import field_map
from django.utils.translation import ugettext as _
from django.contrib.gis.geos import Polygon,Point
import base64
from helpers.func.geo import dict2poly ,poly2dict
import json

"""
一般是用于查询少于多少米内的记录

from django.contrib.gis.measure import D
# 少于3000m的东西
CarWashLocalModel.objects.filter(loc__distance_lte=(p1,D(m=3000)))
"""

class PolygenProc(BaseFieldProc):
    
    def dict_field_head(self,head): 
        head['editor'] = 'com-field-json-edit'
        head['help_text'] ='格式:[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]'
        head['default_value_express'] = 'rt=[]'
        #express = base64.b64encode("""
        #var ls = scope.value.split(',')
        #if(ls.length !=2){
            #rt = false;
        #}else{
        #var longrg = /^(\-|\+)?(((\d|[1-9]\d|1[0-7]\d|0{1,3})\.\d{0,6})|(\d|[1-9]\d|1[0-7]\d|0{1,3})|180\.0{0,6}|180)$/;
        #var latreg = /^(\-|\+)?([0-8]?\d{1}\.\d{0,6}|90\.0{0,6}|[0-8]?\d{1}|90)$/;
        #rt = latreg.test(ls[0]) && longrg.test(ls[1])
        #}
       
        #""".encode('utf-8'))
        #msg = base64.b64encode('经纬度格式不正确'.encode('utf-8'))        
        #head['fv_rule']='express(%s , %s),'%( express.decode('utf-8'),msg.decode('utf-8'))
        #head['placeholder']='lat,log'
        return head
    
    def to_dict(self, inst, name):
        point_value = getattr(inst,name)
        if point_value:
            value =poly2dict(point_value) # '%s,%s'%(point_value.y,point_value.x)
        else:
            value = ''
        return { name :value}
    
    
    def clean_field(self, dc, name):
        """按照geoJson规范，前端传递字符串经纬度顺序:lat,lon;写入点的时候需要切换x,y """
        vale = dc.get(name)
        if vale:
            if isinstance(vale,str):
                ls = json.loads(vale)
            else:
                ls = vale
            return dict2poly(ls)
        else:
            return None

field_map.update({
    models.PolygonField:PolygenProc
})