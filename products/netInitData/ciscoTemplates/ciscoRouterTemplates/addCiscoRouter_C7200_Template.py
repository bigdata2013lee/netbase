#coding=utf-8

from products.netInitData import baseCiscoTemplate

def startCreateCiscoRouter_C7200_Template():
    
    t = baseCiscoTemplate.createBaseTemplate("BaseTpl_CiscoRouter_C7200")
    #cpmCPUTotal
    baseCiscoTemplate.addCpuLoadSnmpDataSource(t)
    #Mem
    baseCiscoTemplate.addMemorySnmpDataSource(t)
    #IpRouter
    baseCiscoTemplate.addIpRouterSnmpDataSource(t)
    #四个温度状态
    baseCiscoTemplate.addTempStateSnmpDataSource(t)
    #四个温度监测值
    baseCiscoTemplate.addTempStateValueSnmpDataSource(t)
    #电源
    baseCiscoTemplate.addSupplyStateSnmpDataSource(t)
    
if __name__ == "__main__":
    
    startCreateCiscoRouter_C7200_Template()