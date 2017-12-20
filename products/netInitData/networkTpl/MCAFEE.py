#coding=utf-8
from products.netModel.templates.template import Template
from products.netModel.templates.ds import SnmpDataSource
from products.netModel.templates.dataPoint import DataPoint
"""
sensorHighestload    1.3.6.1.4.1.8962.2.1.3.1.1.5.1.2.2
pktCapTotal    1.3.6.1.4.1.8962.2.1.3.1.3.1.2
sensorAvgLoad    1.3.6.1.4.1.8962.2.1.3.1.1.5.1.1.2
ratelimitpktdrop    1.3.6.1.4.1.8962.2.1.3.1.2.1.1.1.2
sensorMaxTcpUdpFlows    1.3.6.1.4.1.8962.2.1.3.1.1.6.1.2.2
sensorAvgTcpUdpFlows    1.3.6.1.4.1.8962.2.1.3.1.1.6.1.1.2
sensorAvgIpFragFlows    1.3.6.1.4.1.8962.2.1.3.1.1.6.1.3.2
sensorMaxIpFragFlows    1.3.6.1.4.1.8962.2.1.3.1.1.6.1.4.2
sensorAvgIcmpFlows    1.3.6.1.4.1.8962.2.1.3.1.1.6.1.5.2
sensorMaxIcmpFlows    1.3.6.1.4.1.8962.2.1.3.1.1.6.1.6.2
"""

def addSensorDataSource(t):
    ds = SnmpDataSource("Sensor")
    ds.set("execCycle", 60)
    
    dp1 = DataPoint("Highestload")
    dp1.set("oid", "1.3.6.1.4.1.8962.2.1.3.1.1.5.1.2.2")
    dp1.set("type", "GUAGE")
    ds.addDataPoint(dp1)
    
    dp2 = DataPoint("pktCapTotal")
    dp2.set("oid", "1.3.6.1.4.1.8962.2.1.3.1.3.1.2")
    dp2.set("type", "GUAGE")
    ds.addDataPoint(dp2)
    
    dp3 = DataPoint("AvgLoad")
    dp3.set("oid", "1.3.6.1.4.1.8962.2.1.3.1.1.5.1.1.2")
    dp3.set("type", "GUAGE")
    ds.addDataPoint(dp3)
    
    dp4 = DataPoint("ratelimitpktdrop")
    dp4.set("oid", "1.3.6.1.4.1.8962.2.1.3.1.2.1.1.1.2")
    dp4.set("type", "GUAGE")
    ds.addDataPoint(dp4)
    
    dp5 = DataPoint("MaxTcpUdpFlows")
    dp5.set("oid", "1.3.6.1.4.1.8962.2.1.3.1.1.6.1.2.2")
    dp5.set("type", "GUAGE")
    ds.addDataPoint(dp5)
    
    dp6 = DataPoint("AvgTcpUdpFlows")
    dp6.set("oid", "1.3.6.1.4.1.8962.2.1.3.1.1.6.1.1.2")
    dp6.set("type", "GUAGE")
    ds.addDataPoint(dp6)
    
    dp7 = DataPoint("AvgIpFragFlows")
    dp7.set("oid", "1.3.6.1.4.1.8962.2.1.3.1.1.6.1.3.2")
    dp7.set("type", "GUAGE")
    ds.addDataPoint(dp7)
    
    dp8 = DataPoint("MaxIpFragFlows")
    dp8.set("oid", "1.3.6.1.4.1.8962.2.1.3.1.1.6.1.4.2")
    dp8.set("type", "GUAGE")
    ds.addDataPoint(dp8)
    
    dp9 = DataPoint("AvgIcmpFlows")
    dp9.set("oid", "1.3.6.1.4.1.8962.2.1.3.1.1.6.1.5.2")
    dp9.set("type", "GUAGE")
    ds.addDataPoint(dp9)
    
    dp10 = DataPoint("MaxIcmpFlows")
    dp10.set("oid", "1.3.6.1.4.1.8962.2.1.3.1.1.6.1.6.2")
    dp10.set("type", "GUAGE")
    ds.addDataPoint(dp10)
    
    t.addDataSource(ds)


def createMCAFEETpl():
    t=Template("BaseTpl_MCAFEE")
    t.isBaseTpl = True
    t._saveObj()
    addSensorDataSource(t)

if __name__=="__main__":
    createMCAFEETpl()