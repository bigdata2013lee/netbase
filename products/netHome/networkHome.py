class NetwroKHome(object):
    """
    网络模板首页
    """
    
    def __init__(self,deviceOrg):
        """
        初始化方法
        """
        self.deviceOrg=deviceOrg
        self.allNetworkDevices=self.getHostList()
    
    def getNetworkList(self):
        """
        得到网络设备列表
        """
        if self.deviceOrg is None:return []
        allNetworkDevices = self.deviceOrg.getAllMonitorObjs()
        return allNetworkDevices
    
    def getComponentSorce(self,networkSorces,networkDevice,timeRange=600):
        """
        得到组件评分
        """
        for interface in networkDevice.interfaces:
            if not interface.monitored:continue
            interfaceScore=self.monitorObjScore(interface,timeRange)
            networkSorces["interfaces"].append(interfaceScore)

    def getNetworkSorce(self,timeRange=600):
        """
        得到网络设备评分
        """
        networkSorces={"networks":[],"interfaces":[]}
        for networkDevice in self.allNetworkDevices:
            networkScore=self.monitorObjScore(networkDevice,timeRange)
            networkSorces["networks"].append(networkScore)
            self.getComponentSorce(networkSorces, networkDevice, timeRange)
        for name,sorces in networkSorces.iteritems():
            avgSorce=0
            totalCount=len(sorces)
            good=[i for i in sorces if i]
            badCount=len([i for i in sorces if i==0])
            unknownCount=len([i for i in sorces if i is None])
            if totalCount!=unknownCount:avgSorce=sum(good)/float(totalCount)
            networkSorces[name]=(totalCount-badCount-unknownCount,badCount,unknownCount,avgSorce)
        return networkSorces
    
    
    
    
    