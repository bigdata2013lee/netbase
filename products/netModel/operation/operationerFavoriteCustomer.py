#coding=utf-8
from products.netModel.centerDocModel import CenterDocModel
from products.netModel import medata


class OperationFavoriteCustomer(CenterDocModel):
    "收藏客户记录"
    dbCollection = 'OperationFavoriteCustomer'
    
    def __init__(self,uid=None):
        CenterDocModel.__init__(self)
        
    customer = medata.doc("customer") #服务客户
    operationer=medata.doc("operationer") #运维商
    
    remark = medata.plain("remark","") #血液信息