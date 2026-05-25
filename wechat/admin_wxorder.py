from .models import TWXOrder
from director.shortcut import LivePage,ModelTable,page_dc,director,RowFilter,SelectSearch
from director.ui.excel_btn import op_excel

class WXorderPage(LivePage):
    def get_label(self):
        return '微信订单'
    
    def get_context(self):
        
        return {
            'editor':'com-live-table',
             'editor_ctx':{
                 'tableCtx':TWXOrderTable().get_head_context()
             }
        }  
    
class TWXOrderTable(ModelTable):
    model = TWXOrder
    exclude =[]
    
    def get_operations(self):
        return [
            op_excel()
        ]
    def dict_head(self, head):
        width = {
            'user':150,
            'transaction_id':100,
        }
        if head['name'] in width:
            head['width'] = width[head['name']]
        if head['name']=='id':
            head['after_fields'] = ['user','confirmed','total_fee']
        return head
    
    class filters(RowFilter):
        names =['confirmed']
        range_fields =['create_time']
    
    class search(SelectSearch):
        names = ['user__wxinfo__phone','user__first_name']
        
        def get_option(self, name):
            dc = {
                'user__first_name':'用户昵称',
                'user__wxinfo__phone':'用户手机'
            }
            return {'value':name,'label':dc[name]}

director.update({
    'wxorder':TWXOrderTable,
})

page_dc.update({
    'wxorder':WXorderPage
})