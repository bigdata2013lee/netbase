#coding=utf-8
from products.netModel import medata
from products.netUtils.xutils import getDeviceSnmpAndCommDefaultConfig
from products.netModel.middleware.mwBase import MwBase
class MwIis(MwBase):
    dbCollection = 'MwIis'
    def __init__(self, uid=None):
        MwBase.__init__(self)
        self._medata.update(dict(
            wmiConfig = getDeviceSnmpAndCommDefaultConfig().get("wmiConfig"),
        ))

    host = medata.plain("host","")
    port = medata.plain("port",80)
    wmiConfig = medata.Dictproperty("wmiConfig")
    
    @property
    def manageIp(self):
        """
                管理IP
        (设备配置统一化,添加manageIp获取方式)
        """
        return self.host
    
    
    def getConnCount(self):
        tplName = self.getBaseTemplate().getUid()
        return self.getPerfValue(tplName,"W3SVC_Perf", "CurrentConnections")
    
    def getCmd(self):
        """
          to get IIS version
        """
        cmd = "curl -I http://%s:%s" %(self.host,self.port)
        return cmd
    