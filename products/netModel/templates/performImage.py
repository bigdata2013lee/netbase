#coding=utf-8
from products.netModel.baseModel import DocModel, RefDocObject

class ImagePoint(object):
    """
    图像点
    """
    def __init__(self, uname):
        self.uname = uname
        self.dsName = ""
        self.dpName = ""
        self.unit = ""
        self.color = ""
        self.lineWidth = ""
        self.type = "line"
        
    def toDict(self):
        return {
                "uname":self.uname,
                "dsName":self.dsName,
                "dpName":self.dpName,
                "unit":self.unit,
                "color":self.color,
                "lineWidth":self.lineWidth,
                "type":self.type
        }
        
    @classmethod
    def createInst(cls, dictData):
        """
        通过dict构建图像点对象实例
        """
        iPoint = cls("")
        for k, v in dictData.items():
            setattr(iPoint, k, v)
            
        return iPoint
    
class PerformImage(DocModel):
    """
    性能图像定义
    """
    dbCollection = 'PerformImage'
    
    def __init__(self , uid=None):
        self._id = uid
        self._imagePoints = {}  #数据来源配置
        self._template = None #模板引用
        self.title = "" #名称
        self.description = "" #描述
        self.width = 860 #宽度
        self.height = 400 #高度
    

    def __after_saveObj__(self):
        self._saveProperty(["title", "description", 'width', 'height', '_imagePoints'])
     
    @property
    def template(self):
        return RefDocObject.getInstance(self._template)
    
    @template.setter
    def template(self, tpl):
        self._saveDocProperty(tpl, '_template')
        
             
    @property
    def imagePoints(self):
        """
        imagePoints
        @return: dict
        """
        ret = {}
        for uname, iPointDict in self._imagePoints.items():
            ret [uname] = ImagePoint.createInst(iPointDict)
        return ret
    
    def addImagePoint(self, iPoint):
        """
        addImagePoint
        @param iPoint: 图像点
        """
        dictData = iPoint.toDict()
        uname = dictData["uname"]
        self._imagePoints[uname] = dictData
        xPath = "_imagePoints.%s" % dictData['uname']
        self._commUpdate({"$set":{xPath: dictData}})
        
    
    def deleteImagePoint(self, iPointName):
        """
        deleteImagePoint
        @param iPointName: 图像点 uname
        """
        if not self._imagePoints.has_key(iPointName): return
            
        del self._imagePoints[iPointName]
        xPath = "_imagePoints.%s" % iPointName
        self._commUpdate({"$unset":{xPath:1}})    
    
    
        
        
