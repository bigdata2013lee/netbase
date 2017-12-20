#coding=utf-8
from products.netModel.centerDocModel import CenterDocModel
from products.netModel import medata

class UserLookForPwdRec(CenterDocModel):
    dbCollection = 'UserLookForPwdRec'
    
    def __init__(self, uid=None):
        CenterDocModel.__init__(self)
        

    userId=medata.plain("userId", "")
    code=medata.plain("code", 0)
    stamp=medata.plain("stamp", 0)
    status=medata.plain("status", False)