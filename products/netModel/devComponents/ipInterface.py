#coding=utf-8

from products.netModel import medata
from products.netModel.devComponents.base import DeviceComponent


class IpInterface(DeviceComponent):
    
    dbCollection = 'IpInterface'
    
    def __init__(self, uid=None):
        DeviceComponent.__init__(self)

#-------------------------------------------------------------------------
    
    adminStatus = medata.plain("adminStatus", 1)
    operStatus = medata.plain("operStatus", 1)
    
    ipAddress = medata.IPproperty("ipAddress") #ip
    macAddress = medata.plain("macAddress") #mac地址
    type = medata.plain("type", "ethernetCsmacd") #类型
    speed = medata.plain("speed", 100) #速率
    customSpeed = medata.plain("customSpeed", 0) #自定义速率
    snmpIndex = medata.plain("snmpIndex") #snmp索引
    mtu = medata.plain("mtu")
    description = medata.plain("description") 
    
#---------------------------------------------------------------------------
  

        
    def getStatus(self):
        "获取业务/操作状态"
        val = self.getPerfValue("ethernetCsmacd", "Status", "ifOperStatus")
        if val == 2: return "down"
        elif val == 1: return "up"
        return "unknown"

        
    def getThroughValues(self):
        """
        获取接口进出流量
        """
        _input = self.getPerfValue("ethernetCsmacd", "Throughs", "ifInOctets")
        _output = self.getPerfValue("ethernetCsmacd", "Throughs", "ifOutOctets")
        return {'input':_input, 'output':_output}
    
    
    def getThroughRates(self):
        rs = {"inputRate":None, "outputRate":None}
        tvs = self.getThroughValues()
        if not tvs:return rs
        
        customSpeed = self.getCustomSpeed
        if not customSpeed:customSpeed=1
        ipt=tvs.get("input",0)
        if not ipt:ipt=0
        opt=tvs.get("output",0)
        if not opt:opt=0

        rs["inputRate"] = float(ipt/customSpeed*100)
        rs["outputRate"] = float(opt/customSpeed*100)
        return rs
        

    
    @property
    def getCustomSpeed(self):
        """
        得到自定义速度
        """
        if self.customSpeed:
            return int(self.customSpeed)*100000
        return self.speed
