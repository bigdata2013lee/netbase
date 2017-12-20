#coding=utf-8
from products.netModel.centerDocModel import CenterDocModel
from products.netModel import medata


class DeviceDtail(CenterDocModel):
    dbCollection = 'deviceDtail'
    
    def __init__(self,uid=None):
        CenterDocModel.__init__(self)

    deviceCount = medata.plain("deviceCount",0)
    websiteCount = medata.plain("websiteCount",0)
    networkCount = medata.plain("networkCount",0)
    shortcutCmdCount = medata.plain("shortcutCmdCount",0)
    bootpoCount = medata.plain("bootpoCount",0)
    #监控项目组件 
    processCount = medata.plain("processCount", 0)
    interfaceCount = medata.plain("interfaceCount", 0)
    fileSystemCount = medata.plain("fileSystemCount", 0)
    ipServiceCount = medata.plain("ipServiceCount", 0)
    
    privateCollectorCount = medata.plain("privateCollectorCount", 0)
