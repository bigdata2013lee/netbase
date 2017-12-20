#coding=utf-8
import time
from operator import itemgetter
from products.netPublicModel.userControl import UserControl
from products.netHome.timeIntervalUtil import TimeIntervalUtil
from products.netEvent.monitorObjEvent import MonitorObjEvent
from products.netUtils import xutils
class HostHome(MonitorObjEvent):
    """
    主机首页
    """
    def __init__(self,deviceOrg, loc=None):
        """
        初始化方法
        """
        self.deviceOrg=deviceOrg
        self.location = loc
        self.allHostDevices=self.getHostList()
    
    def getHostList(self):
        """
        得到主机列表
        """
        #conditions = {}
        if self.deviceOrg is None:return []
        conditions = {}
        if self.location:
            conditions["location"] = self.location._getRefInfo()
            
        allHostDevices = self.deviceOrg.getAllMonitorObjs(conditions=conditions)

        return allHostDevices

    def getComponentSorce(self,hostSorces,hostDevice,timeRange=600):
        """
        得到组件评分
        """
        if hasattr(hostDevice, "interfaces"):
            for interface in hostDevice.interfaces:
                if not interface.monitored:continue
                interfaceScore=self.monitorObjScore(interface,timeRange)
                hostSorces["interfaces"].append(interfaceScore)
        if hasattr(hostDevice, "processes"):
            for process in hostDevice.processes:
                if not process.monitored:continue
                processScore=self.monitorObjScore(process,timeRange)
                hostSorces["processes"].append(processScore)
        if hasattr(hostDevice, "ipServices"):
            for ipService in hostDevice.ipServices:
                if not ipService.monitored:continue
                serviceScore=self.monitorObjScore(ipService,timeRange)
                hostSorces["services"].append(serviceScore)

    def getHostSorce(self,timeRange=600):
        """
        得到设备评分
        """
        hostSorces={"devices":[],"processes":[],"services":[],"interfaces":[]}
        for hostDevice in self.allHostDevices:
            deviceScore=self.monitorObjScore(hostDevice,timeRange)
            hostSorces["devices"].append(deviceScore)
            self.getComponentSorce(hostSorces, hostDevice, timeRange)
        for name,sorces in hostSorces.iteritems():
            avgSorce=0
            totalCount=len(sorces)
            good=[i for i in sorces if i]
            badCount=len([i for i in sorces if i==0])
            unknownCount=len([i for i in sorces if i is None])
            if totalCount!=unknownCount:avgSorce=sum(good)/float(totalCount)
            hostSorces[name]=(totalCount-badCount-unknownCount,badCount,unknownCount,avgSorce)
        return hostSorces
    
    def getHostAvailabilitysTop(self,limit=10,timeRange=3600):
        """
        得到主机可用性
        """
        topAvailabilitys={}
        tiu=TimeIntervalUtil()
        IntervalTimes=tiu.getIntervalTime(timeRange)
        availHostTops=self._hostAvailabilitysTop(timeRange)[:limit]
        for availHost in availHostTops:
            host=availHost.get("mobj")
            manageIp=availHost.get("manageIp")

            topAvailability=[self.monitorObjAvailability(host, IntervalTime.get("firstTime"),
                                                         IntervalTime.get("lastTime"))  for IntervalTime in IntervalTimes]
            topAvailabilitys[manageIp]=topAvailability

        strTime=[IntervalTime.get("date") for IntervalTime in IntervalTimes]
        return {"rs":topAvailabilitys,"strTime":strTime}
    
    
    def getNetworkAvailabilitysTop(self,limit=10,timeRange=3600):
        """
        得到网络可用性
        """
        topAvailabilitys={}
        tiu=TimeIntervalUtil()
        IntervalTimes=tiu.getIntervalTime(timeRange)
        availNetworkTops=self._networkAvailabilitysTop(timeRange)[:limit]
        for availNetwork in availNetworkTops:
            interface=availNetwork.get("mobj")
            manageIp=availNetwork.get("manageIp")
            uname=availNetwork.get("uname")
            topAvailability=[self.monitorObjAvailability(interface, IntervalTime.get("firstTime"),
                                                         IntervalTime.get("lastTime"))  for IntervalTime in IntervalTimes]
            topAvailabilitys["%s-%s"%(manageIp,uname)]=topAvailability
        strTime=[IntervalTime.get("date") for IntervalTime in IntervalTimes]
        return {"rs":topAvailabilitys,"strTime":strTime}
        
    
    def getProcessAvailabilitysTop(self,limit=10,timeRange=3600):
        """
        进程可用性
        """
        topAvailabilitys={}
        tiu=TimeIntervalUtil()
        IntervalTimes=tiu.getIntervalTime(timeRange)
        availProcessTops=self._processAvailabilitysTop(timeRange)[:limit]
        for availProcess in availProcessTops:
            process=availProcess.get("mobj")
            manageIp=availProcess.get("manageIp")
            uname= xutils.ellipsisText(availProcess.get("uname"), length=50)
            topAvailability=[self.monitorObjAvailability(process, IntervalTime.get("firstTime"),
                                                         IntervalTime.get("lastTime"))  for IntervalTime in IntervalTimes]
            topAvailabilitys["%s-%s"%(manageIp,uname)]=topAvailability
        strTime=[IntervalTime.get("date") for IntervalTime in IntervalTimes]
        return {"rs":topAvailabilitys,"strTime":strTime}
        
    
    def getServiceAvailabilitysTop(self,limit=10,timeRange=3600):
        """
        服务可用性
        """
        topAvailabilitys={}
        tiu=TimeIntervalUtil()
        IntervalTimes=tiu.getIntervalTime(timeRange)
        availIpServiceTops=self._ipserviceAvailabilitysTop(timeRange)[:limit]
        for availIpService in availIpServiceTops:
            ipservice=availIpService.get("mobj")
            manageIp=availIpService.get("manageIp")
            uname=availIpService.get("uname")
            topAvailability=[self.monitorObjAvailability(ipservice, IntervalTime.get("firstTime"),
                                                         IntervalTime.get("lastTime"))  for IntervalTime in IntervalTimes]
            topAvailabilitys["%s-%s"%(manageIp,uname)]=topAvailability
        strTime=[IntervalTime.get("date") for IntervalTime in IntervalTimes]
        return {"rs":topAvailabilitys,"strTime":strTime}
    
    def _hostAvailabilitysTop(self,timeRange=3600):
        """
        可用性的排行
        """
        availHostTops=[]
        start, end=time.time()-timeRange,time.time()
        for hostDevice in self.allHostDevices:
            manageIp=hostDevice.manageIp
            availability=self.monitorObjAvailability(hostDevice, start, end)
            availHostTops.append(dict(mobj=hostDevice,manageIp=manageIp,availability=availability))
        return sorted(availHostTops,key=itemgetter("availability"),reverse=False)
    
    def _networkAvailabilitysTop(self,timeRange=3600):
        """
        网络可用性的排行
        """
        availNetworkTops=[]
        start, end=time.time()-timeRange,time.time()
        for hostDevice in self.allHostDevices:
            manageIp=hostDevice.manageIp
            for interface in hostDevice.interfaces:
                uname=interface.uname
                availability=self.monitorObjAvailability(interface, start, end)
                availNetworkTops.append(dict(mobj=interface,manageIp=manageIp,uname=uname,availability=availability))
        return sorted(availNetworkTops,key=itemgetter("availability"),reverse=False)
    
    def _processAvailabilitysTop(self,timeRange=3600):
        """
        进程可用性的排行
        """
        availProcessTops=[]
        start, end=time.time()-timeRange,time.time()
        for hostDevice in self.allHostDevices:
            manageIp=hostDevice.manageIp
            for process in hostDevice.processes:
                uname=process.uname
                availability=self.monitorObjAvailability(process, start, end)
                availProcessTops.append(dict(mobj=process,manageIp=manageIp,uname=uname,availability=availability))
        return sorted(availProcessTops,key=itemgetter("availability"),reverse=False)
    
    def _ipserviceAvailabilitysTop(self,timeRange=3600):
        """
        IP服务可用性的排行
        """
        availIpServiceTops=[]
        start, end=time.time()-timeRange,time.time()
        for hostDevice in self.allHostDevices:
            manageIp=hostDevice.manageIp
            for ipservice in hostDevice.ipServices:
                uname=ipservice.uname
                availability=self.monitorObjAvailability(ipservice, start, end)
                availIpServiceTops.append(dict(mobj=ipservice,manageIp=manageIp,uname=uname,availability=availability))
        return sorted(availIpServiceTops,key=itemgetter("availability"),reverse=False)
    
    def getHostEventList(self,limit=100):
        """
        得到主机当前事件列表
        """
        hostEvents=[]
        for hostDevice in self.allHostDevices:
            severity={"$gt":0}
            manageIp=hostDevice.manageIp
            componentType=hostDevice.getComponentType()
            conditions=self._monitorObjEventConditions(hostDevice,severity)
            eventResults=self._monitorObjCurrentEvents(conditions)
            for event in eventResults:
                hostEvent=dict(manageIp=manageIp,
                                                        severity=event.severity,
                                                        firstTime=event.firstTime,
                                                        endTime=event.endTime,
                                                        componentType=componentType,
                                                        message=event.message)
                hostEvents.append(hostEvent)
        allEvents=sorted(hostEvents,key=lambda x:(x.get("endTime"),x.get("severity")),reverse=True)
        return allEvents[:limit]
    
if __name__=="__main__":
    from products.netPublicModel.startNetbaseApp import startApp
    startApp()
    UserControl.login("netbase","netbase")
    hh=HostHome("")
  
    