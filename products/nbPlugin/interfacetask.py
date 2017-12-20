#coding=utf-8
import pickle
from products.netModel.devComponents.ipInterface import IpInterface
from products.dataCollector.plugins.CollectorPlugin import GetTableMap
class InterfaceTask(object):
    tasktype="snmp"
    snmpGetTableMaps = (
        GetTableMap('iftable','.1.3.6.1.2.1.2.2.1',
                {'.1': 'ifindex',
                 '.2': 'id',
                 '.3': 'type',
                 '.4': 'mtu',
                 '.5': 'speed',
                 '.6': 'macaddress',
                 '.7': 'adminStatus',
                 '.8': 'operStatus'}
        ),
    )
    
    def __init__(self,rpyc):
        """
        初始化
        """
        self.rpyc=rpyc

    def getDeviceConfig(self):
        """
        获取OID配置
        """
        pvalue=self.snmpGetTableMaps[0].getoids()
        pconfig={"ptype":"snmp","pcollector":"interface","psave":False,"pvalue":pvalue}
        return pconfig
    
    def mapdata(self, results):
        """
        格式转换
        """
        data = {}
        for col, rows in results.items():
            name = self.snmpGetTableMaps[0]._oids[col]
            clen = len(col)
            for roid, value in rows.items():
                ridx = roid[clen:]
                data.setdefault(ridx, {})
                data[ridx][name] = value
        return data
    
    def processResult(self,device,results):
        """
        解析并构建接口对象
        """
        if not results:return (True,None)
        tabledatas=results.values()[0]
        tabledata=self.mapdata(tabledatas)
        device=self.getDeviceObj(device)
        status,datamaps=(True,self.createIpInterface(device,tabledata))
        if status:self.updateComponent(device,datamaps)

    def getDeviceObj(self,ipAddress):
        
        serObj = self.rpyc.getServiceObj()
        csm = serObj.getCSM("ConfigServiceModel")
        device =pickle.loads(csm.getDeviceByManageIp("main",ipAddress))
        return device
    
    def asmac(self, val):
        """
        转化byte为string
        """
        import struct
        mac = []
        for char in val:
            tmp = struct.unpack('B', char)[0]
            tmp =  str(hex(tmp))[2:]
            if len(tmp) == 1: tmp = '0' + tmp
            mac.append(tmp)
        return ":".join(mac).upper()
    
    def createIpInterface(self,device,iftable):
        "添加接口信息,绑定设备,返回接口实例列表"
        ifObjList = []
        for ifindex,value in iftable.iteritems():
            interfaceIns = IpInterface()
            interfaceIns.name = value.get("id")
            macaddress = value.get("macaddress")
            interfaceIns.macAddress = macaddress
            if macaddress:
                interfaceIns.macAddress = self.asmac(macaddress)
            interfaceIns.speed = value.get("speed")
            interfaceIns.mtu = value.get("mtu")
            interfaceIns.type = value.get("type")
            interfaceIns.snmpIndex = value.get("ifindex")
            interfaceIns.device = device
            ifObjList.append(interfaceIns)
        return ifObjList
    
    def updateComponent(self,device,tmpObjList):
            "更新设备的接口\文件\进程等信息"
            realConfigList = self.getDataList(device)
            realNameList = []
            realDict = {}
            for realEle in realConfigList:
                realNameList.append(realEle.name)
                realDict[realEle.name] = realEle
    
            #没有发现接口\文件\进程等
            if not tmpObjList:
                for realConfig in realConfigList:
                    realConfig.remove()
                return
    
            for tmpObj in tmpObjList:
                #是否为已有的接口\文件\进程等，如果存在需要更新，没有就创建
                if tmpObj.name in realNameList:
                    #接口\文件\进程等是否被锁定
                    realObj = realDict[tmpObj.name]
                    realNameList.remove(tmpObj.name)
                    if realObj.locked:
                        continue
                    else:
                        #更新接口\文件\进程等
                        self.updateConfig(realObj,tmpObj)
                else:
                    #新发现的接口\文件\进程等需要创建
                    tmpObj._saveObj()
    
            #不存在的接口\文件\进程等需要删除
            if realNameList:
                for rname in realNameList:
                    realDict[rname].remove()
                    
    def getDataList(self,device):
        """
        
        """
        return device.interfaces

    def updateConfig(self,realObj,tmpObj):
        "更新设备的接口信息"
        realObj.snmpIndex = tmpObj.snmpIndex
        realObj.type = tmpObj.type
        realObj.mtu = tmpObj.mtu
        realObj.speed = tmpObj.speed
        realObj.macAddress = tmpObj.macAddress

if __name__=="__main__":
    print InterfaceTask().getDeviceConfig()