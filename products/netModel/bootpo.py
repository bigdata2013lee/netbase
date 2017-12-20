#coding=utf-8
from products.netUtils import xutils
from products.netModel import medata
from products.netModel.baseModel import BaseComponentModel
from products.netModel.eventSupport import EventSupport
ipmiConfig=dict(
        netIpmiUserName="root",
        netIpmiIp="",
        netIpmiPassword="netbase"
)

class Bootpo(EventSupport, BaseComponentModel):
    '''
    Bootpo
    '''
    dbCollection = 'Bootpo'
    
    def __init__(self, uid=None):
        BaseComponentModel.__init__(self)
        self._medata.update(dict(
            _id = uid,
            ipmiConfig = ipmiConfig,
        ))
        
    ipmiConfig = medata.Dictproperty("ipmiConfig")#已经没有IPMI端口了，放在通用配置的hcPort里了
    startUpIPMI = medata.plain("startUpIPMI", False)
    billing = medata.doc("billing") #认购单
    lastSentBootpoCmdTime = medata.plain("lastSentBootpoCmdTime", 0)
    
 
    
            