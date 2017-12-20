#coding=utf-8
from products.netModel import medata
from products.netswgl.model.swglDocModel import SwglDocModel

class CpcAddr(SwglDocModel):
    "地址"
    dbCollection = 'CpcAddr'
    
    def __init__(self, uid=None):
        SwglDocModel.__init__(self)
        self._medata.update(dict(
            _id=uid, 
        ))
        
    pid= medata.plain("pid", "") #父级编号
    
    


class Domain(SwglDocModel):
    "领域"
    dbCollection = 'Domain'
    
    def __init__(self, uid=None):
        SwglDocModel.__init__(self)
        self._medata.update(dict(
            _id=uid, 
        ))
        
    pid= medata.plain("pid", "") #父级编号           