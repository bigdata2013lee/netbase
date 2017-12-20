#coding=utf-8
###########################################################################
#       
#
#此软件版权为深圳商之杰科技有限公司所有,更多信息请访问www.netbase.asia
#
#
###########################################################################
from products.netUtils.xutils import nbPath as _p

__doc__ = """
文件系统收集器插件
"""
import pickle
from products.netModel.filesystem import FileSystem2
from products.dataCollector.plugins.CollectorPlugin import GetTableMap
class FileSystemTask():
    columns = {
         '.1': 'snmpindex',
         '.2': 'type',
         '.3': 'mount',
         '.4': 'blockSize',
         '.5': 'totalBlocks',
         }

    snmpGetTableMaps = (
        GetTableMap('fsTableOid','.1.3.6.1.2.1.25.2.3.1',columns),
    )

    typemap = {
        ".1.3.6.1.2.1.25.2.1.1": "other",
        ".1.3.6.1.2.1.25.2.1.2": "ram",
        ".1.3.6.1.2.1.25.2.1.3": "virtualMemory",
        ".1.3.6.1.2.1.25.2.1.4": "fixedDisk",
        ".1.3.6.1.2.1.25.2.1.5": "removableDisk",
        ".1.3.6.1.2.1.25.2.1.6": "floppyDisk",
        ".1.3.6.1.2.1.25.2.1.7": "compactDisk",
        ".1.3.6.1.2.1.25.2.1.8": "ramDisk",
        ".1.3.6.1.2.1.25.2.1.9": "flashMemory",
        ".1.3.6.1.2.1.25.2.1.10": "networkDisk",
        }

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
        pconfig={"ptype":"snmp","pcollector":"filesystem","psave":False,"pvalue":pvalue}
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
        处理SNMP信息
        """
        if not results:return (True,None)
        tabledatas=results.values()[0]
        tabledata=self.mapdata(tabledatas)
        device=self.getDeviceObj(device)
        status,datamaps=(True,self.createFileInfo(device,tabledata))
        if status:self.updateComponent(device,datamaps)
    
    def getDeviceObj(self,ipAddress):
        
        serObj = self.rpyc.getServiceObj()
        csm = serObj.getCSM("ConfigServiceModel")
        device = pickle.loads(csm.getDeviceByManageIp("main",ipAddress))
        return device

    def createFileInfo(self,device,fsTable):
        "添加文件系统信息,绑定设备"
        fileObjList = []
        for snmpindex,value in fsTable.iteritems():
            totalBlocks = value.get("totalBlocks")
            if not totalBlocks:
                continue
            stype=value.get("type")
            stype=".%s"%stype.strip(".")
            disktype = self.typemap.get(stype)
            if disktype != "fixedDisk":
                continue
            fileIns = FileSystem2()
            fileIns.snmpIndex = value.get("snmpindex")
            fileIns.type = disktype
            fileIns.name = value.get("mount")
            fileIns.blockSize = value.get("blockSize")
            fileIns.totalBlocks = totalBlocks
            fileIns.device = device
            fileObjList.append(fileIns)
        return fileObjList
    
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
        return device.fileSystems

    def updateConfig(self,realObj,tmpObj):
        "更新设备的的文件信息"
        realObj.totalBlocks = tmpObj.totalBlocks
        realObj.blockSize = tmpObj.blockSize
        realObj.type = tmpObj.type
        realObj.snmpIndex = tmpObj.snmpIndex

    def modelDevice(self):
        """
        读文件,判断是否需要模型化设备
        """
        f=open(_p("model.txt"),"r")
        rs=f.read()
        f.close()
        return rs
    
if __name__=="__main__":
    fst=FileSystemTask()
    filesystem={'psave':True,'ptype':'snmp','pcollector':'filesystem','pvalue':{}}
    pvalue={"1364738749":{'.1.3.6.1.2.1.25.2.3.1.1':{"1.3.6.1.2.1.25.2.3.1.1.1":1,
                                                      "1.3.6.1.2.1.25.2.3.1.1.2":2,
                                                      "1.3.6.1.2.1.25.2.3.1.1.3":3,
                                                      "1.3.6.1.2.1.25.2.3.1.1.4":4,
                                                      "1.3.6.1.2.1.25.2.3.1.1.5":5,
                                                      "1.3.6.1.2.1.25.2.3.1.1.6":6,
                                                      "1.3.6.1.2.1.25.2.3.1.1.7":7},
                           '.1.3.6.1.2.1.25.2.3.1.3':{"1.3.6.1.2.1.25.2.3.1.3.1":"Memory Buffers",
                                                      "1.3.6.1.2.1.25.2.3.1.3.2":"Real Memory",
                                                      "1.3.6.1.2.1.25.2.3.1.3.3":"Swap Space",
                                                      "1.3.6.1.2.1.25.2.3.1.3.4":"/",
                                                      "1.3.6.1.2.1.25.2.3.1.3.5":"/boot",
                                                      "1.3.6.1.2.1.25.2.3.1.3.6":"/proc/fs/vmblock/mountPoint",
                                                      "1.3.6.1.2.1.25.2.3.1.3.7":"/media/CentOS_5.4_Final"}
                           }}
    
    fst.process("", pvalue, "")
    