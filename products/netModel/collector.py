#coding=utf-8

import random
from products.netModel.baseModel import DocModel
from products.netModel import medata
from products.netPublicModel.collectorClient import ColloectorCallClient
from products import sysStaticConf


class Collector(DocModel):
    
    dbCollection = 'Collector'
    
    def __init__(self, uid=None):
        DocModel.__init__(self)
        self._medata.update(dict(
            _id = uid,
        ))

    host = medata.IPproperty("host", "127.0.0.1")
    mac = medata.plain("mac","")  #
    status = medata.plain("status",None)
    collType = medata.plain("collType","public")  #public|private
    bootpoPort = medata.plain("bootpoPort", 12305)
    tcpServerPort =medata.plain("tcpServerPort", 12368)
    ownCompany = medata.doc("ownCompany")#将收集器与用户关联,public没有公司
        

    @classmethod
    def _loadByHost(cls, hostIp):
        objs = cls._findObjects(conditions={"host":hostIp}, limit=1)
        if(objs): return objs[0]
        return None        
    
    @property
    def devices(self):
        """
        get devices 获取属于该收集器的设备
        @return: 设备list
        """
        from products.netModel.device import Device
        return self._getRefMeObjects('collector', Device)
    
    @property
    def websites(self):
        """
        get websites 获取属于该收集器的站点
        @return: 站点list
        """
        from products.netModel.website import Website
        return self._getRefMeObjects('collector', Website)
    @property
    def mwApaches(self):
        """
        get Middleware 获取属于该收集
        @return: Apachelist
        """
        from products.netModel.middleware.mwApache import MwApache
        return self._getRefMeObjects('collector', MwApache)
    @property
    def mwNginxs(self):
        """
        get Middleware 获取属于该收集
        @return: Nginxlist
        """
        from products.netModel.middleware.mwNginx import MwNginx
        return self._getRefMeObjects('collector', MwNginx)
    @property
    def mwTomcats(self):
        """
        get Middleware 获取属于该收集
        @return: tomcatlist
        """
        from products.netModel.middleware.mwTomcat import MwTomcat
        return self._getRefMeObjects('collector', MwTomcat)
    
    
    @property
    def mwIiss(self):
        """
        get Middleware 获取属于该收集
        @return: Iislist
        """
        from products.netModel.middleware.mwIis import MwIis
        return self._getRefMeObjects('collector', MwIis)
    
    @property
    def networks(self):
        """
        网络设备：如思科，华为相关设备 
        """
        from products.netModel.network import Network
        return self._getRefMeObjects("collector", Network)
    

        
    
    def getAllMonitorObjs(self):
        """
                        获取收集器所有的监控对象
        """
        objs = []
        
        objs.extend(self.devices)
        objs.extend(self.websites)
        objs.extend(self.networks)
        objs.extend(self.mwApaches)
        objs.extend(self.mwNginxs)
        objs.extend(self.mwTomcats)
        objs.extend(self.mwIiss)
        return objs
        
        
        
    def getMonitorObj(self, uid, componentType):
        """
        通过UID, 及组件类型，获取监控对象
        @param uid:
        @param componentType:  
        
        @note: 没有通过收集器ID进一步过滤
        """
        _clss = self.getMainMonitorClss()
        
        for cls in _clss:
            if componentType == cls.getComponentType():
                return cls._loadObj(uid)
            
        return None
    
    
    
    @classmethod
    def getMainMonitorClss(cls):
        "获取主监控对象类"
        from products.netModel.device import Device
        from products.netModel.website import Website
        from products.netModel.network import Network
        from products.netModel.middleware.mwBase import MwBase
        from products.netModel.bootpo import Bootpo
        
        _clss = [Device, Website, Network, Bootpo] + MwBase.getSubMwClss()
        return _clss
    
    @classmethod
    def getFreeCollector(cls, componentType):
        """
        仅限于公有-public收集器
        选择一个空闲的收集器
        空闲是指添加的某类主要的监控对象未达到一定的上限数，上限数在服务器的配置文件中设置
        """
        collectors = cls._findObjects(conditions={"collType":"public"})

        mClss = cls.getMainMonitorClss()
        defaults = sysStaticConf.get("colloectorCapacity", "defaults", 500)
        
        def _getMonitorCls():
            for mcls in mClss:
                if componentType == mcls.getComponentType(): return mcls
            return None
        
        
        mcls = _getMonitorCls()
        if not collectors:return None
        
        col = random.choice(collectors)
        if not mcls: return col
        
        
        def _getCol(col):
            count = mcls._countObjects({"collector": col._getRefInfo()})
            maxCount = sysStaticConf.get("colloectorCapacity", mcls.getComponentType(), defaults)
            if count < maxCount: return col
            return None
        
        
        if _getCol(col): return col
        for col in collectors:
            if _getCol(col):
                return col
            
        return None
    
    
    @classmethod
    def getFreeCollectors(cls, componentType):
        """
        获取空闲的收集器列表
        仅限于公有-public收集器
        """
        collectors = cls._findObjects(conditions={"collType":"public"})

        mClss = cls.getMainMonitorClss()
        defaults = sysStaticConf.get("colloectorCapacity", "defaults", 500)
        
        def _getMonitorCls():
            for mcls in mClss:
                if componentType == mcls.getComponentType(): return mcls
            return None
        
        
        mcls = _getMonitorCls()
        if not collectors:return []
        
        if not mcls: return []
        
        
        def _getCol(col):
            count = mcls._countObjects({"collector": col._getRefInfo()})
            maxCount = sysStaticConf.get("colloectorCapacity", mcls.getComponentType(), defaults)
            if count < maxCount: return col
            return None
        
        
        rs = []
        for col in collectors:
            if _getCol(col):
                rs.append(col)

        return rs
        
    
    def collectorConn(self):
        """
                收集器的联通性
        """
        try:
            cCall = ColloectorCallClient(self.host, timeout=10)
            result = cCall.call("CollVerify")
        except:
            return False
        return result.get("data", False)
        
if __name__=="__main__":
    s=Collector.getFreeCollector("Device")
    print s
        
        
        
        
