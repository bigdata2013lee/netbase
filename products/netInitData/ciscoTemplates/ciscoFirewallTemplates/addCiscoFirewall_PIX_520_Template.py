#coding=utf-8

from products.netInitData import baseCiscoTemplate


def startCreateCiscoFirewall_PIX_520_Template():
    
    
    #CPU 1分钟、5分钟，5秒钟 负载数据源
    cpuLoadOids = dict(
        m1oid = ".1.3.6.1.4.1.9.9.109.1.1.1.1.4.1",
        m5oid = ".1.3.6.1.4.1.9.9.109.1.1.1.1.5.1",
        s5oid = ".1.3.6.1.4.1.9.9.109.1.1.1.1.3.1"
    )
    
    
    
    t = baseCiscoTemplate.createBaseTemplate("BaseTpl_CiscoFirewall_PIX_520")
    
    baseCiscoTemplate.addCpuLoadSnmpDataSource(t, cpuLoadOids)
    
    baseCiscoTemplate.addSwitchMemorySnmpDataSource(t)
    
    baseCiscoTemplate.addConnectionsSnmpDataSource(t)
    
    baseCiscoTemplate.addIKESnmpDataSource(t)
    
    baseCiscoTemplate.addIPSECSnmpDataSource(t)
    

if __name__ == "__main__":
    
    startCreateCiscoFirewall_PIX_520_Template()