#coding=utf-8

from threading import local
from products.netModel.user.user import User


_userLocal = local()


class UserControl(object):
    
    @staticmethod
    def setUser(user=None):
        _userLocal.user = user
        
    @staticmethod
    def getUser():
        return getattr(_userLocal, 'user', None)
    
    
    @staticmethod
    def hasPermission(perm, user=None):
        return True
    
    
    @staticmethod
    def addCtrlCondition(condition):
        u = UserControl.getUser()
        ownCompany = None
        ownCompanyRefInfo = None
        if u: ownCompany = u.ownCompany
        if ownCompany:
            ownCompanyRefInfo = ownCompany._getRefInfo()
        
        _condition = {"ownCompany":ownCompanyRefInfo}
        
        condition.update(_condition)
        
    @staticmethod
    def login(name, pwd):
        users = User._findObjects({"_id":name, "password":pwd})
        if not users:
            raise Exception("Can't login with name:%s, pwd:%s" %(name, pwd))
        
        UserControl.setUser(users[0])
    

if __name__ == "__main__":
    pass
    
       

