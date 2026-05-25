from director.shortcut import LivePage,ModelTable,ModelFields,page_dc,director,SelectSearch,RowFilter
from django.contrib.auth.models import User
from eface.wechat.models import WxInfo
#from helpers.case.jb_admin.admin import UserFields
#from helpers.case.jb_admin.admin_user import UserFields

#from director.shortcut import field_map,model_to_name
from director.fields.modelfields import field_map
from director.model_func.model_info import model_to_name

from director.model_func.field_procs.charproc import CharProc
from django.conf import settings
import binascii
#from helpers.case.jb_admin.uidict import pop_edit_current_row
from director.func .dot_dict import read_dict_path
from django.db.models import Q

class wxuser(LivePage):
    def get_label(self):
        return '微信用户'
    
    def get_context(self):

        return {
            'editor':'com-live-table',
             'editor_ctx':{
                 'tableCtx':WxInfoTable().get_head_context()
             }
        }
    
class WxInfoTable(ModelTable):
    model = WxInfo
    exclude=[]
    pop_edit_fields=['id']
    allow_create = False
    allow_delete = read_dict_path(settings,'WXMINI_APP.wxinfo_delete',False)
    #hide_fields=['user']
    
    
    #def getExtraHead(self):
        #return [
            #{'name':'username',
             #'label':'账号',
             #'editor':'com-table-span',
             ##'click_express':pop_edit_current_row(),
             ##'fields_ctx':UserFields().get_head_context(),
             ##'class':'clickable'
             #}
        #]
        
            #if head['name'] =='preordainprice':
                #head['css']='.clickable{cursor:point}'
                #head['inn_editor'] =  head['editor']
                #head['editor']='com-table-rich-span'
                #head['class']='middle-col btn-like-col'
                #head['cell_class'] = 'if(parseFloat( scope.row.preordainprice ) >0){rt="warning clickable" }else{rt="clickable"}'  
                #head['click_express'] =  pop_edit_current_row()
                #head['fields_ctx'] = PreorderPriceForm().get_head_context()            
    #def getExtraHead(self):
        #userfomr = UserFields()
        #fields_ctx =userfomr.get_pop_edit_ctx(getrow='{pk:scope.vc.par_row.user}')
        #return [
            #{'name':'username','label':'账号',
             #'editor':'com-table-click',
             #'fields_ctx':fields_ctx,
             #'action':fields_ctx.get('action')
             ##'''var fctx=scope.head.fields_ctx;fctx.par_row=scope.row;fctx.row={pk:scope.row.user};cfg.pop_vue_com("com-form-one",scope.head.fields_ctx) ''' 
             #}
        #]
    
    def dict_head(self, head):
        width_dc ={
            'user':200,
            'openid':150,
            'nickname':150,
            'head':120,
            'username':160,
        }
        if width_dc.get(head['name']):
            head['width'] = width_dc.get(head['name'])
        return head
    
    #def dict_row(self, inst):
        #return {
            #'username':  str(inst.user), #.username, #inst.user.username,
            #'nickname': inst.nickname #  inst.dbNickname #base64.b64decode( inst.nickname ).decode('utf-8')
        #}
    
    class filters(RowFilter):
        names =['phone']
        icontains=['phone']
    
    class search(SelectSearch):
        names = ['nickname','user__username']
        label_map={
            'user__username':'用户账号',
        }
        def get_query(self,query):
            if self.qf=='user__username' and self.q:
                return query.filter(Q(user__username=self.q) | Q(user__first_name=self.q))
            else:
                return super().get_query(query)
                    
            
            
 
class NicknameProc(CharProc):
    def filter_clean_search(self, q_str):
        isbase64 = getattr(settings,'WX_NICKNAME_HEX',False)
        if isbase64:
            return binascii.b2a_hex( q_str.encode('utf-8') )
        else:
            return q_str

class WxinfoForm(ModelFields):
    class Meta:
        model = WxInfo
        exclude =[]

field_map.update({
    '%s.nickname'%model_to_name(WxInfo):NicknameProc
})  
      
#def wxinfo2user(pk):
    #wxinfo = WxInfo.objects.get(pk=pk)
    #myform = UserFields(instance = wxinfo.user)
    #return myform.get_row()


director.update({
    'wxuserinfo':WxInfoTable,
    'wxuserinfo.edit':WxinfoForm,
    #'wxuserinfo2user':wxinfo2user,
    
})

page_dc.update({
    'wxuserinfo':wxuser
})