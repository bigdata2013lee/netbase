#coding=utf-8
from products.netModel import medata
from products.netModel.baseModel import BaseComponentModel


class CustomerMap(BaseComponentModel):
    '''
    CustomerMap
    '''
    dbCollection = 'CustomerMap'
    
    def __init__(self, uid=None):
        BaseComponentModel.__init__(self)
        self._medata.update(dict(
            _id = uid,
        ))
        
    mapData = medata.plain("mapData", {})
    zIndex = medata.plain("zIndex", 0)
    
 
    
            