#coding=utf-8

from products.netInitData import baseCiscoTemplate


def startCreateCiscoSwitch_Catalyst_6500_Template():
    """
  创建思科交换机_Catalyst_6500模板
    """
    #温度监测
    TempStatusValueOids = dict(     
                                              
        tsvOid_1 = ".1.3.6.1.4.1.9.9.13.1.3.1.3",                           
    )

    #温度状态
    TempStatusOids = dict(
                           
        tsOid_1 = ".1.3.6.1.4.1.9.9.13.1.3.1.6",   
        LastShutdown = ".1.3.6.1.4.1.9.9.13.1.3.1.5"                       
    )
    
    #供电状态
    SupplyStateOids = dict(
                       
        ssOid_1 = ".1.3.6.1.4.1.9.9.13.1.5.1.3"                                 
    )
    
    #风扇
    fanOids = dict(
                   
        fan1Oid = ".1.3.6.1.4.1.9.9.13.1.4.1.3"
    )
    
    #创建基础模板
    t = baseCiscoTemplate.createBaseTemplate("BaseTpl_CiscoSwitch_Catalyst_6500")
    #CPU 1分钟、5分钟，5秒钟 负载数据源
    baseCiscoTemplate.addCpuLoadSnmpDataSource(t)
    #Mem数据源
    baseCiscoTemplate.addSwitchMemorySnmpDataSource(t)
    
    baseCiscoTemplate.addTempStateSnmpDataSource(t, TempStatusOids)
    
    baseCiscoTemplate.addTempStateValueSnmpDataSource(t, TempStatusValueOids)
    
    baseCiscoTemplate.addSupplyStateSnmpDataSource(t, SupplyStateOids)
    
    baseCiscoTemplate.addFanSnmpDataSource(t, fanOids)
    
    
    
if __name__ == "__main__":
    startCreateCiscoSwitch_Catalyst_6500_Template()