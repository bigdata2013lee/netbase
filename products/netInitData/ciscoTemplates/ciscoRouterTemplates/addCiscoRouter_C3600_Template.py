#coding=utf-8

from products.netInitData import baseCiscoTemplate

###--------------------创建思科路由器C3600模板-----------------------------------------------------------------------
def startCreateCiscoRouter_C3600_Template():
    
    #供电状态
    SupplyStateOids = dict(
                       
        ssOid_1 = ".1.3.6.1.4.1.9.9.13.1.5.1.3.1",                                    
    )
    
    #温度状态
    TempStatusOids = dict(
                           
        tsOid_1 = ".1.3.6.1.4.1.9.9.13.1.3.1.6.1",                           
    )
    
    #mem
    memOids = dict(
        memFreeAOid = ".1.3.6.1.4.1.9.9.48.1.1.1.6.1",
        memFreeBOid = ".1.3.6.1.4.1.9.9.48.1.1.1.6.3",
        memUsedAOid = ".1.3.6.1.4.1.9.9.48.1.1.1.5.1",
        memUsedBOid = ".1.3.6.1.4.1.9.9.48.1.1.1.5.3"
    )
    
    #创建基础模板
    t = baseCiscoTemplate.createBaseTemplate("BaseTpl_CiscoRouter_C3600")
    #CPU 1分钟、5分钟，5秒钟 负载数据源
    baseCiscoTemplate.addCpuLoadSnmpDataSource(t)
    #缓存数据源
    baseCiscoTemplate.addBufferSnmpDataSource(t)
    #内存数据源
    baseCiscoTemplate.addMemorySnmpDataSource(t, memOids)
    #供电状态
    baseCiscoTemplate.addSupplyStateSnmpDataSource(t, SupplyStateOids)
    #温度状态
    baseCiscoTemplate.addTempStateSnmpDataSource(t, TempStatusOids)
    
if __name__ == "__main__":
    startCreateCiscoRouter_C3600_Template()

    
    
    
    
    
    
    