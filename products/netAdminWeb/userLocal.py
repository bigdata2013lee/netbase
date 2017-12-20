#coding=utf-8
from threading import local

_admin_user_local = local()

class UserLocal(object):
    
    @staticmethod
    def getUserType():
        return getattr(_admin_user_local, 'userType', None)
    
    @staticmethod
    def setUserType(userType):
        _admin_user_local.userType = userType
    