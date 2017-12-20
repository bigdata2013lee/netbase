#coding=utf-8
from products.netModel.centerDocModel import CenterDocModel
from products.netModel import medata


class SaleOpRecord(CenterDocModel):
    dbCollection = 'SaleOpRecord'
    
    def __init__(self, uid=None):
        CenterDocModel.__init__(self)
        self._medata.update(dict(_id = uid))
            
    sale = medata.doc("sale")
    opTime = medata.plain("opTime")
    operation = medata.plain("operation", None)
    opDetail = medata.plain("opDetail", None)
    
    
if __name__ == "__main__":
    pass