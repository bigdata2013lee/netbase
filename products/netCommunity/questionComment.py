#coding=utf-8
from products.netModel import medata
from products.netModel.baseModel import DocModel

class QuestionComment(DocModel):
    _allowCache = False
    dbCollection = 'questionComment'
    
    topic=medata.doc("question")
    publisher=medata.doc("publisher")
    ctime = medata.plain("ctime",0)
    content = medata.plain("content","")
    approveNum = medata.plain("approveNum",0)
    reportNum = medata.plain("reportNum",0)
    approveIds = medata.plain("approveIds",[])
    reporterIds = medata.plain("reporterIds",[])     
    accept = medata.plain("accept",False)
     
    def __init__(self):
        DocModel.__init__(self)
        self.__extMedata__(dict())
    
  

    
    
    
    
        
        