#coding=utf-8

from products.netInitData import baseCiscoTemplate


def startCreateCiscoSwitch_Catalyst_3700_Template():
    """
  创建思科交换机Catalyst_3700模板
    """
    
    #CPU
    switchCpuOids = dict(
    
        usageOid = ".1.3.6.1.4.1.9.9.109.1.1.1.1.5.1",
        tempOid = ".1.3.6.1.4.1.9.9.13.1.3.1.3.1005",                
    )
    
    #风扇
    fanOids = dict(
                   
        fan1Oid = ".1.3.6.1.4.1.9.9.13.1.4.1.3.1004"
    )
    
    #电源状态
    SupplyStateOids = dict(
                       
        ssOid_1 = ".1.3.6.1.4.1.9.9.13.1.5.1.3.1",
        #ssOid_2 = ".1.3.6.1.4.1.9.9.13.1.5.1.3.2"                                      
    )
    #创建基础模板
    t = baseCiscoTemplate.createBaseTemplate("BaseTpl_CiscoSwitch_Catalyst_3700")
    #CPU 数据源
    baseCiscoTemplate.addSwitchCpuSnmpDataSource(t, switchCpuOids)
    #Mem数据源
    baseCiscoTemplate.addSwitchMemorySnmpDataSource(t)
    #风扇
    baseCiscoTemplate.addFanSnmpDataSource(t, fanOids)
    #电源状态
    baseCiscoTemplate.addSupplyStateSnmpDataSource(t, SupplyStateOids)
    
        
if __name__ == "__main__":
    
    startCreateCiscoSwitch_Catalyst_3700_Template()