from .models import TWXOrder
from helpers.director.shortcut import TablePage,ModelTable,page_dc,director,RowFilter

class WXorderPage(TablePage):
    def get_label(self):
        return '微信订单'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table_new.html'
    
    class tableCls(ModelTable):
        model = TWXOrder
        exclude =[]
        
        class filters(RowFilter):
            names =['confirmed']
            range_fields =['create_time']

director.update({
    'wxorder':WXorderPage.tableCls,
})

page_dc.update({
    'wxorder':WXorderPage
})