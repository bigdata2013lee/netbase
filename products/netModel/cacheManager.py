#coding=utf-8

import types
from products.netUtils.mcClient import McClient, TimeoutConf



class CacheModel(object):
    
    #_allowCache = True
    

        
    @classmethod
    def _c_loadObj(cls, uid):
        if not uid: return None
        uid = str(uid)
        if not getattr(cls, '_allowCache', True): return None
        medata = McClient.getClient("objects").get("%s[%s]" %(cls.__name__, uid))
        if medata:
            inst = cls()
            inst._medata = medata
            return inst
        return None
    
    @classmethod
    def _c_setObj(cls, obj):
        if not getattr(cls, '_allowCache', True): return
        uid = obj.getUid()
        if not uid: return
        if type(uid) not in types.StringTypes: uid = str(uid)
        
        McClient.getClient("objects").set("%s[%s]" %(cls.__name__, uid), obj._medata, TimeoutConf.objectsTimeout)
        
     
    @classmethod   
    def _c_delObj(cls, obj):
        if not getattr(cls, '_allowCache', True): return
        if not obj: return
        uid = obj.getUid()
        if not uid: return
        if type(uid) not in types.StringTypes: uid = str(uid)
        McClient.getClient("objects").delete("%s[%s]" %(cls.__name__, uid))
    

        
        
    
    
