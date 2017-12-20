#coding=utf-8
from products.netModel.user.baseUser import BaseUser
from products.netModel.user.user import User
from products.netModel.saleOpRecord import SaleOpRecord

class SaleUser(BaseUser):
    dbCollection = 'SaleUser'
    
    def __init__(self, uid=None):
        BaseUser.__init__(self, uid=uid)
        self.__extMedata__(dict())
    
    
    @property
    def users(self):
        """
        用户列表
        """ 
        return self._getRefMeObjects("saleUser",User, conditions={})


    def findOpRecords(self, conditions={}, sortInfo=None, skip=0, limit=400):
        conditions['sale'] = self._getRefInfo()
        rs = SaleOpRecord._findObjects(conditions=conditions, sortInfo=sortInfo, skip=skip, limit=limit)
        return rs