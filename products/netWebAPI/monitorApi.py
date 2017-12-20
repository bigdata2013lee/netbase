#coding=utf-8
from products.netPublicModel.modelManager import ModelManager

from products.netWebAPI.base import BaseApi, apiAccessSettings
from products.netUtils import jsonUtils
from products.netPublicModel.collectorClient import ColloectorCallClient
from products.netHome.hostHome import HostHome
from products.netPublicModel.userMessage import UserMsg
from products.netModel.org.deviceClass import DeviceClass
from products.netPublicModel.userControl import UserControl
from products.netUtils.mcClient import availabilityCacheDecorator,\
    getSummaryInfo_DeviceClass
from products.netModel.org.location import Location
from products.netUtils import xutils
from products.netBilling.extendDevice import ExtendDevice
from products.netPublicModel.emailTemplates import extend_device_mail_html


def _countDevComponents(dev, ctype, selectedComponents, user=None):
    """
    统计打算新增的组件数量,及已经存在的数量
    @return: int
    """
    if not user: user = UserControl.getUser()   
    
    components = getattr(dev, ctype, [])
    existUnames = [cp.uname for cp in components]
    selectedUnames = [cp.get("uname") for cp in selectedComponents]
    newUnames = set(selectedUnames) - set(existUnames)
    return len(newUnames), len(components)

class MonitorApi(BaseApi):
    
    def _getDev(self, uid):
        dr = ModelManager.getMod("dataRoot")
        dev = dr.findDeviceByUid(uid)
        return dev
    
    def _getMo(self, mtype, uid):
        from products.netModel.device import Device
        from products.netModel.website import Website
        
        mTypes = {"Device":Device, 'Website':Website}
        mcls = mTypes.get(mtype)
        return mcls._loadObj(uid)
    
    def searchDevice(self, orgType, orgUid):
        dr = ModelManager.getMod("dataRoot")
        org = dr.loadOrgByUid(orgType, orgUid)
        conditions = {}
        rs = org.getAllMonitorObjs(conditions=conditions)
        def updict(doc):
            return {"title": doc.titleOrUid(), "cpu": doc.getCpu(), "mem": doc.getMem(), "upTime": doc.getSysUpTime(), "status": doc.getStatus()}
        rs = jsonUtils.jsonDocList(rs, updict=updict)
        return rs
    
    def listDevices(self, orgType, orgUid):
        devs = self.searchDevice(orgType, orgUid)
        #return filter(lambda x: x.get("status") is False, devs)
        return devs
    
    def listDevicesBaseInfo(self, orgType, orgUid, locUid=None):
        dr = ModelManager.getMod("dataRoot")
        org = dr.loadOrgByUid(orgType, orgUid)
        loc = Location._loadObj(locUid) if locUid else Location.getDefault()
        
        conditions = {}
        conditions.update({"location": loc._getRefInfo()})
        rs = org.getAllMonitorObjs(conditions=conditions)
        
        igs = ["templates", "description", "objThresholds", "startUpIPMI", "ipmiConfig", "ownCompany",
                "snmpConfig", "lastSentBootpoCmdTime", "monitored", "commConfig", "collector", "wmiConfig", "deviceCls"]
        def updict(doc):
            return {"title": doc.titleOrUid(), "cpu": doc.getCpu(), "mem": doc.getMem(), "upTime": doc.getSysUpTime(), "status": doc.getStatus()}
        rs = jsonUtils.jsonDocList(rs, updict=updict, ignoreProperyties= igs)
        return rs
        
        
    def listDevicesForConfigGrid(self, orgUid=None, locUid=None):
        if  not orgUid or  not locUid: return []
        
        org = DeviceClass._loadObj(orgUid)
        loc = Location._loadObj(locUid) if locUid else Location.getDefault()
        
        if  not org or  not loc: return []
        conditions = {}
        conditions.update({"location": loc._getRefInfo()})
            
        igs = ["templates", "description", "objThresholds", "startUpIPMI", "ipmiConfig", "ownCompany",
                "snmpConfig","monitored", "commConfig", "collector", "wmiConfig", "deviceCls"]
        rs = org.getAllMonitorObjs(conditions=conditions)
        def updict(doc):
            return {"title": doc.titleOrUid()}
        rs = jsonUtils.jsonDocList(rs, updict=updict, ignoreProperyties= igs)
        return rs

    
    def _listDeviceComponents(self, cType, devUid):
        """
        通过发送命令，获取设备组件的配置数据
        @param cType:  <String> interface|process|fileSystem
        @return: <[]>
        """
        defaultPluginSettings = dict(interface="InterfaceMap", process="HRSWRunMap", fileSystem="HRFileSystemMap")
        
        dr = ModelManager.getMod("dataRoot")
        dev = dr.findDeviceByUid(devUid)
        if not dev: return []
        ccClient = ColloectorCallClient(dev.collector.host)
        data = {"uid":dev.getUid(),"componentType":dev.getComponentType()}
        
        pluginSettings = dev.getPluginSettings()
        if not pluginSettings: return []
        rs = ccClient.call(pluginSettings.get(cType, defaultPluginSettings.get(cType)), vars = data)
        errMsg=rs.get("message","")
        if errMsg : UserMsg.warn(errMsg)
        for d in rs["data"]:
            try:d["uname"] = d["uname"].decode("gb2312")
            except: pass
            
        return rs["data"]
    
    
    def listDeviceIpInterfaces(self, devUid):
        return self._listDeviceComponents("interface", devUid)
    
    @apiAccessSettings("edit")
    def updateDeviceIpInterfaces(self, devUid,  interfaces=[]):
        "添加或更新接口配置"
        dev = self._getDev(devUid)
        if not dev: return "warn:not ok, dev is not exist."
#        newCount, existCount = _countDevComponents(dev, "interfaces", interfaces)
#        user = UserControl.getUser()
#        lp = user.levelPolicy
#        hasAuth = lp.interfaceCount - newCount - existCount >= 0
#        if not hasAuth:
#            return "auth_warn:操作失败，无法添加更多的接口"
        dev.update_save_ipInterfaces(interfaces)
        return "成功添加或更新接口配置"
        
    def listDeviceProcesses(self, devUid):
        return self._listDeviceComponents("process", devUid)
    
    @apiAccessSettings("edit")
    def updateDeviceProcesses(self, devUid,  processes=[]):
        "添加或更新进程配置"
        dev = self._getDev(devUid)
        if not dev: return "warn:not ok, dev is not exist."
#        newCount, existCount = _countDevComponents(dev, "processes", processes)
#        user = UserControl.getUser()
#        lp = user.levelPolicy
#        hasAuth = lp.processCount - newCount - existCount >= 0
#        if not hasAuth:        
#            return "auth_warn:操作失败，无法添加更多的进程"        
        dev.update_save_processes(processes)
        return "成功添加或更新进程配置"
    
    
    def listDeviceFileSystems(self, devUid):
        return self._listDeviceComponents("fileSystem", devUid)

    
    @apiAccessSettings("edit")
    def updateDeviceFileSystems(self, devUid,  fileSystems=[]):
        "添加或更新文件系统配置"
        dev = self._getDev(devUid)
#        if not dev: return "warn:not ok, dev is not exist."
#        newCount, existCount = _countDevComponents(dev, "fileSystems", fileSystems)
#        user = UserControl.getUser()
#        lp = user.levelPolicy
#        hasAuth = lp.fileSystemCount - newCount - existCount >= 0
#        if not hasAuth:
#            return "auth_warn:操作失败，无法添加更多的文件系统"
        dev.update_save_fileSystems(fileSystems)
        return "成功添加或更新文件系统配置"
    
    @apiAccessSettings("edit")
    def updateDeviceIpServices(self, devUid,  ipServices=[]):
        "添加或更新IP服务配置"
        dev = self._getDev(devUid)
#        if not dev: return "warn:not ok, dev is not exist."
#        newCount, existCount = _countDevComponents(dev, "ipServices", ipServices)
#        user = UserControl.getUser()
#        lp = user.levelPolicy
#        hasAuth = lp.ipServiceCount - newCount - existCount >= 0
#        if not hasAuth:
#            return "auth_warn:操作失败，无法添加更多的IP服务"
        dev.update_save_ipServices(ipServices)
        return "成功添加或更新IP服务配置"
    
    
    
    def getDeviceClsRecentlyEvents(self, orgType, orgUid):
        dr = ModelManager.getMod("dataRoot")
        org = dr.loadOrgByUid(orgType, orgUid)
        if not org: return []
        conditions = {"severity":{"$gte":3}}
        evts = org.events(conditions=conditions, limit=10)
        return jsonUtils.jsonDocList(evts)
    
    
    def getDeviceClsRecentlyEventsBaseInfo(self, orgType, orgUid, locUid=None):
        dr = ModelManager.getMod("dataRoot")
        org = dr.loadOrgByUid(orgType, orgUid)
        loc = Location._loadObj(locUid) if locUid else Location.getDefault()
        moConditions={}
        moConditions.update({"location": loc._getRefInfo()})
        
        igs = ["collectPointUid", "agent", "companyUid", "historical","evtKeyId", "clearId",
               "eventClass", "clearKey", "eventState", "collector"]
        if not org: return []
        conditions = {"severity":{"$gte":3}}
        evts = org.events(conditions=conditions, moConditions=moConditions, limit=10)
        return jsonUtils.jsonDocList(evts, ignoreProperyties=igs)
        
##------------------------------------------top N------------------------------------------------------##        
    @availabilityCacheDecorator
    def devicesAvailabilityTopN(self, orgType, orgUid, locUid=None, timeRange=3600):
        dr = ModelManager.getMod("dataRoot")
        org = dr.loadOrgByUid(orgType, orgUid)
        loc = Location._loadObj(locUid) if locUid else Location.getDefault()
        hh = HostHome(org, loc)
        
        rs = hh.getHostAvailabilitysTop(timeRange=timeRange)
        
        series = []
        for key, value in rs["rs"].items():
            series.append(dict(name=key, data=value))
            
        return dict(series=series, categories=rs["strTime"])
    
    @availabilityCacheDecorator
    def interfacesAvailabilityTopN(self, orgType, orgUid, locUid=None, timeRange=3600):
        dr = ModelManager.getMod("dataRoot")
        org = dr.loadOrgByUid(orgType, orgUid)
        loc = Location._loadObj(locUid) if locUid else Location.getDefault()
        hh = HostHome(org, loc)
        
        rs = hh.getNetworkAvailabilitysTop(timeRange=timeRange)
        
        series = []
        for key, value in rs["rs"].items():
            series.append(dict(name=key, data=value))
            
        return dict(series=series, categories=rs["strTime"])

    @availabilityCacheDecorator
    def processesAvailabilityTopN(self, orgType, orgUid, locUid=None, timeRange=3600):
       
        dr = ModelManager.getMod("dataRoot")
        org = dr.loadOrgByUid(orgType, orgUid)
        loc = Location._loadObj(locUid) if locUid else Location.getDefault()
        hh = HostHome(org, loc)
        
        rs = hh.getProcessAvailabilitysTop(timeRange=timeRange)
        
        series = []
        for key, value in rs["rs"].items():
            series.append(dict(name=key, data=value))
            
        return dict(series=series, categories=rs["strTime"])
    
    @availabilityCacheDecorator
    def servicesAvailabilityTopN(self, orgType, orgUid, locUid=None, timeRange=3600):
        dr = ModelManager.getMod("dataRoot")
        org = dr.loadOrgByUid(orgType, orgUid)
        loc = Location._loadObj(locUid) if locUid else Location.getDefault()
        hh = HostHome(org, loc)
        
        rs = hh.getServiceAvailabilitysTop(timeRange=timeRange)
        
        series = []
        for key, value in rs["rs"].items():
            series.append(dict(name=key, data=value))
            
        return dict(series=series, categories=rs["strTime"])
    
    
##--------------------------------------------End  Top N--------------------------------------------##
    @getSummaryInfo_DeviceClass
    def getSummaryInfo(self):
        "综合评分与概要信息"
        root = DeviceClass.getRoot()
        hh = HostHome(root)
        return hh.getHostSorce()
        
    
    

    def getRaidInfos(self, moUid, moType="Deive"):
        raidInfos = dict(serialNo=None, productName=None,memorySize=None,
                         vdsOnLineDisk=None,vdsCriticalDisks=None,vdsRebuildDisk=None,
                         pdsDisks=None,pdsCriticalDisks=None,pdsFailedDisks=None)
        
        dr = ModelManager.getMod("dataRoot")
        mo = dr.getMonitorObjByTypeAndUid(moUid, moType)
        if not mo: return raidInfos
        
        raidTpl = mo.getTemplate("ExtendTpl_SshRaidLinux")
        if not raidTpl: return raidInfos
        
        raidInfos["serialNo"] = mo.getStatusValue(raidTpl.getUid(), "raid", "serialNo")
        raidInfos["productName"] = mo.getStatusValue(raidTpl.getUid(), "raid", "productName")
        raidInfos["memorySize"] = mo.getStatusValue(raidTpl.getUid(), "raid", "memorySize")
        
        dptNames = ["vdsOnLineDisk", "vdsCriticalDisks", "vdsRebuildDisk", "pdsDisks", "pdsCriticalDisks", "pdsFailedDisks"]
        for name in dptNames:
            raidInfos[name] = mo.getPerfValue(raidTpl.getUid(), "raid", name)
        
        return raidInfos
    
    
    def getTempAndFanInfos(self, moUid, moType="Deive"):
        raidInfos = dict(ambientTemp=None, okFan=None,failFan=None)
        
        dr = ModelManager.getMod("dataRoot")
        mo = dr.getMonitorObjByTypeAndUid(moUid, moType)
        if not mo: return raidInfos
        
        raidTpl = mo.getTemplate("ExtendTpl_IpmiLinux")
        if not raidTpl: return raidInfos

        
        dptNames = ["ambientTemp", "okFan", "failFan"]
        for name in dptNames:
            raidInfos[name] = mo.getPerfValue(raidTpl.getUid(), "ipmiTempAndFan", name)
        
        return raidInfos
        


    def  hasExtendTpl(self, moUid, tplName, moType="Deive"):
        dr = ModelManager.getMod("dataRoot")
        mo = dr.getMonitorObjByTypeAndUid(moUid, moType)
        if not mo:return False
    
        tpl = mo.getTemplate(tplName)
        if not tpl: return False
        
        return True
        

    def extendDevice(self,host,website,network):
        user=UserControl.getUser()
        if not user:return "warn:请先登录"
        if not xutils.isValiedNum(host):return "warn:主机数目只能为非负数,且不能以0开头"
        if not xutils.isValiedNum(website):return "warn:站点数目只能为非负数,且不能以0开头"
        if not xutils.isValiedNum(network):return "warn:网络数目只能为非负数,且不能以0开头"
        host=int(host)
        website=int(website)
        network=int(network)
        money_host=xutils.countMoney(host,5.0,xutils.setDiscount(host))
        money_website=xutils.countMoney(website, 5.0,xutils.setDiscount(website))
        money_network=xutils.countMoney(network, 5.0,xutils.setDiscount(network))
        money=money_host+money_website+money_network
        if int(money)==0:return "请至少选择一种需要扩充的设备类型"

        extendDevice=ExtendDevice()
        extendDevice.user=user
        extendDevice.deviceCount=host
        extendDevice.websiteCount=website
        extendDevice.networkCount=network
        extendDevice.money=money
        extendDevice._saveObj()
        try:
            self.extendDeviceMail(extendDevice, "网脊用户")
        except:
            return "您的请求已提交，虽然未能正确发送邮件，但是稍后我们会主动联系您，多谢您的支持"
        return "您的请求已提交，稍后我们会主动联系您，多谢您的支持"
    
    
    def extendDeviceMail(self,ed,st):
        subject = st + "设备扩充通知"
        message = extend_device_mail_html %{
                   "deviceCount":ed.deviceCount,
                   "websiteCount":ed.websiteCount,
                   "networkCount":ed.networkCount,
                   "user":ed.user.username,
                   "email":ed.user.email,
                   "contactPhone":ed.user.contactPhone,
                   "originalName":ed.user.originalName,
                   "money":ed.money
                }
        xutils.sendMail(subject, message, recipient_list=[ed.user.username], attachments=[]) 
