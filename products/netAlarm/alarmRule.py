#coding=utf-8
from products.netModel.baseModel import DocModel
from products.netModel import medata
import re



class AlarmRule(DocModel):
    dbCollection = 'AlarmRule'
    
    def __init__(self, uid=None):
        DocModel.__init__(self)
    
    enable = medata.plain("enable",True)
    alarmModel = medata.plain("alarmModel","email")#Sms|Email|APP
    alarmReceive = medata.plain("alarmReceive","") #告警接收者
    description = medata.plain("description","")
    conditionData = medata.plain("conditionData",{})
    ownCompany = medata.doc("ownCompany")
    
    @property
    def conditions(self):
        _conditionData = {}
        conditionData = self.conditionData
        keyWord =  conditionData.get("keyWord","")
        
        severitys = [ int(s) for s in conditionData.get("severity", ['3','4','5'])]
        _conditionData["severity"] = {"$in": severitys}
        
        firstType = conditionData.get("firstType", "")
        componentTypes = conditionData.get(firstType+ "_componentTypes", [])
        
        if componentTypes:
            _conditionData["componentType"] ={"$in": componentTypes} 
            
        
        if keyWord:
            _conditionData["message"] = re.compile(keyWord)

        if firstType == "device" and conditionData.get("deviceIps",""): #大类型 device, 并填写一个或多个ip
            deviceIps = conditionData.get("deviceIps","").split(",")
            _conditionData["deviceIp"]={"$in":deviceIps}
        
        _conditionData["last"] = conditionData["last"] #持续时间（分钟）未转义的条件
        
        return  _conditionData
        

    