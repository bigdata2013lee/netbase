#coding=utf-8
from products.netModel.centerDocModel import CenterDocModel
from products.netModel import medata


class OperationServiceCustomer(CenterDocModel):
    "服务客户记录"
    dbCollection = 'OperationServiceCustomer'
    
    def __init__(self,uid=None):
        CenterDocModel.__init__(self)
        
    customer = medata.doc("customer") #服务客户
    engineer = medata.doc("engineer") #服务工程师
    operationer=medata.doc("operationer") #运维商
    
    remark = medata.plain("remark","") #备注
    serviceContext = medata.plain("serviceContext","") #服务内容说明

    
    

    
    
        
    