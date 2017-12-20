#coding=utf-8
import os
import pickle
from products.netUtils import xutils
from products.nbPlugin.basetask import BaseTask
from twisted.internet import reactor,protocol,defer
from products.netUtils.cmdBase import CmdBase
from products.netUtils.logger import Logging
from products.netUtils.xutils import nbPath as _p
log=Logging.getLogger("modeltask")
class ModelTask(object):
    """
    模型化任务
    """
    tasktype="model"
    def getDeviceConfig(self,ipAddress):
        """
        获取设备的服务配置
        """
        try:
            serObj = self.rpyc.getServiceObj()
            csm = serObj.getCSM(self.options.csmconfig)
            self.sevConfigs = pickle.loads(csm.remoteGetIpServiceDeviceConfig(ipAddress))
            return [serConfig.get("port",None) for serConfig in self.sevConfigs]
        except Exception,ex:
            log.error(ex)

    def getClassCollectorPlugins(self):
        """
        获取设备的收集器插件
        """
        modelPath = " products.dataCollector.plugins"
        clsDict = {}
        for filename in os.listdir(_p("/products/dataCollector/plugins")):
            if filename.endswith("Map.py") or filename.endswith("Map.pyc"):
                clsName = filename.split(".")[0]
                if clsName not in clsDict.keys():
                    lis = modelPath.split(".")
                    lis.append(clsName)
                    clsModelPath = ".".join(lis)
                    try:
                        cls = xutils.importClass(clsModelPath.strip(),clsName)
                    except :
                        log.error("搜集器插件%s实例化失败"%clsName)
                        continue
                    clsDict[clsName] = cls()
                    
        return clsDict
    
    def processEvents(self,result):
        """
        功能:发送事件
        参数:结果
        作者:lb
        时间:2013-2-1
        """
        for sevConfig in self.sevConfigs:
            port=sevConfig.get("port",None)
            if result.has_key(port):
                seruname,serstatus=result.get(port)
                if serstatus=="True":
                    data = {
                        "deviceUid":sevConfig.get("deviceId",None),
                        "component":sevConfig.get("component",None),
                        "message":"IP服务%s已启动"%seruname,
                        "eventKey":None,
                        "severity":0,
                        "collector":"main",
                        "agent":sevConfig.get("agent",None)
                    }
                    self.saveEvent(data)
                else:
                    data = {
                        "deviceUid":sevConfig.get("deviceId",None),
                        "component":sevConfig.get("component",None),
                        "message":"IP服务%s已停止"%seruname,
                        "eventKey":None,
                        "severity":4,
                        "collector":"main",
                        "agent":sevConfig.get("agent",None)
                    }
                    self.saveEvent(data)
    
    def buildOptions(self):
        CmdBase.buildOptions(self)
        self.parser.add_option('--csmconfig',dest='csmconfig',
                               default='IpServiceConfig',
                               help='服务守护进程配置类,默认为IpServiceConfig')
if __name__=="__main__":
    mt=ModelTask()