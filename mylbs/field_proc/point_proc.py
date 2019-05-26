

from helpers.director.model_func.field_proc import BaseFieldProc
from django.contrib.gis.db import models
from helpers.director.base_data import field_map
from django.utils.translation import ugettext as _
from django.contrib.gis.geos import Polygon,Point

"""
一般是用于查询少于多少米内的记录

from django.contrib.gis.measure import D
# 少于3000m的东西
CarWashLocalModel.objects.filter(loc__distance_lte=(p1,D(m=3000)))
"""

class PointProc(BaseFieldProc):
    def to_dict(self, inst, name):
        point_value = getattr(inst,name)
        if point_value:
            value = '%s,%s'%(point_value.x,point_value.y)
        else:
            value = ''
        return { name :value}
    
    
    def clean_field(self, dc, name):
        vale = dc.get(name)
        if vale:
            x,y = vale.split(',')
            return Point(x=float(x),y=float(y),srid=4326)
        else:
            return None

field_map.update({
    models.PointField:PointProc
})