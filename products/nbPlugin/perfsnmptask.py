#coding=utf-8
import time
import pickle
from products.nbPlugin.basetask import BaseTask
from twisted.internet import reactor,protocol,defer
from products.netUtils.cmdBase import CmdBase
from products.netUtils.logger import Logging
log=Logging.getLogger("perfsnmptask")
class PerfSnmpTask(BaseTask):
    """
    SNMP性能任务
    """
    tasktype="snmp"
    def getDeviceConfig(self,ipAddress):
        """
        通过配置对象获取该对象下的所有数据点
        """
        pconfig={}
        try:
            serObj = self.rpyc.getServiceObj()
            csm = serObj.getCSM(self.options.csmconfig)
            self.snmpConfig = pickle.loads(csm.remoteGetSnmpDeviceConfig(self.options.collector,ipAddress))
            pvalue=self.snmpConfig.oidMap.keys()
            pconfig={"pcollector":"snmp","psave":True,"pvalue":pvalue}
        except Exception,ex:
            log.error(ex)
        return pconfig
    
    def processResult(self,device,results):
        """
        处理数据
        """
        for dataTime,result in results.iteritems():
            for oid,value in result.items():
                oid=".%s"%oid.strip()
                oidObjs = self.snmpConfig.oidMap.get(oid)
                if not oidObjs:continue
                for oidObj in oidObjs:
                    data = {"deviceUid":self.snmpConfig.deviceId,
                                 "componentType":oidObj.get("componentType"),
                                 "component":oidObj.get("componentId"),
                                 "templateUid":oidObj.get("tpUid"),
                                 "dataSource":oidObj.get("dsName"),
                                 "dataPoint":oidObj.get("dpName"),
                                 "timeId":dataTime,
                                 "value":value
                    }
                    self.saveResult(data)
            message = self.snmpConfig.snmpStatus.updateStatus(True)
            if message:
                severity = 0
                if self.snmpConfig.snmpStatus.count:
                    severity = 5
                data = {"deviceUid":self.snmpConfig.deviceId,
                             "component":None,
                             "message":message,
                             "eventKey":"snmp",
                             "severity":severity,
                             "collector":"main",
                             "agent":"netperfsnmp"
                }
                self.saveEvent(data)
        return results

    def processEvents(self,msg):
        """
        处理事件
        """
        data = {"deviceUid":self.snmpConfig.deviceId,
             "component":None,
             "message":msg,
             "eventKey":"snmp",
             "severity":5,
             "collector":"main",
             "agent":"snmp"
             }
        self.saveEvent(data)
        
    def buildOptions(self):
        CmdBase.buildOptions(self)
        self.parser.add_option('--csmconfig',dest='csmconfig',
                               default='SnmpPerConfig',
                               help='SNMP守护进程配置类,默认为SnmpPerConfig')
