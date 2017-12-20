#coding=utf-8
'''
Created on 2012-12-3

@author: root
'''
import types
from products.netUtils import xutils
from products.netModel.monitorObj import MonitorObj
from products.netModel import medata
from products.netModel.devComponents.ipInterface import IpInterface
from products.netModel.devComponents.process import Process
from products.netModel.devComponents.filesystem import FileSystem
from products.netModel.templates.template import Template
from products.netModel.eventSupport import DeviceEventSupport
from products.netModel.devComponents.IpService import IpService
from products.netUtils.xutils import getDeviceSnmpAndCommDefaultConfig
import re



class Device(DeviceEventSupport, MonitorObj):
    '''
    Device
    '''
    dbCollection = 'Device'
    
    def __init__(self, uid=None):
        '''
        Constructor
        '''
        MonitorObj.__init__(self)
        self.__extMedata__(getDeviceSnmpAndCommDefaultConfig())
        
#----------------------------------属性---------------------------------------------------#
    deviceCls  = medata.doc("deviceCls") #设备类
    location  = medata.doc("location") #分组位置 
    manageIp = medata.plain("manageIp") #管理IP
    snmpConfig = medata.Dictproperty("snmpConfig")
    commConfig = medata.Dictproperty("commConfig")
    wmiConfig = medata.Dictproperty("wmiConfig")
       
    billing = medata.doc("billing") #认购单
    
    def getManageId(self):
        """
        获取对象的管理Id
        """
        return self.manageIp or self.macAddress or self.titleOrUid()
    
    
    @property
    def isWindowsDev(self):
        "根据设备类型判断设备是否为windows设备"
        if not self.deviceCls: return False
        if self.deviceCls.uname == "windows": return True
        return False
        
    def getSysUpTime(self):
        "运行时间"
        tplName = self.getBaseTemplate().getUid()
        return self.getPerfValue(tplName, "SysUpTime", "UpTime")
        
    def uptimeStr(self):
        "uptimeStr"
        
    def getPingStatus(self):
        "获取ping状态"
        evtMgr = xutils.getEventManager()
        _conditions = {"moUid":self.getUid(), "agent": "netping", "severity":5}
        events = evtMgr.findCurrentEvents(conditions=_conditions)
        
        if events: return False
        return True
        
    
    def getSNMPStatus(self):
        "获取snmp状态"
        return "up"
        

    
    def getCpu(self):
        "cpu利用率"
        baseTemplate=self.getBaseTemplate()
        if not baseTemplate:return {}        
        tplName = baseTemplate.getUid()
        m = re.compile(r"linux", re.I).search(tplName)
        if m: #is linux template
            return {
                    "CPU":self.getPerfValue(tplName, "CPU", "CPU"),
                    #"sysCpu":self.getPerfValue(tplName, "CPU", "sysCpu"),
                    #"freeCpu":self.getPerfValue(tplName, "CPU", "freeCpu"),
                    "1MinLoad":self.getPerfValue(tplName, "Load", "1MinLoad"),
                    "5MinLoad":self.getPerfValue(tplName, "Load", "5MinLoad"),
             }
            
        return {
                    "CPU":self.getPerfValue(tplName, "CPU", "CPU"),
                }
    
    def getMultiCpu(self):
        """
                多核CPU利用率
        """
        baseTemplate=self.getBaseTemplate()
        if not baseTemplate:return {}        
        tplName = baseTemplate.getUid()
        multiCPU=self.getStatusValue(tplName, "multiCPU", "multiCPU").strip()
        return [dict(uname=cpu.split("=")[0],value=cpu.split("=")[1]) 
                                        for cpu in multiCPU.split(" ")]
        
        return {
                    "CPU":self.getPerfValue(tplName, "CPU", "CPU"),
                }
    
    
        
    def getMem(self):
        "mem利用率"
        baseTemplate=self.getBaseTemplate()
        if not baseTemplate:return {}        
        tplName = baseTemplate.getUid()
        m = re.compile(r"linux", re.I).search(tplName)
        if m: #is linux template
            return {
                    "Mem":self.getPerfValue(tplName, "Mem", "Mem"),
                    "totalMem":self.getPerfValue(tplName, "Mem", "totalMem"),
                    "memAvailReal":self.getPerfValue(tplName, "Mem", "memAvailReal"),
                    "memBuffer":self.getPerfValue(tplName, "Mem", "memBuffer"),
                    
             }
        
        return {
                    "totalMem":self.getPerfValue(tplName, "Mem", "totalMem"),
                    "AvailMem":self.getPerfValue(tplName, "Mem", "AvailMem"),
                    "Mem":self.getPerfValue(tplName, "Mem", "Mem"),
                }
    
            

    def getPluginSettings(self):
        "获取插件配置"
        
        baseTpl = self.getBaseTemplate()
        if not baseTpl:
            print "Warning: Device:%s-%s has not the base template" %(self.getUid(), self.manageIp)
            return {}
        
        return baseTpl._medata.get("pluginSettings",{})
    
    def getMultiCPUCmd(self):
        """
                得到多核CPU的获取命令
        """
        return "snmpwalk -v 2c -c  %s %s 1.3.6.1.2.1.25.3.3.1.2"%(
                    self.snmpConfig.get("netSnmpCommunity"),self.manageIp)
    
    def _getDevconponents(self, cType):
        """
                获取设备组件列表
        @param cType: <string> 设备组件类型 
        """
        components = []
        
        if cType == Process.__class__.__name__: components = self.processes
        elif cType == IpInterface.__class__.__name__: components = self.interfaces
        elif cType == FileSystem.__class__.__name__: components = self.fileSystems
        elif cType == IpService.__class__.__name__: components = self.ipServices
        
        return components
    
    @classmethod
    def getSubComponentTypes(cls):
        """
        设备所有组件类型(监控子对象类型)
        """
        from products.netModel.devComponents.ipInterface import IpInterface
        from products.netModel.devComponents.process import Process
        from products.netModel.devComponents.filesystem import FileSystem
        from products.netModel.devComponents.IpService import IpService
        
        return [IpInterface, Process, FileSystem, IpService]
    
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
        for cMedata in devComponentMedatas:
            cpt = None
            components = self._getDevconponents(devComponentType.__name__)
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
    
    def update_save_ipInterfaces(self, ipInterfaceMedatas=[]):
        bindDefaultTpl = self.__bindDevComponentDefaultTpl("ethernetCsmacd")
        return self.__update_save_devComponents(IpInterface, devComponentMedatas=ipInterfaceMedatas, newObjDealFun= bindDefaultTpl)
        
    def removeIpInterface(self, unames):
        return self.__removeDevComponent(IpInterface, unames)
        
        
#--------------------------------processes---------------------------------------------------        
    @property
    def processes(self):
        return self._getRefMeObjects("device", Process, conditions={})
        
        
    def update_save_processes(self, processMedatas=[]):
        bindDefaultTpl = self.__bindDevComponentDefaultTpl("OSProcess")
        return self.__update_save_devComponents(Process, devComponentMedatas=processMedatas, newObjDealFun=bindDefaultTpl)      
        
    def removeProcess(self, unames):
        return self.__removeDevComponent(Process, unames)
    
    
#------------------------------------fileSystems-----------------------------------------------

    @property
    def fileSystems(self):
        return self._getRefMeObjects("device", FileSystem, conditions={})
        
    def update_save_fileSystems(self, fileSystemMedatas=[]):
        bindDefaultTpl = self.__bindDevComponentDefaultTpl("FileSystem")    
        self.__update_save_devComponents(FileSystem, devComponentMedatas=fileSystemMedatas, newObjDealFun=bindDefaultTpl)
            
    def removeFileSystem(self, unames):
        return self.__removeDevComponent(FileSystem, unames)
    
    
#------------------------------------IpServices-----------------------------------------------

    @property
    def ipServices(self):
        return self._getRefMeObjects("device", IpService, conditions={})
        
        
    def _getIpServiceByName(self, name, ipServices=[]):
        "通过name检索一个IP服务实例"
        for ipsev in ipServices or self.ipServices:
            if name and  ipsev.uname == name: return ipsev
        return None
            
        
    def update_save_ipServices(self, ipServiceMedatas=[]):
        bindDefaultTpl = self.__bindDevComponentDefaultTpl("IpService")    
        self.__update_save_devComponents(IpService, devComponentMedatas=ipServiceMedatas, newObjDealFun=bindDefaultTpl)
            
    def removeIpService(self, unames):
        return self.__removeDevComponent(IpService, unames)


    
    def remove(self):
        """
        删除设备，先删除设备中的相关组件，再删除设备本身
        """
        for  c in self.interfaces: c.remove()
        for  c in self.processes: c.remove()
        for  c in self.ipServices: c.remove()
        for  c in self.fileSystems: c.remove()
        
        MonitorObj.remove(self)
        
        
    @staticmethod
    def getDevComponentClass(componentType):
        "设备类的静态方法，得到设备组件类"
        from products.netModel.devComponents.ipInterface import IpInterface
        from products.netModel.devComponents.IpService import IpService
        from products.netModel.devComponents.filesystem import FileSystem
        from products.netModel.devComponents.process import Process
        
        componentTypes=[IpInterface, IpService, FileSystem, Process]
        for c in componentTypes:
            if c.__name__ == componentType: return c
            
        return None
        
    @staticmethod    
    def zhDevComponentTypes():
        zhComponentTypes = {'IpInterface':"接口", 'Process':"进程",'FileSystem':"文件系统",'IpService':"IP服务"}
        return zhComponentTypes
    
