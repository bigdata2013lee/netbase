#coding=utf-8
from products.netModel.templates.template import Template
from products.netModel.templates.ds import CmdDataSource
from products.netModel.templates.dataPoint import DataPoint
from products.netModel.website import Website
from products.netModel.collector import Collector
from products.netModel.templates.threshold import MaxThreshold

def startCreateWebSiteTemplate():
    """
    创建web站点模板
    """
        #创建模板
    t = Template("BaseTpl_CmdWebSite")
    t.isBaseTpl=True
    t._saveObj()
    
    #ssh命令ifconfig数据源
    dshp= CmdDataSource("http")
    dshp.set("cmd", "cmd=mo.getCmd()")
    dshp.set("execType","script")
    dshp.set("parser","http")
    #解析http下的大小数据点
    dpsize = DataPoint("size")
    dpsize.set("type","GUAGE")
    dpsize.set("valueType","Num")
    #解析http下的响应时间数据点
    dptime = DataPoint("time")
    dptime.set("type","GUAGE")
    dptime.set("valueType","Num")
    #添加阀值到数据点
    maxt=MaxThreshold("maxTime")
    maxt.set("max", 5)
    maxt.set("zname", "最大响应时间")
    maxt.set("description","站点响应时间的最大值限制，建议设置在5s(秒)左右")
    maxt.set("format","站点%(title)s在%(eventInfo.collectPointTitle)s线路的当前响应时间为%(val)ss超过设定的最大值:%(max)s秒")
    maxt.set("severity", 3)
    dptime.addThreshold(maxt)
    
#    #解析http下的站点状态数据点
#    dpstatus = DataPoint("status")
#    dpstatus.set("type","GUAGE")
#    dpstatus.set("valueType","Num")

    dshp.addDataPoint(dpsize)
    dshp.addDataPoint(dptime)
#    dshp.addDataPoint(dpstatus)

    #添加数据源到模板
    t.addDataSource(dshp)
    return t

def getCollector():
    """
    得到收集器
    """
    collector = Collector._loadObj("main")
    return collector

def startCreateWebSite(collector,hostName,templateWebSite):
    """
    创建web站点
    """
    #创建web站点
    wb=Website()
    wb._saveObj()
    wb.collector = collector
    wb.hostName=hostName
    #绑定模板
    wb.bindTemplate(templateWebSite)
    
def startCreateWebSiteConfig():
    """
    创建站点配置
    """
    #创建收集器,返回收集器对象
    collector=getCollector()
    
    #创建命令行模板,返回命令行模板并将其放入到模板列表中
    #templateWebSite=startCreateWebSiteTemplate()
    
    #获取创建的模板
    templateWebSite=Template._findObjects()[0]
    
    #添加可以监控的Web站点列表
    hostNames=["www.test.com","www.google.cn","www.pudn.com","www.csdn.net","www.netbase.cc","www.zenoss.com","www.test.cam","www.netbase.nbnetwork"]
    for hostName in hostNames:
        startCreateWebSite(collector,hostName,templateWebSite)

if __name__=="__main__":
    startCreateWebSiteTemplate()