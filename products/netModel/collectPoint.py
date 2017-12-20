from products.netModel.baseModel import DocModel
from products.netModel import medata
class CollectPoint(DocModel):
    dbCollection = 'CollectPoint'
    
    def __init__(self, uid=None):
        DocModel.__init__(self)
        self._medata.update(dict(
            _id = uid,
        ))
    hostIp=medata.IPproperty("hostIp", "127.0.0.1")
    port=medata.plain("port", 8888)
    ss=medata.plain("ss", "guangdong")
        
    @classmethod
    def _loadByHostIp(cls, hostIp):
        objs = cls._findObjects(conditions={"hostIp":hostIp}, limit=1)
        if(objs): return objs[0]
        return None