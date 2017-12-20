#coding=utf-8
import time
import pickle
from products.nbPlugin.basetask import BaseTask
from twisted.internet import reactor,protocol,defer
from products.netUtils.cmdBase import CmdBase
from products.netUtils.logger import Logging
log=Logging.getLogger("statustask")
class StatusTask(BaseTask):
    """
    SNMP性能任务
    """
    tasktype="status"
    def getDeviceConfig(self,ipAddress):
        """
        通过配置对象获取该对象下的所有数据点
        """
        self.deviceConfig=None
        serObj = self.rpyc.getServiceObj()
        csm = serObj.getCSM(self.options.csmconfig)
        deviceConfigs = pickle.loads(csm.remoteGetPingDeviceConfigs(self.options.collector))
        for deviceConfig in deviceConfigs:
            if deviceConfig.deviceIp==ipAddress:
                self.deviceConfig=deviceConfig
                break
        return self.deviceConfig

    def processEvents(self,severity,msg):
        """
        功能:保存PING结果至redis
        作者:wl
        时间:2013-1-22
        """
        data = {
          'deviceUid':self.deviceConfig.deviceId,
          'component':self.deviceConfig.deviceId,
          "message":msg,
          "eventKey":'device ping',
          "severity":severity,
          "collector":"main",
          "agent":"netping"
        }
        self.saveEvent(data)
        
        
    def buildOptions(self):
        CmdBase.buildOptions(self)
        self.parser.add_option('--csmconfig',dest='csmconfig',
                               default='PingConfig',
                               help='ping守护进程配置类,默认为PingConfig')
