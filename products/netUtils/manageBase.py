#coding=utf-8
import os
from products.netUtils.cmdBase import CmdBase
from products.netUtils.settings import ManagerSettings
from products.rpcService.client import Client

class ManageBase(CmdBase):
    """
    管理端后台守护进程基类
    """
    def __init__(self):
        """
        初始化参数设置
        """
        self.rpycConfig()
        CmdBase.__init__(self)
    
    def rpycConfig(self):
        """
        rpyc远程调用配置
        """
        self.rpcHost=ManagerSettings.getSettings().get("rpycConnection", "rpcHost")
        self.rpcPort=ManagerSettings.getSettings().getAsInt("rpycConnection", "rpcPort")
        self.rpyc = Client(self.rpcHost,self.rpcPort)
    
    def getManageObjConifgs(self):
        """
        通过rpyc远程获取所有设备配置
        """
        import pickle
        def afun(serviceObj=None):
            csm = serviceObj.getCSM(self.options.csmconfig)
            return csm.remoteGetManageObjConfigs(self.options.collector)
        configResults = self.rpyc.access(afun)
        if configResults is None:return []
        return pickle.loads(configResults)
