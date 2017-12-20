#coding=utf-8
from products.netPublicModel.dataRoot import DataRoot
from products.netEvent.eventManager import EventManager
from products.netBoot.bootpoSev import BootpoSev
class ModelManager(object):
    """
    Public Model管理器
    """
    def __init__(self):
        pass

    _public_models = {}

    @staticmethod
    def regist(mid, modObj):
        """
        功能:模块对象注册方法
        参数:mid -type:string，modObj －type:Obj
        作者:wl
        时间:2013.1.29
        """
        ModelManager._public_models[mid] = modObj

    @staticmethod
    def unregist(mid):
        """
        功能:模块注销方法
        参数:mid -type:string
        作者:wl
        时间:2013.1.29
        """
        del ModelManager._public_models[mid]

    @staticmethod
    def getMod(mid):
        """
        功能:通过MID获取模块对象
        参数:mid -type:string
        作者:wl
        时间:2013.1.29
        """
        return ModelManager._public_models[mid]
    
#------------------------------------------------------------------------------------------------#
def _registConfigModels():
    """
    注册监控配置相关的Public Model
    """
    from products.netPublicModel.baseConfigModel import ConfigServiceModel
    from products.netPublicModel.config.commandConfig import CommandConfig
    from products.netPublicModel.config.processConfig import ProcessDeviceConfig
    from products.netPublicModel.config.pingConfig import PingConfig
    from products.netPublicModel.config.ipServiceConfig import IpServiceConfig
    from products.netPublicModel.config.snmpPerfConfig import SnmpPerConfig
    from products.netPublicModel.config.modelConfig import ModelConfig
    from products.netPublicModel.config.wmiPerfConfig import WmiConfig
    from products.netPublicModel.config.collectConfig import CollectConfig
    from products.netAlarm.netalarm import AlarmAction
    
    ModelManager.regist('ConfigServiceModel', ConfigServiceModel())
    ModelManager.regist('CommandConfig', CommandConfig())
    ModelManager.regist('ProcessDeviceConfig', ProcessDeviceConfig())
    ModelManager.regist('PingConfig', PingConfig())
    ModelManager.regist('IpServiceConfig', IpServiceConfig())
    ModelManager.regist('SnmpPerConfig', SnmpPerConfig())
    ModelManager.regist('ModelConfig', ModelConfig())
    ModelManager.regist('WmiConfig', WmiConfig())
    ModelManager.regist('CollectConfig', CollectConfig())
    ModelManager.regist('AlarmAction', AlarmAction())
    

def initPublicModel():
    """
    功能:初始化并注册Public Model
    """
    ModelManager.regist('dataRoot', DataRoot())
    ModelManager.regist('bootpoSev', BootpoSev())
    ModelManager.regist('eventManager', EventManager())
    _registConfigModels()



