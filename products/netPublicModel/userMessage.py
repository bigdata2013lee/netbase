#coding=utf-8
from products.netPublicModel.userControl import UserControl




class UserMsg(object):
    
    _max=10
    
    @classmethod
    def _user(cls, ):
        return UserControl.getUser()
    
    @classmethod
    def _insert(cls, msgtype, msg):
        u = cls._user()
        if not u: return False
        
        if not hasattr(u, "__user_message__"): u.__user_message__ = []
        length = len(u.__user_message__)
        if length >= cls._max: 
            u.__user_message__ = u.__user_message__[length - cls._max + 1 : length]
        
        u.__user_message__.append({"msgtype":msgtype, "msg": msg})
        
        return True
    
    @classmethod
    def warn(cls, msg):
        cls._insert("warn", msg)
        
    
    @classmethod
    def info(cls, msg):
        cls._insert("info", msg)
    
    
    @classmethod
    def got(cls):
        u = cls._user()
        if not u: return None
        if not getattr(u, "__user_message__", []): return None
        
        return  u.__user_message__.pop(0)
    
    
    