#coding=utf-8
from products.netModel.centerDocModel import CenterDocModel
from products.netModel import medata

class RechargeForm(CenterDocModel):
    dbCollection = 'RechargeForm'
    
    def __init__(self, uid=None):
        CenterDocModel.__init__(self)
        
        

    adminUser=medata.plain("adminUser", "")
    submitTime=medata.plain("submitTime", 0)
    completeTime=medata.plain("completeTime", 0)
    status=medata.plain("status", 0)
    money=medata.plain("money", 0)
    rechargeInstructions=medata.plain("rechargeInstructions","")
    
    saleUser = medata.doc("saleUser")
    customer = medata.doc("customer")
    
    
    