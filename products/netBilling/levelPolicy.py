#coding=utf-8
from products.netModel.centerDocModel import CenterDocModel
from products.netModel import medata


class LevelPolicy(CenterDocModel):
    """
    用户级别策略，有四种：免费版、标准版、企业版、定制版
    """
    dbCollection = 'LevelPolicy'
    
    def __init__(self, uid=None):
        CenterDocModel.__init__(self)
        self.__extMedata__(dict( _id=uid))
        
    
    deviceCount = medata.plain("deviceCount",5)
    websiteCount = medata.plain("websiteCount",5)
    networkCount = medata.plain("networkCount",5)
    shortcutCmdCount = medata.plain("shortcutCmdCount",0)
    bootpoCount = medata.plain("bootpoCount",10)
    #监控项目组件 
    processCount = medata.plain("processCount", 0)
    interfaceCount = medata.plain("interfaceCount", 0)
    fileSystemCount = medata.plain("fileSystemCount", 0)
    ipServiceCount = medata.plain("ipServiceCount", 0)
    
    privateCollectorCount = medata.plain("privateCollectorCount", 0)
    
    
if __name__ == "__main__":
    pass