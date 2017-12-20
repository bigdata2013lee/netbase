#-*- coding:utf-8 -*-
###########################################################################
#       
#
#此软件版权为深圳商之杰科技有限公司所有,更多信息请访问www.netbase.asia
#
#
###########################################################################

__doc__ = """
进程组件配置获取
"""
import chardet
from products.dataCollector.plugins.CollectorPlugin \
    import SnmpPlugin,GetTableMap

HRSWRUNENTRY = '.1.3.6.1.2.1.25.4.2.1'

def repeat(name,names):
    if name in names:
        return False
    else:
        names.append(name)
    return True

class HRSWRunMap(SnmpPlugin):

    maptype = "OSProcessMap"
    compname = "os"
    relname = "processes"
    modname = "Products.ZenModel.OSProcess"
    classname = 'createFromObjectMap'

    columns = {
         '.1': 'snmpIndex',
         '.2': 'procName',
         '.4': 'procPath',
         '.5': 'parameters',
         }

    snmpGetTableMaps = (
        GetTableMap('hrSWRunEntry',HRSWRUNENTRY,columns),
    )

    def process(self,device,results,log):
        """
        解析进程数据
        ＠device:设备对象
        """
        names=[]
        datamaps=[]
        getdata,tabledata = results
        pidtable = tabledata.get("hrSWRunEntry")
        if not pidtable:
            errMsg="无法获取数据,请检查SNMP配置是否正确!"
            log.warn(errMsg)
            return errMsg,datamaps
        for snmpindex,value in pidtable.iteritems():
            try:
                procPath = value.get("procPath")
                prcode=chardet.detect(procPath).get("encoding","utf-8")
                if prcode is None:prcode="utf-8"
                value["procPath"]=procPath.decode(prcode)
                
                procName = value.get("procName")
                prncode=chardet.detect(procName).get("encoding","utf-8")
                if prncode is None:prncode="utf-8"
                value["procName"]=procName.decode(prncode)
                
                parameters = value.get("parameters")
                parcode=chardet.detect(parameters).get("encoding","utf-8")
                if parcode is None:parcode="utf-8"
                value["parameters"]=parameters.decode(parcode)
            except Exception,e:
                log.warn("编码格式错误")
            procname = self.makeProcessName(value)
            #非标准进程丢弃不处理
            if not procname:
                continue
            if not repeat(procname,names):continue
            value["uname"]=procname
            datamaps.append(value)
        return "",datamaps
    
    def makeProcessName(self,valueDict):
        procName = valueDict.get("procName")
        procPath = valueDict.get("procPath")
        parameters = valueDict.get("parameters")
        #非标准进程丢弃不处理
        if not procName or not procPath:
            return None
        #忽略参数时，procPath就是name
        retname=procName
        if procPath.find("\\") == -1:
            retname = procPath
        if parameters:
            parameters=parameters.strip()
            retname=retname+" "+parameters
        return retname
