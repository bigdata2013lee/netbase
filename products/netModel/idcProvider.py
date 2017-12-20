#coding=utf-8
from products.netModel.centerDocModel import CenterDocModel


class IdcProvider(CenterDocModel):
    dbCollection = 'IdcProvider'
    
    def __init__(self, uid=None):
        CenterDocModel.__init__(self)
        
        self._medata.update(dict(
            _id = uid,
            title = ""
        ))

    