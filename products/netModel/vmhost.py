#coding=utf-8

from products.netModel.monitorObj import MonitorObj
from products.netModel import medata
from products.netUtils.xutils import nbPath as _p

class Vmhost(MonitorObj):
    
    dbCollection = 'Vmhost'
    
    def __init__(self, uid=None):

        MonitorObj.__init__(self)
        self._medata.update(dict(
            commConfig=dict(
                netCommandCommandTimeout=30
            ), 
        ))
        
    host = medata.plain("host")
    port = medata.plain("port")
    username = medata.plain("username")
    password = medata.plain("password")
    commConfig = medata.Dictproperty("commConfig")
    title = medata.plain("title")
    vmhostCls  = medata.doc("vmhostClass")
    
    
    def getManageId(self):

        return self.host
    
    def addVirMachine(self):
        pass
    
    def getVirMachine(self):
        pass
    
    def removeVirMachine(self):
        pass
    
    def getCmd(self):

        parts = [_p("/bin/python") ,_p("/products/netCommand/pyexec/getVmhostData.py")]
        if self.host:
            parts.append('-h %s' % self.host)
        if self.port:
            parts.append('-o %s' % self.port)
        if self.username:
            parts.append('-u %s' % self.username)
        if self.password:
            parts.append("-p '%s'" % self.password)
            
        cmd = ' '.join(parts)
        return cmd
        