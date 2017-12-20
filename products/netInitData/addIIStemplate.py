#coding=utf-8
from products.netModel.templates.template import Template
from products.netModel.templates.ds import WmiDataSource
from products.netModel.templates.dataPoint import DataPoint
from products.netModel.templates.ds import CmdDataSource


def startCreateIISWMITemplate():
    '''
    iis wmi template
    '''
    t=Template("BaseTpl_IIS")
    t.isBaseTpl=True
    t._saveObj()
       
    dshp= WmiDataSource("W3SVC_Perf")
    dshp.set("cmd", "SELECT * FROM Win32_PerfRawData_W3SVC_WebService WHERE Name='_Total'")
        
    def _createCommDataPoint(ds, dpName, dpType="GUAGE", valueTpye="Num"):
        dp = DataPoint(dpName)
        dp.set("type", dpType)
        dp.set("valueType",valueTpye)
        ds.addDataPoint(dp)
        
    _createCommDataPoint(dshp,"CurrentConnections")
    _createCommDataPoint(dshp,"BytesTotalPersec")
    _createCommDataPoint(dshp,"GetRequestsPersec")

    t.addDataSource(dshp)
    
    ds= CmdDataSource("Version")
    ds.set("cmd","cmd=mo.getCmd()")
    ds.set("execType","script")
    ds.set("parser","iisParser") 
    
    mwVersion = DataPoint("mwVersion")
    mwVersion.set("valueType","String")
    ds.addDataPoint(mwVersion)
    
    t.addDataSource(ds)

if __name__=="__main__":
    startCreateIISWMITemplate()
    