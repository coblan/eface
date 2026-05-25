from director.base_data import js_tr_list, js_lib_list, js_stamp_dc
#from django.utils.translation import ugettext as _
#from .maintenance.update_static_timestamp import js_stamp_dc

def get_tr():
    return {
    }

js_tr_list.append(get_tr)

def get_lib(request): 
    dc = {
        'wechat':'/static/js/wechat.pack.js?t=%s&v=8'%js_stamp_dc.get('wechat_pack_js'),
    }
    return dc

js_lib_list.append(get_lib)