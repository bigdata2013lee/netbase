#coding=utf-8
from products.netModel.templates.threshold import Threshold
from products.netModel.templates.base import BaseObj


class DataPoint(BaseObj):
    def __init__(self, uname):
        self._medata = dict(
            uname = uname,
            valueType="Num",
            unit="Decimal",
            median = 32,
            type = "ABSOLUTE",
            thresholds = {},
        )
        

        
    @property
    def _thresholds(self):
        return self._medata["thresholds"]
     
    def addThreshold(self, th):
        """
        添加阀值
        @param th: <Threshold> 
        @return: 
        """
        if not th.uname: raise Exception('Threshold uname can not be empty!')
        self._thresholds[th.uname] = th._medata
        return self
    
    def deleteThreshold(self, thName):
        """
        删除一个阀值
        @param thName: 阀值名称 type->string 
        """
        if thName in self._thresholds:
            del self._thresholds[thName]
            
    @property
    def thresholds(self):
        """
        获取所有的阀值
        @return: <{thName:<Threshold>}>
        """
        dps = {}
        for thName, thMedata in self._thresholds.items():
            dp = Threshold.createInst(thMedata)
            dps[thName] = dp
        return dps
    
   
    
    @classmethod
    def createInst(cls, medata):    
        dp = DataPoint("")
        dp._medata.update(medata)
        return dp
