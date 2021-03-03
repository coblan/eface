from helpers.director.base_data import js_tr_list, js_lib_list
from django.utils.translation import ugettext as _
from helpers.maintenance.update_static_timestamp import js_stamp_dc

def get_tr():
    return {
    }

js_tr_list.append(get_tr)

def get_lib(request): 
    dc = {
        'my_gaode': '/static/js/gaode.pack.js?t=%s'%js_stamp_dc.get('gaode_pack_js'),
        'gaode_map':'https://webapi.amap.com/maps?v=1.4.15&key=0909294a753dfe00a0aa124b6ecb93eb',
        'gaode_loca':'https://webapi.amap.com/loca?key=0909294a753dfe00a0aa124b6ecb93eb&v=1.3.0'
    }
    return dc

js_lib_list.append(get_lib)