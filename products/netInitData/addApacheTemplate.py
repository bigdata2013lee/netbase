#coding=utf-8
from products.netModel.templates.template import Template
from products.netModel.templates.ds import CmdDataSource
from products.netModel.templates.dataPoint import DataPoint
from products.netModel.templates.threshold import MaxThreshold

def startCreateApacheTemplate():
    """
    创建Apache站点模板
    """
    #创建模板
    t = Template("BaseTpl_Apache")
    t.isBaseTpl=True
    t._saveObj()
    #创建数据源
    dshp= CmdDataSource("MwApache")
    dshp.set("cmd", "cmd=mo.getCmd()")
    dshp.set("execType","script")
    dshp.set("parser","middlewareDefaultParser")
    #创建数据点
    connection = DataPoint("connection")
    connection.set("type","DERIVE")
    #添加阀值到数据点
    maxt=MaxThreshold("maxconnection")
    maxt.set("max", 50)#setting
    maxt.set("format","Apache%(title)s连接数最大值为%(max)s")
    connection.addThreshold(maxt)
    dshp.addDataPoint(connection)

    bytesPerSec = DataPoint("bytesPerSec")
    bytesPerSec.set("type","GUAGE")
    dshp.addDataPoint(bytesPerSec)
    
    mwVersion = DataPoint("mwVersion")
    mwVersion.set("valueType","String")
    dshp.addDataPoint(mwVersion)
    
    reqPerSec = DataPoint("reqPerSec")
    reqPerSec.set("type","GUAGE")
    reqPerSec.set("valueType","Num")
    dshp.addDataPoint(reqPerSec)
    
    upTime = DataPoint("upTime")
    upTime.set("valueType","String")
    dshp.addDataPoint(upTime)

   
    #添加数据源到模板
    t.addDataSource(dshp)
    return t

if __name__=="__main__":
    startCreateApacheTemplate()
