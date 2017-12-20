#coding=utf-8
from products.netModel import medata
from products.netswgl.model.swglDocModel import SwglDocModel

class SEngineerFavorit(SwglDocModel):
    "工程师收藏"
    dbCollection = 'SEngineerFavorit'
    def __init__(self, uid=None):
        SwglDocModel.__init__(self)
        self._medata.update(dict(
            _id=uid, 
        ))        
        
        
    user= medata.doc("user") #收藏用户
    sEngineer= medata.doc("sEngineer") #被收藏的工程师
    time=medata.plain("time", 0) #收藏时间