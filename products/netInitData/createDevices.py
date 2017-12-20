#coding=utf-8
from products.netModel.device import Device
def startCreateDevices(collector,ipAddress,template,company,devClsPath,commConfig=None):
    """
    创建单个设备
    """
    #创建设备
    dev=Device()
    dev._saveObj()
    dev.manageIp = ipAddress
    dev.collector = collector
    if commConfig is not None:
        dev.commConfig=commConfig
    #绑定模板
    dev.bindTemplate(template)
    dev.bindTemplate(template)
    return dev
    
def startCreateCmdDevice(collector,ipAddress,template,company,devClsPath):
    """
    创建cmd设备配置
    """
    #SSH设备配置,需修改用户名密码
    commConfig=dict(
                        netCommandPort=22,
                        netCommandUsername="root",
                        netCommandPassword="netbase",
                        netCommandLoginTimeout=10,
                        netCommandCommandTimeout=15, 
                        netKeyPath="~/.ssh/id_dsa",
                        netMaxOIDPerRequest=40, 
                        netSshConcurrentSessions=10
                )
    startCreateDevices(collector,ipAddress,template,company,devClsPath,commConfig)

def startCreateSnmpDevice(collector,ipAddress,template):
    """
    创建SNMP设备配置
    """
    startCreateDevices(collector,ipAddress,template)

        