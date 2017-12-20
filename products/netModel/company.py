#coding=utf-8
from products.netModel.centerDocModel import CenterDocModel


class Company(CenterDocModel):
    dbCollection = 'Company'
    
    def __init__(self, uid=None):
        CenterDocModel.__init__(self)
        
        self._medata.update(dict(
            _id = uid,
            logo = "", #公司log图标
            address = "", #公司地址
            description = "", #描述
        ))

    @property
    def user(self):
        from products.netModel.user.user import User
        users = self._getRefMeObjects("ownCompany", User, {})
        if users: return users[0]
        return None
        