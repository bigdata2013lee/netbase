#coding=utf-8
from products.netBilling.levelPolicy import LevelPolicy


def createFreeVersion():
    """
    免费版:设备5个，监控项目各设备5个， 站点1个，开关机对象1个，快捷命令1个
    """
    lp = LevelPolicy("free")
    lp.deviceCount = 5
    lp.websiteCount = 1
    lp.networkCount = 0
    lp.bootpoCount = 1
    lp.shortcutCmdCount = 1
    lp.interfaceCount = 5
    lp.fileSystemCount = 5
    lp.ipServiceCount = 5
    lp.processCount = 5
    lp._saveObj()
    
def createStandardVersion():
    """
    标准版:设备20个，监控项目各设备10个，站点5个，开关机对象5个，快捷命令5个机次数
    """
    lp = LevelPolicy("standard")
    lp.deviceCount = 20
    lp.websiteCount = 5
    lp.networkCount = 0
    lp.bootpoCount = 5
    lp.shortcutCmdCount = 10
    lp.interfaceCount = 10
    lp.fileSystemCount = 10
    lp.ipServiceCount = 10
    lp.processCount = 10
    lp._saveObj()
    
    
def createEnterpriseVersion():
    """
    企业版
    """
    lp = LevelPolicy("enterprise")
    lp.title = "企业版"
    lp.deviceCount = 20
    lp.websiteCount = 10
    lp.networkCount = 10
    lp.bootpoCount = 20
    lp.shortcutCmdCount = 10
    lp.interfaceCount = 200
    lp.fileSystemCount = 200
    lp.ipServiceCount = 200
    lp.processCount = 200
    lp.privateCollectorCount = 3
    lp._saveObj()
    

def createCustomizationVersion():
    """
    定制版:设备100个，监控项目各设备20个，站点20个，网络100个，开关机对象50个，快捷命令20个
    """
    lp = LevelPolicy("customization")
    lp.deviceCount = 100
    lp.websiteCount = 20
    lp.networkCount = 100
    lp.bootpoCount = 50
    lp.shortcutCmdCount = 20
    lp.interfaceCount = 20
    lp.fileSystemCount = 20
    lp.ipServiceCount = 20
    lp.processCount = 20
    lp.privateCollectorCount = 5
    lp._saveObj()


def initLevelPolicies():
    createFreeVersion()
    createStandardVersion()
    createEnterpriseVersion()
    createCustomizationVersion()
     
      

if __name__ == "__main__":
    initLevelPolicies()