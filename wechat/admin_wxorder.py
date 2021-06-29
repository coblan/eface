from .models import TWXOrder
from helpers.director.shortcut import TablePage,ModelTable,page_dc,director,RowFilter,SelectSearch

class WXorderPage(TablePage):
    def get_label(self):
        return '微信订单'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table_new.html'
    
    class tableCls(ModelTable):
        model = TWXOrder
        exclude =[]
        
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
            names = ['user__first_name']
            
            def get_option(self, name):
                dc = {
                    'user__first_name':'用户'
                }
                return {'value':name,'label':dc[name]}

director.update({
    'wxorder':WXorderPage.tableCls,
})

page_dc.update({
    'wxorder':WXorderPage
})