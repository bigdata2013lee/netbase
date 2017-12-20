#coding=utf-8
from products.netModel.baseModel import DocModel
from products.netModel import medata

class ShareComment(DocModel):
    _allowCache = False
    dbCollection = 'ShareComment'
    
  
    
    def __init__(self):
        DocModel.__init__(self)
        self.__extMedata__(dict())

    topic=medata.doc("share")
    publisher=medata.doc("publisher")
    ctime = medata.plain("ctime",0)
    content = medata.plain("content","")
    approveNum = medata.plain("approveNum",0)
    reportNum = medata.plain("reportNum",0)
    approveIds = medata.plain("approveIds",[])
    reporterIds = medata.plain("reporterIds",[])