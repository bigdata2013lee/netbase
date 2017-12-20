#coding=utf-8


import time
from products.netEvent.settings import eventConfig
from products.netPublicModel.modelManager import ModelManager
from products.netTasks import NetbaseSysTask
from products.netEvent.event import Event

def clearExpireEvent(evtMgr):
    conditions = {
        "historical":False,
        "endTime": {'$lte': time.time()-eventConfig.get('currentEvtExpireTime') }
    }
    events = evtMgr.findEvents(conditions=conditions)
    for evt in events: evtMgr.currentEvent2Histroy(evt) #当前事件转历史
    
    #删除到期的事件
    Event._getDbTable().remove({"endTime":{"$lte":time.time() - eventConfig.get('maxSaveTime')}})

class Task(NetbaseSysTask):
    
    def __runService__(self):
        evtmgr = ModelManager.getMod('eventManager')
        while True:
            clearExpireEvent(evtmgr)
            time.sleep(60*60)
        


        

