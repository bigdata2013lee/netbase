#coding=utf-8
from products.netModel.baseModel import DocModel

class MWeight(DocModel):
    "监控组件"
    
    dbCollection = 'MWeight'
    
    def __init__(self, uid=None):
        self._id = uid
        self.title = ""
        self.description = ""
        self.targetMOType = "" #适用监控对象类型
        
        
    def __after_saveObj__(self):
        self._saveProperty(['title', 'description', 'targetMOType'])
