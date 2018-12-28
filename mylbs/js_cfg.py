from helpers.director.base_data import js_tr_list, js_lib_list
from django.utils.translation import ugettext as _
from helpers.maintenance.update_static_timestamp import js_stamp_dc

def get_tr():
    return {
    }

js_tr_list.append(get_tr)

def get_lib(request): 
    dc = {
        'gaode':'https://webapi.amap.com/maps?v=1.4.12&key=您申请的key值',
        'gaode_css': '',
        'mylbs':'/static/js/mylbs.pack.js?t=%s'%js_stamp_dc.get('mylbs_pack_js'),
    }
    return dc

js_lib_list.append(get_lib)