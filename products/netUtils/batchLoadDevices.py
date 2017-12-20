#coding=utf-8
import os
from products.netModel.user.user import User
from products.netModel.device import Device
from products.netModel.network import Network
from products.netModel.collector import Collector
from products.netPublicModel.modelManager import ModelManager as MM
from products.netModel.org.deviceClass import DeviceClass
from products.netModel.org.networkClass import NetworkClass
from products.netPublicModel import devTemplateMaps
from products.netUtils.readExecl import ReadExecl
from products.netUtils.xutils import nbPath as _p

class BatchLoadDevices(object):
    """
        批量加载设备(通过excel)
    """    
    def checkIPAddr(self,ip):
        """
                检查IP地址的格式是否正确
        """
        
        return True
    
    def addDevice(self,row):
        """
                批量添加设备
        """
        did,devicepath,productId,title,deviceIp,community,collectorIp,userName=row
        did=int(did)
        user=User._loadByUserName(userName)
        if user is not None:
            company = user.ownCompany
            if self.checkIPAddr(deviceIp) and self.checkIPAddr(collectorIp):
                collector = Collector._loadByHost(collectorIp)
                if collector is not None:
                    dev=Device()
                    dev.title =title
                    dev.manageIp = deviceIp
                    deviceCls= DeviceClass.findByPath("/devicecls/%s"%devicepath)
                    if not deviceCls:
                        print "设备类%s不存在,编号%s无法添加,请重新添加该设备!"%(devicepath,did)
                        return
                    dev.deviceCls=deviceCls
                    dev.collector = collector
                    dev.ownCompany = company
                    dev.snmpConfig.update(dict(netSnmpCommunity=community))
                    dev._saveObj()
                    dr = MM.getMod('dataRoot')
                    dr.fireEvent("add_new_device", dev=dev)
                else:
                    print "收集器%s不正确,编号%s无法添加,请重新添加该设备!"%(collectorIp,did)
            else:
                print "IP%s地址格式不正确,编号%s无法添加,请重新添加该设备!"%(deviceIp,did)
        else:
            print "用户%s不存在,编号%s无法添加,请重新添加该设备!"%(userName,did)
    
    def addNetwork(self,row):
        """
                添加网络设备
        """
        did,networkpath,productId,title,deviceIp,community,collectorIp,userName=row
        did=int(did)
        user=User._loadByUserName(userName)
        if user is not None:
            company = user.ownCompany
            if self.checkIPAddr(deviceIp) and self.checkIPAddr(collectorIp):
                collector = Collector._loadByHost(collectorIp)
                if collector is not None:
                    nwk=Network()
                    nwk.title =title
                    nwk.manageIp = deviceIp
                    networkCls= NetworkClass.findByPath(networkpath)
                    if not networkCls:
                        print "设备类%s不存在,编号%s无法添加,请修改后重新添加!"%(networkpath,did)
                        return
                    nwk.networkCls = networkCls
                    prodcutIdMap = devTemplateMaps.networkDevice.get(networkpath,{})
                    if not productId in prodcutIdMap.keys():
                        print "该设备型号%s不存在,编号%s无法添加,请修改后重新添加!"%(productId,did)
                        return
                    if not prodcutIdMap[productId]:
                        print "该设备型号%s模板不存在,编号%s无法添加,请联系管理员添加模板!"%(productId,did)
                        return 
                    nwk.productId=productId
                    nwk.collector = collector
                    nwk.ownCompany = company
                    nwk.snmpConfig.update(dict(netSnmpCommunity=community))
                    nwk._saveObj()
                    dr = MM.getMod('dataRoot')
                    dr.fireEvent("add_new_network", net=nwk)
                else:
                    print "收集器%s不正确,编号%s无法添加,请重新添加该设备!"%(collectorIp,did)
            else:
                print "IP%s地址格式不正确,编号%s无法添加,请重新添加该设备!"%(deviceIp,did)
        else:
            print "用户%s不存在,编号%s无法添加,请重新添加该设备!"%(userName,did)
        
    def deamonLoadDevice(self,filePath,xlsName,function):
        """
                通过后台批量添加设备
        """
        rel=ReadExecl(filePath,xlsName)
        if os.path.exists(filePath):
            tables=rel.parseExcel()
            for i in xrange(len(tables)):
                row=tables[i]
                if len(row)==8:
                    func=getattr(self,function)
                    func(row)
                else:
                    print "excel中第%d行数据格式不正确!"%(i)
        else:
            print "文件不存在或者路径错误!"

if __name__=="__main__":
    import sys
    xlsName="Devices"
    from products.netPublicModel.startNetbaseApp import startApp
    startApp(False,False)
    function=sys.argv[1]
    fileName=sys.argv[2]
    filePath=_p("/products/netInitData/%s" %fileName)
    BatchLoadDevices().deamonLoadDevice(filePath,xlsName,function)