#coding=utf-8
from products.netModel.baseModel import DocModel
from products.netModel import  mongodbManager as dbManager

class CenterDocModel(DocModel):
    
    def __init__(self):
        DocModel.__init__(self)
    
    
    @classmethod
    def _getDbTable(cls):
        """
            得到当前对象的mongodb集合表
        """
        db = dbManager.getNetCenterDB()
        table = getattr(db, getattr(cls,"dbCollection","") or cls.__name__)
        return table

