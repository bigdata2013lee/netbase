#coding=utf-8
from products.netModel.templates.base import BaseObj
from products.netUtils import xutils
from products.netModel.baseModel import RefDocObject

class Threshold(BaseObj):
    def __init__(self):
        self._medata = dict(
            severity=3,
            monitored=True,
            zname="", #中文名
            description="", #说明备注
        )

        
    def getType(self):
        return self._medata['type']
        
    @classmethod
    def createInst(cls, medata):
        "通过元数据创建 Threshold 子类实例"
        allowTypes = dict(MinThreshold=MinThreshold, MaxThreshold=MaxThreshold, 
                          RangeThreshold=RangeThreshold,StatusThreshold=StatusThreshold,
                          KeyThreshold=KeyThreshold,CompareThreshold=CompareThreshold)
        th = allowTypes.get(medata['type'])("")
        th._medata = medata
        
        return th

    def _getRefInfo(self):
        """
        得到当前对象的序列化唯一标示
        """
        return RefDocObject.getRefInfo(self)
        
        
        
        
        
#########################################################################


class MinThreshold(Threshold):
    def __init__(self, uname):
        Threshold.__init__(self)
        self._medata.update(dict(
            type=self.__class__.__name__, uname=uname, min=0
        ))
        
    def formatEvtMessage(self, title, val, unit = None, eventInfo={}):
        min = self.get("min")
        if unit == "Bit":
            val = xutils.byte2readable(val)
            
        zname = (self.get("zname", self.uname) or "")
        formats  = self.get("format", u"%(title)s %(zname)s:%(val)s低于设定的最小阀值:%(min)s")
        data=dict(title=title, val=val, min=min, zname=zname)
        for key, val in eventInfo.items():
            data.update({"eventInfo." + key : val})
        return formats %data
    
class MaxThreshold(Threshold):
    def __init__(self, uname):
        Threshold.__init__(self)
        self._medata.update(dict(
            type=self.__class__.__name__, uname=uname, max=100 
        ))
    
    def formatEvtMessage(self, title, val, unit=None, eventInfo={}):
        val=round(val,3)
        max = self.get("max")
        if unit == "Bit":
            val = xutils.byte2readable(val)
        zname = (self.get("zname", self.uname) or "")
        formats  = self.get("format", u"%(title)s %(zname)s:%(val)s超过设定的最大阀值:%(max)s")
        data = dict(title=str(title), val=val, max=max, zname=zname)    
        for key, val in eventInfo.items():
            data.update({"eventInfo." + key : val})
        return formats %data

class RangeThreshold(Threshold):
    def __init__(self, uname):
        Threshold.__init__(self)
        self._medata.update(dict(
            type=self.__class__.__name__, uname=uname, min=0, max=100 
        ))
    
    def formatEvtMessage(self, title, val, unit=None, eventInfo={}):
        min = self.get("min")
        max = self.get("max")
        if unit == "Bit":
            val = xutils.byte2readable(val)
            
        zname = (self.get("zname", self.uname) or "")
        formats  = self.get("format", u"%(title)s %(zname)s:%(val)s 超过设定的范围阀值:%(min)s~%(max)s")
        data = dict(title=title, val=val,min=min, max=max, zname=zname)
        for key, val in eventInfo.items():
            data.update({"eventInfo." + key : val})
        return formats %data
    
   
class StatusThreshold(Threshold):
    """
    状态阀值
    """
    def __init__(self, uname):
        Threshold.__init__(self)
        self._medata.update(dict(
            type=self.__class__.__name__, uname=uname,status=None
        ))
    def formatEvtMessage(self,title,val, eventInfo={}):
            status=self.get("status")
            zname = (self.get("zname", self.uname) or "")
            formats  = self.get("format", u"%(title)s %(zname)s:%(val)s 相对于%(status)s状态发生改变")
            data = dict(title=title, val=val,zname=zname,status=status)
            for key, val in eventInfo.items():
                data.update({"eventInfo." + key : val})
            return formats %data
        
class KeyThreshold(Threshold):
    """
    关键字阀值
    """
    def __init__(self, uname):
        Threshold.__init__(self)
        self._medata.update(dict(
            type=self.__class__.__name__, uname=uname, key=None
        ))

    def formatEvtMessage(self, title, val, eventInfo={}):
        key=str(self.get("key"))
        zname = (self.get("zname", self.uname) or "")
        formats  = self.get("format", u"%(title)s %(zname)s:%(val)s匹配关键字%(key)s")
        data = dict(title=title, val=val,key=key, zname=zname)
        for key, val in eventInfo.items():
            data.update({"eventInfo." + key : val})
        return formats %data
    
class CompareThreshold(Threshold):
    """
    比对阀值
    """
    def __init__(self, uname):
        Threshold.__init__(self)
        self._medata.update(dict(
            type=self.__class__.__name__, uname=uname
        ))

    def formatEvtMessage(self, title, val, eventInfo={}):
        zname = (self.get("zname", self.uname) or "").encode("utf-8")
        formats  = self.get("format", u"%(title)s %(zname)s:%(val)s 相对于上次发生变化")
        data = dict(title=title, val=val, zname=zname)
        for key, val in eventInfo.items():
            data.update({"eventInfo." + key : val})
        return formats %data
