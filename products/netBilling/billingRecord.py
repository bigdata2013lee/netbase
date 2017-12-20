#coding=utf-8
from products.netModel.baseModel import DocModel
from products.netModel import medata

class BillingRecord(DocModel):
    dbCollection = 'BillingRecord'
    
    def __init__(self, uid=None):
        DocModel.__init__(self)
        
    time = medata.plain("time", 0)
    ownCompany = medata.doc("ownCompany") #公司
    itemName = medata.plain("itemName", "") #收入、支出项目名称
    itemMoney = medata.plain("itemMoney", 0) #收入、支出项目金额