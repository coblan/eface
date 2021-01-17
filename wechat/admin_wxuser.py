from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,SelectSearch
from django.contrib.auth.models import User
from eface.wechat.models import WxInfo
#from helpers.case.jb_admin.admin import UserFields
from helpers.case.jb_admin.admin_user import UserFields

from helpers.director.shortcut import field_map,model_to_name
from helpers.director.model_func.field_procs.charproc import CharProc
from django.conf import settings
import binascii

class wxuser(TablePage):
    def get_label(self):
        return '微信用户'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = WxInfo
        exclude=[]
        hide_fields=['user']
        
        def getExtraHead(self):
            userfomr = UserFields()
            fields_ctx =userfomr.get_pop_edit_ctx(getrow='{pk:scope.vc.par_row.user}')
            return [
                {'name':'username','label':'账号','editor':'com-table-click',
                 'fields_ctx':fields_ctx,
                 'action':fields_ctx.get('action')
                 #'''var fctx=scope.head.fields_ctx;fctx.par_row=scope.row;fctx.row={pk:scope.row.user};cfg.pop_vue_com("com-form-one",scope.head.fields_ctx) ''' 
                 }
            ]
        
        def dict_head(self, head):
            width_dc ={
                'openid':150,
                'nickname':150,
                'head':120,
                'username':160,
            }
            if width_dc.get(head['name']):
                head['width'] = width_dc.get(head['name'])
            return head
        
        def dict_row(self, inst):
            return {
                'username': str(inst.user), #inst.user.username,
                'nickname': inst.dbNickname #base64.b64decode( inst.nickname ).decode('utf-8')
            }
        
        class search(SelectSearch):
            names = ['nickname']
 
class NicknameProc(CharProc):
    def filter_clean_search(self, q_str):
        isbase64 = getattr(settings,'WX_NICKNAME_HEX',False)
        if isbase64:
            return binascii.b2a_hex( q_str.encode('utf-8') )
        else:
            return q_str
   
field_map.update({
    '%s.nickname'%model_to_name(WxInfo):NicknameProc
})  
      
def wxinfo2user(pk):
    wxinfo = WxInfo.objects.get(pk=pk)
    myform = UserFields(instance = wxinfo.user)
    return myform.get_row()


director.update({
    'wxuserinfo':wxuser.tableCls,
    'wxuserinfo2user':wxinfo2user
})

page_dc.update({
    'wxuserinfo':wxuser
})