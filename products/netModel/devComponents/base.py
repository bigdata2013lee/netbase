#coding=utf-8
from products.netModel.monitorObj import MonitorObj
from products.netModel import medata

class DeviceComponent(MonitorObj):
    
    def __init__(self):
        MonitorObj.__init__(self)
        self.__extMedata__({"uname": None})
        
    device = medata.doc("device")
    
    def  titleOrUid(self):
        return self.title or self.uname or self.getUid()
    
    @property
    def uname(self):
        return self._medata.get("uname")
    
    @property
    def collector(self):
        if self.device:
            return self.device.collector
        
        return None
    
    
        
    