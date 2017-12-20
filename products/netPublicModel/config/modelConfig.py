#coding=utf-8
import pickle
from products.netPublicModel.baseConfigModel import ConfigServiceModel
from products.netPublicModel.modelManager import ModelManager

class ModelConfig(ConfigServiceModel):
    
    def remoteGetObjConfigByUid(self, objUid,componentType):
        """
                获取设备的配置
        """
        dr=ModelManager.getMod("dataRoot")
        device = dr.getMonitorObjByTypeAndUid(objUid,componentType)
        return pickle.dumps(device)
    
    def remoteModifyCollectIp(self,collectIp):
        """
                远程修改收集器IP
        """
        pass
