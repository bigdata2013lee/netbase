#coding=utf-8

from products.netModel import medata
from products.netModel.devComponents.base import DeviceComponent


class Process(DeviceComponent):
    dbCollection = 'Process'
    
    def __init__(self, uid=None):
        DeviceComponent.__init__(self)
        self.__extMedata__({})

    procName = medata.plain("procName","")
    procPath = medata.plain("procPath", "")
    snmpIndex = medata.plain("snmpIndex", 0)
    parameters = medata.plain("parameters")
    
    
    
    def getCpu(self):
        "cpu利用率"
        return self.getPerfValue("OSProcess", "ps", "cpu")
        
    def getMem(self):
        "mem利用率"
        return  self.getPerfValue("OSProcess", "ps", "mem")
    
    