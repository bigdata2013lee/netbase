#coding=utf-8
'''
Created on 2012-12-3
@author: root
'''
import types
from products.netUtils import xutils
from products.netModel import medata
from products.netModel.monitorObj import MonitorObj
from products.netModel.templates.template import Template
from products.netModel.eventSupport import DeviceEventSupport
from products.netModel.devComponents.ipInterface import IpInterface
from products.netUtils.xutils import getDeviceSnmpAndCommDefaultConfig



class Network(DeviceEventSupport, MonitorObj):
    '''
    Network设备
    '''
    dbCollection = 'Network'
    
    def __init__(self, uid=None):
        '''
        Constructor
        '''
        MonitorObj.__init__(self)
        self.__extMedata__(getDeviceSnmpAndCommDefaultConfig())
        
#----------------------------------属性---------------------------------------------------#
    networkCls  = medata.doc("networkCls") #网络类
    location=medata.doc("location")
    manageIp = medata.plain("manageIp") #管理IP
    productId = medata.plain("productId") #产品型号 格式(厂商__产品编号)
    snmpConfig = medata.Dictproperty("snmpConfig")
    commConfig = medata.Dictproperty("commConfig")
    billing = medata.doc("billing") #认购单
    
    def getManageId(self):
        """
        获取设备对象的管理Id
        """
        return self.manageIp
        
    def getSysUpTime(self):
        "运行时间"
        baseTemplate=self.getBaseTemplate()
        if not baseTemplate:return {}
        tplName = baseTemplate.getUid()
        return self.getPerfValue(tplName, "SysUpTime", "UpTime")
        
    
    def getCpu(self):
        "cpu利用率"
        baseTemplate=self.getBaseTemplate()
        if not baseTemplate:return {}
        tplName = baseTemplate.getUid()
        return {"CPU":self.getPerfValue(tplName, "CPU", "CPU")}
        
        
    def getMem(self):
        "mem利用率"
        baseTemplate=self.getBaseTemplate()
        if not baseTemplate:return {}
        tplName = baseTemplate.getUid()
        return {
                "Mem":self.getPerfValue(tplName, "Mem", "Mem"),
                "totalMem":self.getPerfValue(tplName, "Mem", "totalMem"),
                "memAvailReal":self.getPerfValue(tplName, "Mem", "MemLeft") or self.getPerfValue(tplName, "Mem", "memAvailReal")
         }
        
    def getPingStatus(self):
        "获取ping状态"
        evtMgr = xutils.getEventManager()
        _conditions = {"moUid":self.getUid(), "agent": "netping", "severity":5}
        events = evtMgr.findCurrentEvents(conditions=_conditions)
        
        if events: return False
        return True

            

    def getPluginSettings(self):
        "获取插件配置"
        
        baseTpl = self.getBaseTemplate()
        if not baseTpl:
            print "Warning: Network:%s-%s has not the base template" %(self.getUid(), self.manageIp)
            return {}
        
        return baseTpl._medata.get("pluginSettings",{})
    
    
    def _getDevconponents(self, cType):
        """
        获取设备组件列表
        @param cType: <string> 设备组件类型 
        """
        components = []
        if cType == "IpInterface": 
            components = self.interfaces
        return components
    
    @classmethod
    def getSubComponentTypes(cls):
        """
        网络所有组件类型(监控子对象类型)
        """
        from products.netModel.devComponents.ipInterface import IpInterface
        return [IpInterface]
    
#-------------------------------通用处理设备组件的方法----------------------------------------------------

    
    def __bindDevComponentDefaultTpl(self, basetplName):
        def fun(cpt):
            tpl = Template._loadObj(basetplName)
            if tpl: cpt.bindTemplate(tpl)
        return fun

        
    def __update_save_devComponents(self, devComponentType, devComponentMedatas=[], newObjDealFun=None):
        """
        更新或保存设备组件信息
        @param devComponentType: <DeviceComponent 子类>
        @param devComponentMedatas: [<dict>] 元数据的配置 uname必须的，其它配置项，请参考具体Model
        @param newObjDealFun: 新组件对象附加处理函数
        """
        components = self._getDevconponents(devComponentType.__name__)
        for cMedata in devComponentMedatas:
            cpt = None
            for _cpt in components:
                if _cpt and _cpt.uname == cMedata.get("uname"): 
                    cpt = _cpt
                    break
                
            if cpt:
                cpt.__extMedata__(cMedata)
            else:
                cpt = devComponentType()
                cpt.__extMedata__(cMedata)
                if newObjDealFun: newObjDealFun(cpt)
            cpt.ownCompany = self.ownCompany
            cpt.device = self 
            cpt._saveObj()   
            
            
    def __removeDevComponent(self, devComponentType, unames):
        """
        删除设备组件
        @param devComponentType: <DeviceComponent 子类>
        @param unames: <String | List<String>> 
        """
        if not unames: return
        _unames = []
        if type(unames) in types.StringTypes: _unames.append(unames)
        else: _unames.extend(unames)
        
        components = self._getDevconponents(devComponentType.__name__)
        for name in _unames:
            cpt = None
            for _cpt in components:
                if _cpt and _cpt.uname == name:
                    cpt = _cpt
                    break
                

            if cpt:
                cpt.remove()
                #todo other things...
                
        return            
            
#-------------------------------interfaces----------------------------------------------------
    @property
    def interfaces(self):
        return self._getRefMeObjects("device", IpInterface, conditions={})
    
    def _getInterfaceByName(self, name, interfaces=[]):
        "通过name检索一个接口实例"
        for iface in interfaces or self.interfaces:
            if name and  iface.uname == name: return iface
        return None
    
    def update_save_ipInterfaces(self, ipInterfaceMedatas=[]):
        bindDefaultTpl = self.__bindDevComponentDefaultTpl("ethernetCsmacd")
        return self.__update_save_devComponents(IpInterface, devComponentMedatas=ipInterfaceMedatas, newObjDealFun= bindDefaultTpl)
                
    def removeIpInterface(self, unames):
        return self.__removeDevComponent(IpInterface, unames)
    
    
    def remove(self):
        """
        删除设备，先删除设备中的相关组件，再删除设备本身
        """
        for  c in self.interfaces: c.remove()
        
        MonitorObj.remove(self)
        
    

        

    