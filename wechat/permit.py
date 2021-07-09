from helpers.director.shortcut import model_to_name, model_full_permit, add_permits, model_read_permit
from .models import *

permits=[
    
    ('WxInfo',model_read_permit(WxInfo),model_to_name(WxInfo),'model'),
    ('WxInfo.edit', model_full_permit(WxInfo), model_to_name(WxInfo), 'model' ),
    
    ('TWXOrder',model_read_permit(TWXOrder),model_to_name(TWXOrder),'model'),
    ('TWXOrder.edit', model_full_permit(TWXOrder), model_to_name(TWXOrder), 'model' ),    

]
add_permits(permits)