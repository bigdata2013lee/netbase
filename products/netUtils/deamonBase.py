#coding=utf-8
import os,pickle
from products.netUtils.cmdBase import CmdBase
from products.netUtils.settings import CollectorSettings
from products.rpcService.client import Client
class DeamonBase(CmdBase):
    """
    收集器数据收集守护进程基类
    """
    def __init__(self):
        """
        初始化参数设置
        """
        self.rpycConfig()
        self.collectorConfig()
        CmdBase.__init__(self)
    
    def collectorConfig(self):
        """
        获取分布式配置
        """
        settings = CollectorSettings.getSettings()
        collUid = settings.get('collector','colUid')
        self.collector = None
        if collUid and  collUid != "None":
            self.collector=self.rpyc.getServiceObj().getDataRoot().getCollectorHost(collUid)
        if not self.collector:
            self.collector = CollectorSettings.getSettings().get("collector", "colHost")
        
    def rpycConfig(self):
        """
        rpyc远程调用配置
        """
        self.rpcHost=CollectorSettings.getSettings().get("rpycConnection", "rpcHost")
        self.rpcPort=CollectorSettings.getSettings().getAsInt("rpycConnection", "rpcPort")
        self.rpyc = Client(self.rpcHost,self.rpcPort)
    
    def getManageObjConifgs(self):
        """
        通过rpyc远程获取所有设备配置
        """
        import zlib
        def afun(serviceObj=None):
            csm = serviceObj.getCSM(self.options.csmconfig)
            return csm.remoteGetManageObjConfigs(self.options.collector)
        configResults = self.rpyc.access(afun)
        
        if configResults is None:return []
        return pickle.loads(zlib.decompress(configResults))
    
    def buildOptions(self):
        CmdBase.buildOptions(self)
        self.parser.add_option('--collector',dest='collector',
                               default=self.collector,
                               help='搜集器ID,默认为main')
