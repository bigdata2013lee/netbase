#coding=utf-8
from products.netModel.centerDocModel import CenterDocModel
from products.netModel import medata
import time

class Billing(CenterDocModel):
    """
    认购单
    """
    dbCollection = 'Billing'
    
    def __init__(self, uid=None):
        CenterDocModel.__init__(self)
        self.__extMedata__(dict( _id=uid))
    
    
    counts = medata.plain("counts",dict(Device=0,Website=0,Bootpo=0,ShortcutCmd=0,Network=0))
    
    ownCompany = medata.doc("ownCompany") #公司
    startTime = medata.plain("startTime",0) #起始时间
    endTime = medata.plain("endTime",0) #过期时间
    
    totalPrice = medata.plain("totalPrice", 0) #总价
    
    isvalid = medata.plain("isvalid", True) #有效，归档后，无效
    
    @classmethod
    def  isAvailableBilling(cls, b):
        if not b: return False
        if  not  b.isvalid: return False
        if time.time() >= b.endTime: return False
        return True 
    
    



    
        
        
