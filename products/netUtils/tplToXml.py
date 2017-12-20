#coding=utf-8
import os
from products.netModel.templates.template import Template

objectFormat = '<object id="%s" module="%s" class="%s">'
propertyFormat = '<property id="%s" module="w">%s</property>'
head='<?xml version="1.0" encoding="UTF-8"?>\n<objects>'
tail="</tomanycont>\n</object>\n</objects>"

def convertToXml(tplObj,filename=None):
    """
    tpl:template
    filename:path to save xml file
    """
    if not filename:
        filename = "%s.xml" %tplObj._medata["_id"]
    xmlIter = dictToXML(tplObj)
    fobj = open(filename,'w')
    for line in xmlIter:
        fobj.write("%s%s" %(line,os.linesep))
    fobj.close()

def dictToXML(tplObj):
    yield head
    yield "<!--('netbase','wanjee','%s')-->" %tplObj._medata["_id"]
    yield objectFormat %(tplObj._medata["_id"],str(tplObj).rsplit('.',1)[0][1:],tplObj.__class__.__name__)  
    tpl_pros = tplObj._medata
    for tpl_pro in tpl_pros.keys():
            if tpl_pro != "dataSources" and tpl_pro != "_id":
                yield propertyFormat %(tpl_pro,tpl_pros[tpl_pro])      
    yield '<tomanycont id="datasources">'
    for ds in tpl._dataSources:
        dsObj = tpl.getDataSource(ds)
        ds_pros = dsObj._medata
        yield objectFormat %(dsObj.uname,str(dsObj).rsplit('.',1)[0][1:],dsObj.__class__.__name__)
        for ds_pro in ds_pros.keys():
            if ds_pro != "dataPoints":
                yield propertyFormat %(ds_pro,ds_pros[ds_pro]) 
        yield '<tomanycont id="datapoints">'
        for dp in dsObj.dataPoints: 
            dpObj = dsObj.getDataPoint(dp)
            yield objectFormat %(dpObj.uname,str(dpObj).rsplit('.',1)[0][1:],dpObj.__class__.__name__)
            dp_pros = dpObj._medata
            for dp_pro in dp_pros.keys():
                if dp_pro != "thresholds":
                    yield propertyFormat %(dp_pro,dp_pros[dp_pro])            
            yield '<tomanycont id="thresholds">'
            for thObj in dpObj.thresholds.values():
                yield objectFormat %(thObj.uname,str(thObj).rsplit('.',1)[0][1:],thObj.__class__.__name__)
                th_pros = thObj.__dict__["_medata"]
                for th_pro in th_pros.keys():
                    yield propertyFormat %(th_pro,th_pros[th_pro])                
                yield "</object>"
            yield '</tomanycont>'
            yield "</object>"
        yield '</tomanycont>'
        yield "</object>"
    yield tail
    
if __name__=="__main__":
    tpl = Template._findObjects()[0]
    f = open("new.xml",'w')
    for i in dictToXML(tpl):
        f.write("%s%s" %(i,os.linesep))
    f.close()
    
                    
        
    
