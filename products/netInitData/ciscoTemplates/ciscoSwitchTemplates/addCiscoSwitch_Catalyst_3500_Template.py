#coding=utf-8

from products.netInitData import baseCiscoTemplate


def startCreateCiscoSwitch_Catalyst_3500_Template():
    """
  创建思科交换机Catalyst_3500模板
    """

    #CPU 1分钟、5分钟，5秒钟 负载数据源
    cpuLoadOids = dict(
        m1oid = ".1.3.6.1.4.1.9.9.109.1.1.1.1.4",
        m5oid = ".1.3.6.1.4.1.9.9.109.1.1.1.1.5",
        s5oid = ".1.3.6.1.4.1.9.9.109.1.1.1.1.3"
    )
    
    #Switch CPU Temp
    switchCpuOids = dict(
    
        tempOid = ".1.3.6.1.4.1.9.9.13.1.3.1.3.1005"                
    )

    #风扇
    fanOids = dict(
                   
        fan1Oid = ".1.3.6.1.4.1.9.9.13.1.4.1.3.1004"
    )
    
    #电源状态
    SupplyStateOids = dict(
                       
        ssOid_1 = ".1.3.6.1.4.1.9.9.13.1.5.1.3.1003",
        #ssOid_2 = ".1.3.6.1.4.1.9.9.13.1.5.1.3.2"                                      
    )
    #创建基础模板
    t = baseCiscoTemplate.createBaseTemplate("BaseTpl_CiscoSwitch_Catalyst_3500")
    #CPU 数据源
    baseCiscoTemplate.addCpuLoadSnmpDataSource(t, cpuLoadOids)
    #Mem数据源
    baseCiscoTemplate.addSwitchMemorySnmpDataSource(t)
    #风扇
    baseCiscoTemplate.addFanSnmpDataSource(t, fanOids)
    #电源状态
    baseCiscoTemplate.addSupplyStateSnmpDataSource(t, SupplyStateOids)
    
    #CPU Temp
    baseCiscoTemplate.addSwitchCpuSnmpDataSource(t, switchCpuOids)
    
        
if __name__ == "__main__":
    
    startCreateCiscoSwitch_Catalyst_3500_Template()