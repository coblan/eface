from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director
from django.contrib.auth.models import User
from eface.wechat.models import WxInfo
import base64
from helpers.case.jb_admin.admin import UserFields
 
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
            return [
                {'name':'username','label':'账号','editor':'com-table-click',
                 'heads':userfomr.get_heads(),
                 'ops':userfomr.get_operations(),
                 'action':''' cfg.pop_vue_com({editor:"com-form-one", ctx:{
                 init_express:'ex.director_call("wxuserinfo2user",{pk:scope.vc.par_row.pk}).then((row)=>{ex.vueAssign(scope.vc.row,row)})',
                 heads:scope.head.heads,ops:scope.head.ops,ops_loc:"bottom",row:{pk:scope.row.user},par_row:scope.row}}) ''' }
            ]
        
        def dict_row(self, inst):
            return {
                'username':inst.user.username,
                'nickname':base64.b64decode( inst.nickname ).decode('utf-8')
            }
        
      
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