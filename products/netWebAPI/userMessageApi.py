#coding=utf-8
from products.netWebAPI.base import BaseApi
from products.netPublicModel.userMessage import UserMsg



class UserMessageApi(BaseApi):
    
    def got(self):
        msg = None
        try:
            msg = UserMsg.got()
        except Exception, e:
            pass
        
        return msg
    
    def warn(self, msg):
        return UserMsg.warn(msg)
    
    
    def info(self, msg):
        return UserMsg.info(msg)
