#coding=utf-8
import pickle
from products.nbPlugin.basetask import BaseTask
from twisted.internet import reactor,protocol,defer
from products.netUtils.cmdBase import CmdBase
from products.netUtils.logger import Logging
log=Logging.getLogger("ipservicetask")
class IpServiceTask(BaseTask):
    """
    服务任务
    """
    tasktype="service"
    def getDeviceConfig(self,ipAddress):
        """
        获取设备的服务配置
        """
        pconfig={}
        try:
            serObj = self.rpyc.getServiceObj()
            csm = serObj.getCSM(self.options.csmconfig)
            self.sevConfigs = pickle.loads(csm.remoteGetIpServiceDeviceConfig(self.options.collector,ipAddress))
            pvalue=[serConfig.port for serConfig in self.sevConfigs]
            pconfig={"pcollector":"service","psave":True,"pvalue":pvalue}
        except Exception,ex:
            log.error(ex)
        return pconfig

    def processResult(self,device,results):
        """
        功能:发送事件
        参数:结果
        作者:lb
        时间:2013-2-1
        """
        for sevConfig in self.sevConfigs:
            port=sevConfig.port
            for dataTime,result in results.iteritems(): 
                if result.has_key(port):
                    serstatus=result.get(port)
                    if serstatus:
                        data = {
                            "deviceUid":sevConfig.deviceId,
                            "component":sevConfig.component,
                            "message":"IP服务%s已启动"%sevConfig.component,
                            "eventKey":None,
                            "severity":0,
                            "collector":"main",
                            "timeId":dataTime,
                            "agent":"service"
                        }
                        self.saveEvent(data)
                    else:
                        data = {
                            "deviceUid":sevConfig.deviceId,
                            "component":sevConfig.component,
                            "message":"IP服务%s已停止"%sevConfig.component,
                            "eventKey":None,
                            "severity":4,
                            "collector":"main",
                            "timeId":dataTime,
                            "agent":"service"
                        }
                        self.saveEvent(data)
    
    def buildOptions(self):
        CmdBase.buildOptions(self)
        self.parser.add_option('--csmconfig',dest='csmconfig',
                               default='IpServiceConfig',
                               help='服务守护进程配置类,默认为IpServiceConfig')