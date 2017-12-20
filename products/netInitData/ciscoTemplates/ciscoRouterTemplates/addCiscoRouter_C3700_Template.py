#coding=utf-8

from products.netInitData import baseCiscoTemplate

###--------------------创建思科路由器C3700模板-----------------------------------------------------------------------
def startCreateCiscoRouter_C3700_Template():
    
    #供电状态
    SupplyStateOids = dict(
                       
        ssOid_1 = ".1.3.6.1.4.1.9.9.13.1.5.1.3.1",     
        ssOid_2 = ".1.3.6.1.4.1.9.9.13.1.5.1.3.2", 
        ssOid_3 = ".1.3.6.1.4.1.9.9.13.1.5.1.3.3", 
        ssOid_4 = ".1.3.6.1.4.1.9.9.13.1.5.1.3.4",                                
    )
    
    #温度状态
    TempStatusOids = dict(
                           
        tsOid_1 = ".1.3.6.1.4.1.9.9.13.1.3.1.6.1",                           
    )
    
    
    #创建基础模板
    t = baseCiscoTemplate.createBaseTemplate("BaseTpl_CiscoRouter_C3700")
    #CPU 1分钟、5分钟，5秒钟 负载数据源
    baseCiscoTemplate.addCpuLoadSnmpDataSource(t)
    #缓存数据源
    baseCiscoTemplate.addBufferSnmpDataSource(t)
    #内存数据源
    baseCiscoTemplate.addMemorySnmpDataSource(t)
    #供电状态
    baseCiscoTemplate.addSupplyStateSnmpDataSource(t, SupplyStateOids)
    #温度状态
    baseCiscoTemplate.addTempStateSnmpDataSource(t, TempStatusOids)
    #风扇
    baseCiscoTemplate.addFanSnmpDataSource(t)
    
if __name__ == "__main__":
    startCreateCiscoRouter_C3700_Template()

    
    
    
    
    
    
    