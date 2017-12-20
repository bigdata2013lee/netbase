#coding=utf-8
from products.netModel import medata
from products.netModel.monitorObj import MonitorObj

class MwBase(MonitorObj):
    def __init__(self):
        MonitorObj.__init__(self)
        self._medata.update(dict(
            commConfig=dict(
                netCommandCommandTimeout=180
            ), 
        ))

    middlewareClass  = medata.doc("middlewareClass") #中间件类

    commConfig = medata.Dictproperty("commConfig")

        
    def getManageId(self):
        """
         获取对象的管理Id
        """
        return self.host
        
    def getCmd(self):
        pass
    
    
    
    def getConnCount(self):
        "子类重写此方法，得到连接数"
        return 0
    
    
    @classmethod
    def getSubMwClss(cls):
        from products.netModel.middleware.mwApache import MwApache
        from products.netModel.middleware.mwTomcat import MwTomcat
        from products.netModel.middleware.mwNginx import MwNginx
        from products.netModel.middleware.mwIis import MwIis
        
        ctypes =  [MwApache,MwTomcat,MwNginx, MwIis]
        return ctypes


    @staticmethod
    def getSubMwCls(componentType):
        "通过组件类型名称， 获取中间件子类"
        ctypes =  MwBase.getSubMwClss()
        for ct in ctypes:
            if componentType == ct.__name__: return ct
        
        return None