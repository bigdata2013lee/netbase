#coding=utf-8
'''
Created on 2013-8-29

@author: root
'''
import pickle
from products.netPublicModel.baseConfigModel import ConfigServiceModel
from products.netPublicModel.modelManager import ModelManager
from products.netAlarm import alarmRecord,alarmRule

class AlarmConfig(ConfigServiceModel):
    
    def remoteEevent(self,conditions={}):
        dr=ModelManager.getMod("eventManager")
        Events = dr.findCurrentEvents(conditions=conditions)
        return pickle.dumps(Events)
    
    def remoteRecordObj(self):
        return  pickle.dumps(alarmRecord.AlarmRecord()) 
    
    def remoteRules(self,conditions={}):
        rule=alarmRule.AlarmRule._findObjects(conditions=conditions)
        return pickle.dumps(rule)
      
    def remoteRecords(self,conditions={}):
        records=alarmRecord.AlarmRecord._findObjects(conditions=conditions)
        return pickle.dumps(records)  
