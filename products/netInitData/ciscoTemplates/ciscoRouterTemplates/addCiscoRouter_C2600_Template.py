#coding=utf-8

from products.netInitData import baseCiscoTemplate

###--------------------创建思科路由器C2600模板-----------------------------------------------------------------------
def startCreateCiscoRouter_C2600_Template():
    """
  创建思科路由器C2600模板
    """
    #创建基础模板
    t = baseCiscoTemplate.createBaseTemplate("BaseTpl_CiscoRouter_C2600")
    #CPU 1分钟、5分钟，5秒钟 负载数据源
    baseCiscoTemplate.addCpuLoadSnmpDataSource(t)
    #缓存数据源
    baseCiscoTemplate.addBufferSnmpDataSource(t)
    #内存数据源
    baseCiscoTemplate.addMemorySnmpDataSource(t)
    
if __name__ == "__main__":
    startCreateCiscoRouter_C2600_Template()

    
    
    
    
    
    
    