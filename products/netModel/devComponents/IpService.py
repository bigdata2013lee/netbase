#coding=utf-8

from products.netModel import medata
from products.netModel.devComponents.base import DeviceComponent
from products.netModel.baseModel import RefDocObject

class IpService(DeviceComponent):
    """
    @note: uname格式 协议_端口
    """
    dbCollection = 'IpService'
    
    def __init__(self, uid=None):
        DeviceComponent.__init__(self)
        self._medata.update(dict(
            collectPoints=[]#收集点
        ))

#-------------------------------------------------------------------------
    
    protocol = medata.plain("protocol", "tcp")
    port = medata.plain("port", 0)
#---------------------------------------------------------------------------


    @property
    def collectPoints(self):
        "get collectPoints"
        collectPoints=self._medata['collectPoints']
        return [RefDocObject.getInstance(collectPoint) 
                                    for collectPoint in collectPoints]
    
    @collectPoints.setter
    def collectPoints(self, collectPoints):
        "set collectPoints"
        self._medata["collectPoints"] = [collectPoint._getRefInfo() 
                                    for collectPoint in collectPoints]
        self._saveObj()


