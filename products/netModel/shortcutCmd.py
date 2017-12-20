#coding=utf-8
from products.netModel import medata
from products.netModel.baseModel import DocModel

class ShortcutCmd(DocModel):
    dbCollection = 'ShortcutCmd'
    

    
    def __init__(self):
        DocModel.__init__(self)
        self.__extMedata__(dict())
    
    
    
    cmd = medata.plain("cmd","")
    targetDev = medata.doc("targetDev")
    lastExecuteTime = medata.plain("lastExecuteTime", 0) #上次执行时间(时间戳/秒)
    ownCompany = medata.doc("ownCompany") #公司
    billing = medata.doc("billing")
    
        