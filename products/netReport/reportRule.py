#coding=utf-8
from products.netModel.baseModel import DocModel
from products.netModel.device import Device
from products.netModel.network import Network
from products.netModel.website import Website
from products.netModel import medata

class ReportRule(DocModel):
    dbCollection = 'ReportRule'
    def __init__(self, uid=None):
        DocModel.__init__(self)
    description = medata.plain("description","")
    exportFormat= medata.plain("exportFormat","PDF")
    toMail= medata.plain("toMail",[])
    timeRange = medata.plain("timeRange",{})
    filterCondition = medata.plain("filterCondition",{})
    ownCompany = medata.doc("ownCompany")
    
    @property
    def conditions(self):
        """
                报表过滤条件
        """
        __filterCondition={}
        filterCondition=self.filterCondition
        for cls,values in filterCondition.iteritems():
            monitorObj=[]
            for clsId in values.get("objClass"):
                try:
                    cls=cls.replace("Class", "").lower().capitalize()
                    mobj=eval(cls).getMonitorObjByUid(clsId)
                    if not mobj:continue
                    monitorObj.append(mobj)
                except:pass
            for report in values.get("reports"):
                if not __filterCondition.has_key(report):
                    __filterCondition[report]=[]
                __filterCondition[report].extend(monitorObj)
        return __filterCondition