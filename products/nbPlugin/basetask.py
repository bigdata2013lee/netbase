#coding=utf-8
from products.dataCollector.redisManager import RedisManager
from products.netUtils.cmdBase import CmdBase
class BaseTask(RedisManager,CmdBase):
    """
    基础任务类
    """
    tasktype="base"
    def __init__(self,rpyc):
        """
        初始化服务任务
        """
        self.rpyc=rpyc
        CmdBase.__init__(self,"%s.xml"%self.tasktype)
    
    def getDeviceConfig(self,ipAddress):
        pass