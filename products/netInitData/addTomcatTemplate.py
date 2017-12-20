#coding=utf-8
from products.netModel.templates.template import Template
from products.netModel.templates.ds import CmdDataSource
from products.netModel.templates.dataPoint import DataPoint
from products.netModel.templates.threshold import MaxThreshold

def startCreateTomcatTemplate():
    """
    创建Tomcat模板
    """
            #创建模板
    t = Template("BaseTpl_Tomcat")
    t.isBaseTpl=True
    t._saveObj()
    
    #Tomcat数据源
    dshp= CmdDataSource("MwTomcat")
    dshp.set("cmd", "cmd=mo.getCmd()")
    dshp.set("execType","script")
    dshp.set("parser","middlewareDefaultParser")
    
        
    #创建数据点连接数
    cThreadCount = DataPoint("cThreadCount")
    cThreadCount.set("type","GUAGE")
    cThreadCount.set("valueType","Num")
    #添加阀值到数据点
    maxt=MaxThreshold("cThreadCount")
    maxt.set("max", 50)#setting
    cThreadCount.addThreshold(maxt)
    dshp.addDataPoint(cThreadCount)
        
    cThreadsBusy = DataPoint("cThreadsBusy")
    cThreadsBusy.set("type","GUAGE")
    cThreadsBusy.set("valueType","Num")
    dshp.addDataPoint(cThreadsBusy)
    
    totalMem = DataPoint("totalMem")
    totalMem.set("type","GUAGE")
    totalMem.set("unit","Bit")
    totalMem.set("valueType","Num")
    
    maxt=MaxThreshold("maxTotalMem")
    maxt.set("max", 10*1024*1024)
    maxt.set("format","%(title)s %(zname)s:%(val)s超过设定的最大阀值")
    totalMem.addThreshold(maxt)
    dshp.addDataPoint(totalMem)
    
    freeMem = DataPoint("freeMem")
    freeMem.set("type","GUAGE")
    freeMem.set("valueType","Num")
    dshp.addDataPoint(freeMem)
    
    mwVersion = DataPoint("mwVersion")
    mwVersion.set("valueType","String")
    dshp.addDataPoint(mwVersion)
    
    osVersion = DataPoint("osVersion")
    osVersion.set("valueType","String")
    dshp.addDataPoint(osVersion)
    
    errorPerSec = DataPoint("errorPerSec")
    errorPerSec.set("type","DERIVE")
    errorPerSec.set("valueType","Num")
    dshp.addDataPoint(errorPerSec)
    
    bytesPerSec = DataPoint("bytesPerSec")
    bytesPerSec.set("type","DERIVE")
    bytesPerSec.set("valueType","Num")
    dshp.addDataPoint(bytesPerSec)
    
    reqPerSec = DataPoint("reqPerSec")
    reqPerSec.set("type","DERIVE")
    reqPerSec.set("valueType","Num")
    dshp.addDataPoint(reqPerSec)
    
    jvmVersion = DataPoint("jvmVersion")
    jvmVersion.set("valueType","String")
    dshp.addDataPoint(jvmVersion)



  
    #添加数据源到模板
    t.addDataSource(dshp)
    return t

if __name__=="__main__":
    startCreateTomcatTemplate()