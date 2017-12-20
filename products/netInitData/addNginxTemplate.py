#coding=utf-8
from products.netModel.templates.template import Template
from products.netModel.templates.ds import CmdDataSource
from products.netModel.templates.dataPoint import DataPoint
from products.netModel.templates.threshold import MaxThreshold


def startCreateNginxTemplate():
    """
    创建Nginx模板
    """
    #创建模板
    t = Template("BaseTpl_Nginx")
    t.isBaseTpl=True
    t._saveObj()
    
    #创建数据源
    dshp= CmdDataSource("MwNginx")
    dshp.set("cmd", "cmd=mo.getCmd()")
    dshp.set("execType","script")
    dshp.set("parser","middlewareDefaultParser")
       
    #当前 Nginx 正处理的活动连接数
    connection = DataPoint("connection")
    connection.set("type","GUAGE")
    connection.set("valueType","Num")
    #添加阀值到数据点
    maxt=MaxThreshold("maxconnection")
    maxt.set("max", 50)#setting
    maxt.set("format","Nginx%(title)s连接数最大值为%(max)s")
    connection.addThreshold(maxt)
    dshp.addDataPoint(connection)

    reqPerSec = DataPoint("reqPerSec")
    reqPerSec.set("type","DERIVE")
    reqPerSec.set("valueType","Num")
    dshp.addDataPoint(reqPerSec)

    errorPerSec = DataPoint("errorPerSec")
    errorPerSec.set("type","DERIVE") 
    errorPerSec.set("valueType","Num")
    dshp.addDataPoint(errorPerSec)
    
    mwVersion = DataPoint("mwVersion")
    mwVersion.set("valueType","String")
    dshp.addDataPoint(mwVersion)
    

 
    t.addDataSource(dshp)
    return t

if __name__=="__main__":
    startCreateNginxTemplate()
