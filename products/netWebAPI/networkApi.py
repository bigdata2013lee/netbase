#coding=utf-8
import types
from products.netPublicModel.modelManager import ModelManager as MM
from products.netWebAPI.base import BaseApi
from products.netPublicModel import devTemplateMaps
from products.netModel.collector import Collector
from products.netModel.org.networkClass import NetworkClass
from products.netPublicModel.userControl import UserControl
from products.netModel.network import Network
from products.netUtils import jsonUtils
from products.netPublicModel.userMessage import UserMsg
from products.netPublicModel.collectorClient import ColloectorCallClient
from products.netPublicModel.modelManager import ModelManager
from products.netHome.hostHome import HostHome
from products.netPerData.perDataMerger import PerDataMerger
from products.netModel.devComponents.ipInterface import IpInterface
from products.netUtils.settings import ManagerSettings
from products.netModel.org.location import Location
from products.netBilling.billingSys import BillingSys
settings = ManagerSettings.getSettings()


class Perf(object):
    
    def getNetworkCpuPerfs(self, net, timeUnit):
        """
        获取设备cpu性能
        """
        coll = net.collector
        dbName = net._getPerfDbName()
        baseTpl = net.getBaseTemplate()
        if not baseTpl:
            print "warning: Can't find the base template on Network %s" %net.getUid()
            return []
        tableName = net._getPerfTablName(baseTpl.getUid(), "CPU", "CPU") #cpu的数据源及数据点标识都为CPU
        datas = PerDataMerger().getPerfDataByTimeUnit(coll, dbName, tableName,net.createTime, timeUnit)
        return datas
    
  
    
    def getNetworkMemPerfs(self, net, timeUnit):
        coll = net.collector
        dbName = net._getPerfDbName()
        baseTpl = net.getBaseTemplate()
        if not baseTpl:
            print "warning: Can't find the base template on Network %s" %net.getUid()
            return []
        tableName = net._getPerfTablName(baseTpl.getUid(), "Mem", "Mem")
        datas = PerDataMerger().getPerfDataByTimeUnit(coll, dbName, tableName, net.createTime, timeUnit)
        
        return datas
    
    def getFirewallCurrentSessionPerfs(self, net, timeUnit):
        coll = net.collector
        dbName = net._getPerfDbName()
        baseTpl = net.getBaseTemplate()
        if not baseTpl:
            print "warning: Can't find the base template on Network %s" %net.getUid()
            return []  
        tableName = net._getPerfTablName(baseTpl.getUid(), "Connections", "currentSession")
        datas = PerDataMerger().getPerfDataByTimeUnit(coll, dbName, tableName, net.createTime, timeUnit)   
        return datas    
         
    
    def getInterfaceThroughsPerfs(self, iface, timeUnit):
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

    


class NetworkApi(BaseApi):
    
    
    def getNetwork(self, uid):
        net = Network._loadObj(uid)
        updict= {"cpu": net.getCpu(), "mem": net.getMem(), "upTime": net.getSysUpTime(), 
                 "status": net.getStatus()}
        return jsonUtils.jsonDoc(net, updict)
    
    def getBaseInfo(self, uid):
        net = Network._loadObj(uid)
        igs = ["commConfig", "templates", "objThresholds", "ownCompany", "networkCls", "wmiConfig", "snmpConfig", "collector"]
        updict= {"cpu": net.getCpu(), "mem": net.getMem(), "upTime": net.getSysUpTime(), 
                 "status": net.getStatus()}
        return jsonUtils.jsonDoc(net, updict, ignoreProperyties = igs)
    
    
    def getNetworkById(self, uid):
        net = Network._loadObj(uid)
        updict = {"collector" :net.collector.titleOrUid()}
        rs = jsonUtils.jsonDoc(net, updict=updict, ignoreProperyties=["networkCls",  "ownCompany"])
        return rs
    
    def getDevTemplateMaps(self, group):
        """
        获取网络设备产品型号
        @param path: 网络设备的分类路径
        @return: [<string>] 产品型号列表
        """
        rsDicts = devTemplateMaps.listProductIdsByGroup(group)
        return rsDicts
    
    def checkCollector(self,user,coll):
        """
                验证收集器
        """
        if not coll: return "warn:连接收集器失败,收集器不存在!"
        result=coll.collectorConn()
        if not result: return "warn:连接收集器失败,请确认收集器是否正常!"
        return "ok"


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

    def addNetworkDevice(self, baseConfig, snmpConfig={}, commConfig={}):
        """添加网络设备，如思科路由器等"""
        user = UserControl.getUser()
        if BillingSys.hasEnoughPolicyForAdd(Network):
            return "warn:你的网络设备监控项目权限不足，请购买服务后再试."
        
        collUid = baseConfig.get("collector",None)
        coll = Collector._loadObj(collUid)
        checkRs=self.checkCollector(user, coll)
        if checkRs != "ok": return checkRs
        manageIp=baseConfig.get("manageIp")
        #eCheckResult =  self._externalCheck(coll, manageIp, snmpConfig.get("netSnmpCommunity","public"))
        #if eCheckResult != "ok": return eCheckResult
    

        productId = baseConfig.get("productId", "")
        networkClsPath = baseConfig.get("networkClsPath", "")
        
        networkCls = NetworkClass.findByPath(networkClsPath)
        if not networkCls:
            return "warn:添加失败，找不到网络类."
        
        ownCompany = user.ownCompany
        
        from products.netModel.baseModel import RefDocObject
        conditions = {"ownCompany": RefDocObject.getRefInfo(ownCompany), "manageIp":baseConfig.get("manageIp")}
        num = Network._countObjects(conditions)
        if num:
            return "warn:添加网络设备失败，用户添加的IP地址已经存在！" 
        
        loc = Location._loadObj(baseConfig.get("location", "")) or Location.getDefault()
        if not (coll and networkCls and ownCompany): return "warn:添加网络设备失败！配置有错！"
        
        
        net =Network()
        net.collector = coll
        net.networkCls = networkCls
        net.location = loc
        net.ownCompany = ownCompany
        net.productId = productId
        net.manageIp = manageIp
        net.title = baseConfig.get("title", "")
        net.description = baseConfig.get("description", "")
        net.commConfig.update(commConfig)
        net.snmpConfig.update(snmpConfig)
        net._saveObj()
        dr = MM.getMod('dataRoot')
        dr.fireEvent("add_new_network", net=net)
        return "成功添加设备"
    
    #根据uid删除网络设备
    def delNetwork(self, uid):
        net = Network._loadObj(uid)
        if not net: return "warn:fail"
        net.remove()
        dr = MM.getMod('dataRoot')
        dr.fireEvent("remove_network_device", net=net)
        return "删除设备成功！"
    
    #保存网络设备，如思科路由器等
    def saveNetworkDevice(self, baseConfig, snmpConfig={}, commConfig={}):
        uid = baseConfig.get("networkId", "")
        if not uid: return "warn:保存设备失败!"
        net = Network._loadObj(uid)
        if not net: return "warn:保存设备失败！"
        net.manageIp = baseConfig.get("manageIp");
        net.title = baseConfig.get("title", "")
        net.description = baseConfig.get("description", "")
        net.commConfig.update(commConfig)
        net.snmpConfig.update(snmpConfig)
        net._saveObj()
        dr = MM.getMod('dataRoot')
        dr.fireEvent("save_new_network", net=net)
        return "成功修改设备"
    

    def listNetworks(self, orgType, orgUid):
        dr = ModelManager.getMod("dataRoot")
        org = dr.loadOrgByUid(orgType, orgUid)
        conditions = {}
        objs = org.getAllMonitorObjs(conditions=conditions)
        def updict(doc):
            return {"title": doc.titleOrUid(), "cpu": doc.getCpu(), "mem": doc.getMem(), "upTime": doc.getSysUpTime(), "status": doc.getStatus()}
        rs = jsonUtils.jsonDocList(objs, updict=updict)
        return rs
    
        
    def listNetworksForConfigGrid(self, orgUid=None):
        org=None
        if not orgUid:
            org = NetworkClass.getRoot()
        
        else:
            org = NetworkClass._loadObj(orgUid)
            
        if  not org:return []
        conditions = {}
        igs = ["templates", "description", "objThresholds", "ownCompany",
                "snmpConfig","monitored", "commConfig", "collector", "wmiConfig", "deviceCls"]
        rs = org.getAllMonitorObjs(conditions=conditions)
        def updict(doc):
            return {"title": doc.titleOrUid()}
        rs = jsonUtils.jsonDocList(rs, updict=updict, ignoreProperyties= igs)
        return rs
    
    
    def getOrgRecentlyEvents(self, orgType, orgUid):
        dr = ModelManager.getMod("dataRoot")
        org = dr.loadOrgByUid(orgType, orgUid)
        
        if not org: return []
        conditions = {"severity":{"$gte":3}}
        evts = org.events(conditions=conditions, limit=10)
        return jsonUtils.jsonDocList(evts)
    
    def networksAvailabilityTopN(self, orgType, orgUid, timeRange=3600):
        dr = ModelManager.getMod("dataRoot")
        org = dr.loadOrgByUid(orgType, orgUid)
        
        hh = HostHome(org)
        
        rs = hh.getHostAvailabilitysTop(timeRange=timeRange)
        
        series = []
        for key, value in rs["rs"].items():
            series.append(dict(name=key, data=value))
            
        return dict(series=series, categories=rs["strTime"])
    
    
    def interfacesAvailabilityTopN(self, orgType, orgUid, timeRange=3600):
        dr = ModelManager.getMod("dataRoot")
        org = dr.loadOrgByUid(orgType, orgUid)
        
        hh = HostHome(org)
        
        rs = hh.getNetworkAvailabilitysTop(timeRange=timeRange)
        
        series = []
        for key, value in rs["rs"].items():
            series.append(dict(name=key, data=value))
            
        return dict(series=series, categories=rs["strTime"])
    
    def getSummaryInfo(self):
        root = NetworkClass.getRoot()
        hh = HostHome(root)
        return hh.getHostSorce()
    
    #----------------click NetworkNode--------------------------------------------------     
    #获得网络设备类最近的事件
    def getNetworkClsRecentlyEvents(self, uid):
        net = Network._loadObj(uid)
        if not net: return []
        conditions = {"severity":{"$gte":3}}
        evts = net.events(conditions=conditions, limit=10)
        return jsonUtils.jsonDocList(evts)

#----------------------end 获取设备组件的远程配置信息----------------------#
    
    def getNetworkFireWallPerfs(self, uid, timeUnit="day"):
        net = Network._loadObj(uid)
        currSessPerfs = {"name":"currentSession", "type":"spline", "data":Perf().getFirewallCurrentSessionPerfs(net, timeUnit)}
        return [currSessPerfs]

    def getNetorkCpuMemPerfs(self, uid, timeUnit="day"):
        net = Network._loadObj(uid)
        cpuPerfs = {"name":"cpu", "type":"spline", "data":Perf().getNetworkCpuPerfs(net, timeUnit)}
        memPerfs = {"name":"mem",  "type":"spline", "color":"#27AD1D", "data":Perf().getNetworkMemPerfs(net, timeUnit)}
        return [cpuPerfs, memPerfs]
    
    def getInterfacesPerfs(self, uid, timeUnit="day", hasSelectInterface=[]):
        "获取设备所有的接口流量性能图数据"
        net = Network._loadObj(uid)
        rs = []
        if not hasSelectInterface:
            return rs
        if hasSelectInterface and  type(hasSelectInterface) == types.ListType:
            for ifaceUid in hasSelectInterface:
                iface = IpInterface._loadObj(ifaceUid)
                if not iface: continue
                rs.append(Perf().getInterfaceThroughsPerfs(iface, timeUnit))
            return rs
        if hasSelectInterface == "all":
            for iface in net.interfaces:
                rs.append(Perf().getInterfaceThroughsPerfs(iface, timeUnit))
            return rs

    
   
    #----------------------------------start 获取设备组件的本地配置信息---------------------------------#
    #获得网络设备接口状态
    def getNetworkInterfaces(self, uid):
        net = Network._loadObj(uid)
        if not net: return []
        def updict(iface):
            return dict(status =  iface.getStatus(), throughValues = iface.getThroughValues())
        ret = jsonUtils.jsonDocList(net.interfaces, updict=updict)
        return ret
    
    def getInterfacesUname(self, uid):
        rs = []
        net = Network._loadObj(uid)
        if not net: return []
        if not net.interfaces: return []
        for interface in net.interfaces:
            rs.append({"_id":interface.getUid(), "uname":interface.uname})
        return rs
    
    
    def getNetworkCpuMemPerfs(self, uid, timeUnit="day"):
        net = Network._loadObj(uid)
        cpuPerfs = {"name":"cpu", "type":"spline", "data":Perf().getNetworkCpuPerfs(net, timeUnit)}
        memPerfs = {"name":"mem",  "type":"spline", "color":"#27AD1D", "data":Perf().getNetworkMemPerfs(net, timeUnit)}
        return [cpuPerfs, memPerfs]
    
    
    def getNetworkComponents(self, uid, cType):
        """
        获取本地组件的列表，从数据库中加载相关的组件
        @param uid: <String> 设备编号
        @param cType: <String> 组件类型 IpInterface
        """
        net = Network._loadObj(uid)
        if not net: return []
        
        components = []
        if cType == "IpInterface":
            components = net.interfaces

        return jsonUtils.jsonDocList(components)
    
    
    
    ##---------------------网络设备接口相关操作-----------------------------------------------------------------
    
    def _listNetworkComponents(self, cType, netUid):
        """
        通过发送命令，获取设备组件的配置数据
        @param cType:  <String> interface
        @return: <[]>
        """
        defaultPluginSettings = dict(interface="InterfaceMap")
        
        net = Network._loadObj(netUid)
        if not net: return []
        ccClient = ColloectorCallClient(net.collector.host)
        data = {"uid":net.getUid(),"componentType":net.getComponentType()}
        pluginSettings = net.getPluginSettings() or defaultPluginSettings
        rs = ccClient.call(pluginSettings.get(cType, defaultPluginSettings.get(cType)), vars = data)
        errMsg=rs.get("message","")
        
        if errMsg : UserMsg.warn(errMsg)
        return rs["data"]
    
    
    def listNetworkIpInterfaces(self, netUid):
        return self._listNetworkComponents("interface", netUid)
        
            
    def updateNetworkIpInterfaces(self, netUid,  interfaces=[]):
        "添加或更新接口配置"
        net = Network._loadObj(netUid)
        if not net: return "warn:not ok, network is not exist."
        net.update_save_ipInterfaces(interfaces)
        return "成功添加或更新接口配置"
    
    def delNetworkComponents(self, uid, cUids, cType):
        net = Network._loadObj(uid)
        if not net: return "warn:fail"
        
        components = []
        
        def _fill_unames():
            unames = []
            for c in components:
                if c.getUid() in cUids: unames.append(c.uname)
            return unames
            
        if cType == "IpInterface":
            components = net.interfaces
            net.removeIpInterface(_fill_unames())
        
        return "成功删除了设备组件"
    
    def setCustomSpeed(self, ifaceUid, customSpeed=0):
        "设置接口自定义带宽"
        iface = IpInterface._loadObj(ifaceUid)        
        if not iface: return "warn:设置的接口已经不存在"
        iface.customSpeed = customSpeed
        return "已经设置接口自定义带宽成功"
            
    

    