#coding=utf-8
from products.netPublicModel.userControl import UserControl
from products.netModel.device import Device
from products.netModel.network import Network
from products.netModel import medata
from products.netModel.baseModel import DocModel


subMoTypes=[Device,Network]

class Location(DocModel):
    dbCollection = 'Location'

    ownCompany = medata.doc("ownCompany") #公司
    locType = medata.plain("locType", "common")  #common | default
    zIndex = medata.plain("zIndex", 1)
    def __init__(self):
        DocModel.__init__(self)
        
        
    def getCurMonitorObjs(self, conditions={}, allowTypes=[]):
        """
        getCurMonitorObjs
        """
        UserControl.addCtrlCondition(conditions)
        rs=[]
        
        for smt in subMoTypes:
            if not allowTypes:
                rs1= self._getRefMeObjects('location', smt, conditions=conditions)
                rs.extend(rs1)
            elif smt.__name__ in allowTypes:
                rs1= self._getRefMeObjects('location', smt, conditions=conditions)
                rs.extend(rs1)

        return rs


    
    def addMo(self, mo):
        mo.location = self;
    

        
    @classmethod
    def getDefault(cls):
        "获取用户默认的分组"
        _condition={"locType":"default"}
        UserControl.addCtrlCondition(_condition)
        
        tb = cls._getDbTable()
        mObj = tb.find_one(_condition)
        if not mObj:return None
        defLoc = cls._loadObjFromMap(mObj)
        return defLoc


