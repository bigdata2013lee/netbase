#coding=utf-8
from products.netInitData import baseCiscoTemplate



def startCreateCiscoRouter_C1700_Template():
    
    cpuLoadOids = dict(
        m1oid = ".1.3.6.1.4.1.9.9.109.1.1.1.1.24",
        m5oid = ".1.3.6.1.4.1.9.9.109.1.1.1.1.25",
        s5oid = ".1.3.6.1.4.1.9.9.109.1.1.1.1.26"
    )
    
    t = baseCiscoTemplate.createBaseTemplate("BaseTpl_CiscoRouter_C1700")
    #CPU数据源
    baseCiscoTemplate.addCpuLoadSnmpDataSource(t, cpuLoadOids)
    #Mem数据源
    baseCiscoTemplate.addMemorySnmpDataSource(t)
    #Router相关数据源
    baseCiscoTemplate.addIpRouterSnmpDataSource(t)

if __name__ == "__main__":
    startCreateCiscoRouter_C1700_Template()