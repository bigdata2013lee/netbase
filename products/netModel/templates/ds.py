#coding=utf-8
from products.netModel.templates.cmdParser import CmdParser
from products.netModel.templates.dataPoint import DataPoint
from products.netModel.templates.base import BaseObj



class BaseDataSource(BaseObj):
    def __init__(self, uname):
        self._medata = dict(
            type = self.__class__.__name__ , 
            uname = uname,
            title = "",
            dataPoints = {},
            monitored = True
        )
        

        
    def getType(self):
        return self.__class__.__name__
    
    @property
    def _dataPoints(self):
        return self._medata["dataPoints"]
     
    def addDataPoint(self, dp):
        """
        添加数据点
        @param dp: <DataPoint> 
        @return: 
        """
        if not dp.uname: raise Exception('Datapoint uname can not be empty!')
        self._dataPoints[dp.uname] = dp._medata
        return self
    
    def getDataPoint(self, dpName):
        dpMedata = self._medata['dataPoints'].get(dpName, None)
        if not dpMedata: return None
        return DataPoint.createInst(dpMedata)
    
    def deleteDataPoint(self, dpName):
        """
            删除一个数据点
            @param dpName: 数据点名称 type->string 
        """
        if dpName in self._dataPoints:
            del self._dataPoints[dpName]
            
    @property
    def dataPoints(self):
        """
        获取所有的数据点
        @return: <{dpName:<DataPoint>}>
        """
        dps = {}
        for dpName, dpMedata in self._dataPoints.items():
            dp = DataPoint("")
            dp._medata = dpMedata
            dps[dpName] = dp
        return dps
        
    @classmethod
    def createInst(cls, medata):
        ds = None
        allowTypes = dict(
            SnmpDataSource=SnmpDataSource,
            WmiDataSource = WmiDataSource,
            CmdDataSource=CmdDataSource,
        )
        
        if medata["type"] not in allowTypes:
            print "create datasource inst warrning: %s not in allow types." % medata["type"]
            return ds
        
        ds = allowTypes[medata['type']]("")
        ds._medata.update(medata)

        return ds


#------------------------------ sub class --------------------------------------#
class SnmpDataSource(BaseDataSource):

    def __init__(self, uname):
        BaseDataSource.__init__(self, uname)



class CmdDataSource(BaseDataSource):
    def __init__(self, uname):
        BaseDataSource.__init__(self, uname)
        self._medata.update(dict(
            cmd = "",  #命令
            execType = 'ssh', #执行方式  ssh|telnet|script, 默认script
            execCycle = 300 #执行周期(秒)
        ))

    def getCmd(self, mo=None):
        "获取命令"
        return CmdParser.parse(self.get("cmd"), mo)
        

class WmiDataSource(BaseDataSource):
    def __init__(self, uname):
        BaseDataSource.__init__(self, uname)
        self._medata.update(dict(
            cmd = "",  #命令
            nameSpace = "root/cimv2",
            sourceType = 'WMI',
            execCycle = 300,
        ))
        
    
    def getCmd(self, mo=None):
        "获取命令"
        return CmdParser.parse(self.get("cmd"), mo)
    
    
    
    
    
    
