#coding=utf-8
import os
import json
import random
from products.netPublicModel.modelManager import ModelManager as MM
from products.netWebAPI.base import BaseApi, apiAccessSettings
from products.netUtils import jsonUtils
from products.netModel.collector import Collector
from products.netModel.org.deviceClass import DeviceClass
from products.netModel.device import Device
from products.netPublicModel.userControl import UserControl
from products.netModel import  mongodbManager as dbManager
from products.netModel.devComponents.ipInterface import IpInterface
from products.netModel.devComponents.process import Process
from products.netPerData.perDataMerger import PerDataMerger
from products.netBilling.billingSys import BillingSys
from products.netPublicModel.collectorClient import ColloectorCallClient

from products.netUtils.settings import ManagerSettings
from products.netModel.org.location import Location
import types


settings = ManagerSettings.getSettings()

class Perf(object):
    
    def getDeviceCpuPerfs(self, dev, timeUnit):
        """
        获取设备cpu性能
        """
        coll = dev.collector
        dbName = dev._getPerfDbName()
        baseTpl = dev.getBaseTemplate()
        if not baseTpl:
            print "warning: Can't find the base template on Device %s" %dev.getUid()
            return []
        tableName = dev._getPerfTablName(baseTpl.getUid(), "CPU", "CPU") #cpu的数据源及数据点标识都为CPU
        
        datas = PerDataMerger().getPerfDataByTimeUnit(coll, dbName, tableName, dev.createTime, timeUnit)
        
        return datas
    
  
    
    def getDeviceMemPerfs(self, dev, timeUnit):
        coll = dev.collector
        dbName = dev._getPerfDbName()
        baseTpl = dev.getBaseTemplate()
        if not baseTpl:
            print "warning: Can't find the base template on Device %s" %dev.getUid()
            return []
        tableName = dev._getPerfTablName(baseTpl.getUid(), "Mem", "Mem")
        datas = PerDataMerger().getPerfDataByTimeUnit(coll, dbName, tableName, dev.createTime, timeUnit)
        
        return datas
    
    def getInterfaceThroughsPerfs(self, iface, timeUnit):
        if not iface: return {"title": "", "series": []}
        coll = iface.collector
        dbName = iface._getPerfDbName()
        baseTpl = iface.getBaseTemplate()
        
        if not baseTpl:
            print "warning: Can't find the base template on Interface %s" %iface.getUid()
            return []
        inputTableName = iface._getPerfTablName(baseTpl.getUid(), "Throughs", "ifInOctets")
        outputTableName = iface._getPerfTablName(baseTpl.getUid(), "Throughs", "ifOutOctets")
        
        inputDatas = PerDataMerger().getPerfDataByTimeUnit(coll, dbName, inputTableName, iface.createTime, timeUnit)
        outputDatas = PerDataMerger().getPerfDataByTimeUnit(coll, dbName, outputTableName, iface.createTime, timeUnit)
        series = [
                {"name":'In', "type":"spline", "data": inputDatas},
                {"name":'Out', "type":"spline", "data": outputDatas},
              ]

        return {"title": iface.titleOrUid(), "series": series}
    
    def getProcessPerfs(self, proc, timeUnit):
        coll = proc.collector
        dbName = proc._getPerfDbName()
        baseTpl = proc.getBaseTemplate()
        
        if not baseTpl:
            print "warning: Can't find the base template on Process %s" %proc.getUid()
            return []
        memTableName = proc._getPerfTablName(baseTpl.getUid(), "ps", "mem")
        cpuTableName = proc._getPerfTablName(baseTpl.getUid(), "ps", "cpu")
        
        cpuDatas = PerDataMerger().getPerfDataByTimeUnit(coll, dbName, cpuTableName, proc.createTime, timeUnit)
        memDatas = PerDataMerger().getPerfDataByTimeUnit(coll, dbName, memTableName, proc.createTime, timeUnit)
        series = [
                {"name":'Cpu', "type":"spline", "yAxis": 1, "data": cpuDatas},
                {"name":'Mem', "type":"spline","data": memDatas},
              ]
        
        return {"title": proc.titleOrUid(), "series": series}


class DeviceApi(BaseApi):
    
    def _getDev(self, uid):
        dr = MM.getMod("dataRoot")
        dev = dr.findDeviceByUid(uid)
        return dev
    
    def getDevice(self, uid):
        dev = self._getDev(uid)
        
        
        updict= {"cpu": dev.getCpu(), "mem": dev.getMem(), "upTime": dev.getSysUpTime(), 
                 "status": dev.getStatus()}
         
        return jsonUtils.jsonDoc(dev, updict, ignoreProperyties=["objThresholds"])
    
    def getDeviceBaseInfo(self, uid):
        dev = self._getDev(uid)
        updict= {"cpu": dev.getCpu(), "mem": dev.getMem(), "upTime": dev.getSysUpTime(), 
                 "status": dev.getStatus(), "collector": dev.collector.titleOrUid()}
        
        igs =["objThresholds", "templates", "deviceCls", "wmiConfig","commConfig", "lastSentBootpoCmdTime", 
              "ownCompany", "snmpConfig"]
        
        return jsonUtils.jsonDoc(dev, updict, ignoreProperyties=igs)
        
    
    def getDeviceClsRecentlyEvents(self, uid):
        dev = self._getDev(uid)
        if not dev: return []
        conditions = {"severity":{"$gte":3}}
        evts = dev.events(conditions=conditions, limit=10)
        return jsonUtils.jsonDocList(evts)
    
    def getDeviceClsLastEvents(self, uid):
        """
                   获得设备最新的一条事件！
        """
        dev = self._getDev(uid)
        if not dev:return {}
        conditions = {"severity":{"$gte":3}}
        evt = dev.events(conditions=conditions, limit=1)
        if not evt:
            return {}
        return jsonUtils.jsonDoc(evt[0])
           
    def getDeviceClsRecentlyEventsBaseInfo(self, uid):
        dev = self._getDev(uid)
        if not dev: return []
        conditions = {"severity":{"$gte":3}}
        igs = ["collectPointUid", "agent", "companyUid", "historical", "moUid","evtKeyId", "clearId",
               "eventClass", "clearKey",  "eventState", "collector"]
        evts = dev.events(conditions=conditions, limit=10)
        return jsonUtils.jsonDocList(evts, ignoreProperyties=igs)
    
#----------------------start 获取设备组件的远程配置信息----------------------#
    def getDevInterfaces(self, uid, simple=False):
        dev = self._getDev(uid)
        if not dev: return []
        igs = ["objThresholds", "ownCompany", "templates", "device", "customSpeed", "snmpIndex", "mtu"]
        def updict(iface):
            return dict(status =  iface.getStatus(), throughValues = iface.getThroughValues())
        
        if simple:
            def updict(iface):
                return {}
            
        return jsonUtils.jsonDocList(dev.interfaces, updict=updict, ignoreProperyties=igs)
    
    
    def getDevFileSystems(self, uid):
        dev = self._getDev(uid)
        if not dev: return []
        igs = ["templates", "objThresholds","ownCompany", "device", "snmpIndex", "createTime", "monitored"]
        def updict(fs):
            return dict(capacity=fs.capacity, usedCapacity=fs.usedCapacity)
        
        return jsonUtils.jsonDocList(dev.fileSystems, updict=updict, ignoreProperyties=igs)
    
    
    def getDevProcesses(self, uid, simple=False):
        dev = self._getDev(uid)
        if not dev: return []
        igs = ["templates", "objThresholds","ownCompany", "device", "snmpIndex", "type", "createTime"]
        def updict(obj):
            return {"status": obj.getStatus(), "cpu":obj.getCpu(), "mem":obj.getMem()}
        if simple:
            def updict(proc):
                return {}
        return jsonUtils.jsonDocList(dev.processes, updict=updict, ignoreProperyties=igs)
    
    def getMultiCpu(self,uid):
        dev = self._getDev(uid)
        if not dev: return []
        return dev.getMultiCpu()
    
    def getDevIpServices(self, uid):
        dev = self._getDev(uid)
        if not dev: return []
        def updict(obj):
            return {"status": obj.getStatus()}
        return jsonUtils.jsonDocList(dev.ipServices, updict=updict)
    
    
#----------------------end 获取设备组件的远程配置信息----------------------#
    
  
    def getDeviceCpuMemPerfs(self, uid, timeUnit="day"):
        dev = self._getDev(uid)
        cpuPerfs = {"name":"cpu", "type":"spline", "data":Perf().getDeviceCpuPerfs(dev, timeUnit)}
        memPerfs = {"name":"mem",  "type":"spline", "color":"#27AD1D", "data":Perf().getDeviceMemPerfs(dev, timeUnit)}
        return [cpuPerfs, memPerfs]
        

    
    def getInterfacesPerfs(self, devUid, timeUnit="day"):
        "获取设备所有的接口流量性能图数据"
        dev = self._getDev(devUid)
        rs = []
        for iface in dev.interfaces:
            rs.append(Perf().getInterfaceThroughsPerfs(iface, timeUnit))
            
        return rs

    def getInterfacePerfs(self, uid, timeUnit="day"):
        "获取设备所有的接口流量性能图数据"
        iface = IpInterface._loadObj(uid)
        rs = Perf().getInterfaceThroughsPerfs(iface, timeUnit)
            
        return rs
    
    def getProcessesPerfs(self, devUid, timeUnit="day"):
        "获取设备所有的进程性能图数据"
        dev = self._getDev(devUid)
        rs = []
        for proc in dev.processes:
            rs.append(Perf().getProcessPerfs(proc, timeUnit))
            
        return rs
    
    def getProcessPerfs(self, uid, timeUnit="day"):
        "获取设备所有的接口流量性能图数据"
        proc = Process._loadObj(uid)
        rs = Perf().getProcessPerfs(proc, timeUnit)
            
        return rs
    
    
#----------------------------------start 获取设备组件的本地配置信息---------------------------------#
    def getDevComponents(self, uid, cType):
        """
        获取本地组件的列表，从数据库中加载相关的组件
        @param uid: <String> 设备编号
        @param cType: <String> 组件类型 [Process|IpInterface|IpService|FileSystem]
        """
        dev = self._getDev(uid)
        if not dev: return []
        igs = ["templates", "objThresholds","ownCompany", "device",  "createTime", "monitored"]
        components = []
        if cType == "Process":
            components = dev.processes
        elif cType == "IpInterface":
            components = dev.interfaces
            
        elif cType == "IpService":
            components = dev.ipServices
            
        elif cType == "FileSystem":
            components = dev.fileSystems
            
        return jsonUtils.jsonDocList(components, ignoreProperyties=igs )
        
 
#----------------------------------end 获取设备组件的本地配置信息---------------------------------#

    @apiAccessSettings("del")
    def delDevComponents(self, uid, cUids, cType):
        dev = self._getDev(uid)
        if not dev: return "warn:删除设备组件失败，原因:设备不存在"
        
        components = []
        
        def _fill_unames():
            unames = []
            for c in components:
                if c.getUid() in cUids: unames.append(c.uname)
            return unames
        
        if cType == "Process":
            components = dev.processes
            dev.removeProcess(_fill_unames())
            
        elif cType == "IpInterface":
            components = dev.interfaces
            dev.removeIpInterface(_fill_unames())
            
        elif cType == "IpService":
            components = dev.ipServices
            dev.removeIpService(_fill_unames())
            
        elif cType == "FileSystem":
            components = dev.fileSystems
            dev.removeFileSystem(_fill_unames())
        
        return "成功删除了设备组件"


    @apiAccessSettings("edit")
    def saveDevBaseInfo(self, uid, title="", location="", description=""):
        dev = self._getDev(uid)
        if not dev: return "fail"
        dev.title=title
        dev.description=description
        if location:
            loc  =  Location._loadObj(location)
            if loc: dev.location = loc
            
        dev._saveObj()
        return "成功保存信息"
        

    def getDevSnmpConfig(self, uid):
        dev = self._getDev(uid)
        if not dev: return {}
        
        return dev.snmpConfig
    
    @apiAccessSettings("edit")
    def saveDevSnmpConfig(self, uid, config={}):
        dev = self._getDev(uid)
        if not dev: return "warn:保存Snmp配置失败"
        dev.snmpConfig = config
        return "成功保存Snmp配置"

    def getDevCommConfig(self, uid):
        dev = self._getDev(uid)
        if not dev: return {}
        return dev.commConfig

    @apiAccessSettings("edit")
    def saveDevCommConfig(self, uid, config={}):
        dev = self._getDev(uid)
        if not dev: return "warn:保存通用配置失败"
        dev.commConfig = config
        return "成功保存配置"
    
    def listCollectors(self, componentType="Device"):
        """
        用于添加设备时下拉菜单选择收集器
         """
        collectors = {"public":[], "private":[]}
        user = UserControl.getUser()
        ownCompany = user.ownCompany
        if not  ownCompany: return collectors

        publicColls = Collector.getFreeCollectors(componentType)
        privateColls = ownCompany._getRefMeObjects( "ownCompany", Collector)
        for coll in privateColls:
            collectors["private"].append({"_id":coll.getUid(),"title":coll.titleOrUid(), "host": coll.host})
        
        random.shuffle(publicColls)
        for coll in publicColls:
            collectors["public"].append({"_id":coll.getUid(),"title":coll.titleOrUid(), "host": coll.host})
                        
        return collectors
    
    
    def listDeviceCls(self):
        root =  DeviceClass.getRoot()
        nodes = root.listAllNodes(includeSelf=False)
        def updict(node):
            return dict(titlePath=node.getTitlePath())
        rs = jsonUtils.jsonDocList(nodes,updict=updict)
        return rs
    
    
    
    def listLocation(self):
        root =  Location.getDefault()
        nodes = root.listAllNodes(includeSelf=True)
        def updict(node):
            return dict(titlePath=node.getTitlePath())
        rs = jsonUtils.jsonDocList(nodes,updict=updict)
        return rs
 

    def _externalCheck(self, coll, manageIp, snmpCommunity="public"):
        """
        添加设备前，作外部条件检查，正常返回"ok",不正常返回警告信息
        """
        if coll is None:  return "warn:收集器不存在"
        elif type(coll) in types.StringTypes: return coll
        
        try:
            cCall = ColloectorCallClient(coll.host)
            data = {"manageIp":manageIp,"snmpCommunity":snmpCommunity}
            result = cCall.call("PingSnmp",data)
        except Exception,e:
            print e
            return "warn:连接收集器失败"
        
        if result == 1:
            return "warn:ping设备%s失败"  %manageIp
        elif result == 2:
            return "warn:请确认设备%s snmp服务已开启" %manageIp
        
        return "ok"
        

    @apiAccessSettings("edit")
    def addDevice(self, baseConfig, snmpConfig={}, commConfig={}, ipmiConfig={}, billingUid=None):
        "添加设备"
        user = UserControl.getUser()
        if BillingSys.hasEnoughPolicyForAdd(Device):
            return "warn:用户级别策略不足,无法支付新的主机监控，请删除不想要的设备以腾出数量或升级用户级别策略."
        
        collUid = baseConfig.get("collector",None)
        coll = Collector._loadObj(collUid)
        checkRs=self.checkCollector(user, coll)
        if checkRs != "ok": return checkRs
        #manageIp=baseConfig.get("manageIp")
        #eCheckResult =  self._externalCheck(coll, manageIp, snmpConfig.get("netSnmpCommunity","public"))
        #if eCheckResult != "ok": return eCheckResult
        
        deviceCls = DeviceClass._loadObj(baseConfig.get("deviceCls", ""))
        baseConfig.update(dict(deviceCls=deviceCls))  
        
        location = Location._loadObj(baseConfig.get("location", ""))
        baseConfig.update(dict(location=location))
        
        return self.loadDevice(user,baseConfig,coll,snmpConfig=commConfig,commConfig=commConfig)
    
    def loadDevice(self,user,baseConfig,coll,snmpConfig={},commConfig={}):
        """
                加载设备到数据库
        """        
        ownCompany = user.ownCompany
        from products.netModel.baseModel import RefDocObject
        conditions = {"ownCompany": RefDocObject.getRefInfo(ownCompany), "manageIp":baseConfig.get("manageIp")}
        num = Device._countObjects(conditions)
        if num:
            return "warn:添加设备失败，用户添加的IP地址已经存在！"
    
        deviceCls = baseConfig.get("deviceCls",None)
        loc = baseConfig.get("location", None) or Location.getDefault()
        company = user.ownCompany
        if not (coll and deviceCls and company): return "warn:fail"
         
        dev =Device()
        dev.collector = coll
        dev.deviceCls = deviceCls
        dev.location = loc
        dev.ownCompany = company
        
        dev.manageIp = baseConfig.get("manageIp");
        dev.title = baseConfig.get("title", "")
        dev.description = baseConfig.get("description", "")

        dev.commConfig.update(commConfig)
        dev.snmpConfig.update(snmpConfig)
         
        dev._saveObj()
         
        dr = MM.getMod('dataRoot')
        dr.fireEvent("add_new_device", dev=dev)
        return "成功添加设备"
    
    @apiAccessSettings("add")
    def batchNetAddDevice(self,batchConfig=None):
        """
                批量网段添加设备
        """
        from products.netUtils.IpUtil import getAllSegmentIps
        user = UserControl.getUser()
        if user.isExpired():
            return json.dumps(dict(info="帐号已过期或欠费，无法进行相关操作，请及时充值",error=1,detail=[]))
        
        if batchConfig is None:
            return json.dumps(dict(info="请添加批量添加信息!",error=1,detail=[]))
        
        network=batchConfig.get("ips",None)
        if not network:
            return json.dumps(dict(info="请填写网段信息!",error=1,detail=[]))
        
        deviceclass=batchConfig.get("deviceclass",None)
        deviceCls=self.checkDeviceClass(deviceclass)
        if type(deviceCls)==type(""):
            return deviceCls #error msg

        collUid = batchConfig.get("collector",None)
        coll = Collector._loadObj(collUid)
        checkRs=self.checkCollector(user, coll)
        if checkRs != "ok": return checkRs

        
        communities=batchConfig.get("snmpname","public").split(",")
        batchIps=getAllSegmentIps(network)
        if not batchIps:return json.dumps(dict(info="填写的网段格式不正确,请重新填写!",error=1,detail=[]))
        
        batchCfgs=dict(batchIps=batchIps,communities=communities)
        rs=self.batchAddDevice(user,coll,deviceCls,batchIps, batchCfgs)
        return rs
                

    @apiAccessSettings("add")
    def batchFileAddDevice(self,batchConfig=None):
        """
                批量文件添加设备
        """
        batchIps=[]
        communities=[]
        from products.netUtils.readExecl import ReadExecl
        from products.netUtils.IpUtil import checkip
        user = UserControl.getUser()
        if user.isExpired():
            return json.dumps(dict(info="帐号已过期或欠费，无法进行相关操作，请及时充值",error=1,detail=[]))
        deviceclass=batchConfig.get("deviceclass",None)
        deviceCls=self.checkDeviceClass(deviceclass)
        if type(deviceCls)==type(""):
            return deviceCls #error msg

        collUid = batchConfig.get("collector",None)
        coll = Collector._loadObj(collUid)
        checkRs=self.checkCollector(user, coll)
        if checkRs != "ok": return checkRs
        

        
        filePath=batchConfig.get("UpLoadFile","")
        if not os.path.exists(filePath):
            return json.dumps(dict(info="导入的文件不存在!",error=1,detail=[]))
        rel=ReadExecl(filePath,"Devices")
        tables=rel.parseExcel()
        if tables is None:return json.dumps(dict(info="你上传的文件格式不对!",error=1,detail=[]))
        for i in xrange(len(tables)):
            row=tables[i]
            if len(row)==3:
                did,deviceIp,community=row
                if not checkip(deviceIp):
                    return json.dumps(dict(info="编号%dIP地址格式不正确!"%did,error=1,detail=[]))
                batchIps.append(deviceIp)
                communities.append(community)
            else:
                return json.dumps(dict(info="第%d行数据格式不正确!"%i,error=1,detail=[]))
        batchCfgs=dict(batchIps=batchIps,communities=communities)
        return self.batchAddDevice(user,coll,deviceCls,batchIps,batchCfgs)
    
    def checkDeviceClass(self,deviceclass):
        """
                验证设备类信息
        """
        if deviceclass is None:
            return "warn:请填写设备类信息!"
        deviceCls= DeviceClass.findByPath("/devicecls/%s"%deviceclass)
        if not deviceCls:
            return "warn:设备类不存在!"
        return deviceCls
 
    def checkCollector(self,user,coll):
        """
                验证收集器
        """
        if not coll: return "warn:连接收集器失败,收集器不存在!"
        result=coll.collectorConn()
        if not result: return "warn:连接收集器失败,请确认收集器是否正常!"
        return "ok"
        
    
    @apiAccessSettings("add")
    def batchAddDevice(self,user,coll,deviceCls,batchIps,batchCfgs,title=""):
        """
                批量添加设备
        """
        detailMessages=[]
        successAddCount=0
        collHost=coll.host
        ccl=ColloectorCallClient(collHost)
        rs=ccl.verifyDevice(batchCfgs)
        devInfos=rs.get("data")
        message=rs.get("message")
        if message.find("warn")>=0 and not devInfos:return json.dumps(dict(info=message.replace("warn",""),error=1,detail=[]))
        for batchIp in batchIps:
            status=devInfos.get(batchIp,None)
            if status is None:
                message="设备%s添加失败,请检查其网络连通性是否正常!"%batchIp
                detailMessages.append(dict(ip=batchIp,message=message))
                continue
            if status==False:
                message="设备%s添加失败,SNMP配置是否正常!"%batchIp
                detailMessages.append(dict(ip=batchIp,message=message))
                continue
            baseConfig={}
            baseConfig.update(dict(manageIp=batchIp,deviceCls=deviceCls))
            message=self.loadDevice(user,baseConfig,coll)
            message=message.replace("auth_warn:","").replace("warn:","")
            if message.find("成功")>=0:successAddCount+=1
            detailMessages.append(dict(ip=batchIp,message=message))
        return json.dumps(dict(info="%d个设备添加成功,%d个设备添加失败!"%(successAddCount,len(batchIps)-successAddCount),error=0,detail=detailMessages))
    
    @apiAccessSettings("del")
    def delDevice(self, uid):
        dev = self._getDev(uid)
        if not dev: return "fail"
        
        manageIp = dev.manageIp
        dev.remove()
        dr = MM.getMod('dataRoot')
        dr.fireEvent("remove_host_device", dev=dev)
        self.delDeviceEvents(manageIp)
        return "成功删除设备"
    
    @apiAccessSettings("del")
    def delDeviceEvents(self,manageIp):
        db = dbManager.getNetEventDB() 
        db.events.remove({'deviceIp':manageIp})
        db.historyEvents.remove({'deviceIp':manageIp})
    
   
    @apiAccessSettings("edit")
    def setCustomSpeed(self, ifaceUid, customSpeed=0):
        "设置接口自定义带宽"
        iface = IpInterface._loadObj(ifaceUid)        
        if not iface: return "warn:设置的接口已经不存在"
        iface.customSpeed = customSpeed
        return "已经设置接口自定义带宽成功"
    #-------------------------------------------------------------------------------------------------------
    
    
            

        