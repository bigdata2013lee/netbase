#coding=utf-8
from products.netAdminWeb.userLocal import UserLocal


def _getUserType(userType):
    from products.netModel.user.saleUser import SaleUser
    from products.netModel.user.engineerUser import EngineerUser
    from products.netModel.operation.operationer import Operationer
    from products.netModel.user.adminUser import AdminUser
    
    
    for userCls in [SaleUser, EngineerUser,AdminUser, Operationer]:
        if userCls.__name__ == userType: return userCls
    
    return None


class NetBaseBackend(object):
    def authenticate(self,username=None, password=None):
        userType = UserLocal.getUserType()
        if not userType:
            print "Warning: unknow user type while authenticate"
            return None
        
        User = _getUserType(userType)
        userObj = User._loadByUserName(username)
        import hashlib
        if userObj and userObj.password == hashlib.md5(password).hexdigest():
            return  userObj
        return None
    
    def get_user(self, user_id):
        userType = UserLocal.getUserType()
        user = _getUserType(userType)
        return user._loadObj(user_id)
    