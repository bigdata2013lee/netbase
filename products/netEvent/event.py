#coding=utf-8

from products.netModel.baseModel import DocModel
from products.netModel import  mongodbManager as dbManager, medata
from products.netUtils import xutils



class EventDocModel(DocModel):
    _allowCache = False
    
    def __init__(self):
        DocModel.__init__(self)
    
    @classmethod
    def _getDbTable(cls):
        """
        得到当前对象的mongodb集合表
        """
        db = dbManager.getNetEventDB()
        table = getattr(db, getattr(cls,"dbCollection","") or cls.__name__)
        return table
    
class EventBase(EventDocModel):
    
    def __init__(self, uid=None):
        EventDocModel.__init__(self)

        
    moUid = medata.plain("moUid")
    componentType = medata.plain("componentType","")
    evtKey = medata.plain("evtKey")
    evtKeyId = medata.plain("evtKeyId","")
        
    clearId = medata.plain("clearId","")
    label = medata.plain("label","")
    message = medata.plain("message","")
    eventState = medata.plain("eventState",xutils.eventStates['unacknowledge'])
    severity = medata.plain("severity",3)
    firstTime = medata.plain("firstTime",3)
    endTime = medata.plain("endTime",3)
    count = medata.plain("count",1)
    
    agent = medata.plain("agent")
    collector = medata.plain("collector")
    historical = medata.plain("historical", False)
                            
class Event(EventBase):
    dbCollection = "events"
    
    def __init__(self, uid=None):
        EventBase.__init__(self, uid)
        

    
