#coding=utf-8

import ConfigParser
from products.netUtils.xutils import nbPath as _p


class Settings(object):
    
    def __init__(self, name):
        self._loadConf(name)
    
    def _loadConf(self, name):
        cf=ConfigParser.ConfigParser()
        cf.read(_p("/etc/%s.conf" %name))
        self._cf = cf
        
    def get(self, section, option):
            return self._cf.get(section, option)
    
    def getAsInt(self, section, option):
            num = self._cf.get(section, option)
            return int(num)

class ManagerSettings(object):
    
    @classmethod
    def getSettings(cls):
        inst = getattr(cls, "SETTINGS_INST", None)
        if not inst:
            inst = Settings("manager")
            cls.SETTINGS_INST = inst
        
        return inst
    
class DbSettings(object):
    
    @classmethod
    def getSettings(cls):
        inst = getattr(cls, "SETTINGS_INST", None)
        if not inst:
            inst = Settings("db")
            cls.SETTINGS_INST = inst
        
        return inst
    
class CollectorSettings(object):
    
    @classmethod
    def getSettings(cls):
        inst = getattr(cls, "SETTINGS_INST", None)
        if not inst:
            inst = Settings("collector")
            cls.SETTINGS_INST = inst
        
        return inst
        
class MemCacheSettings(object):
    
    @classmethod
    def getSettings(cls):
        inst = getattr(cls, "SETTINGS_INST", None)
        if not inst:
            inst = Settings("memcache")
            cls.SETTINGS_INST = inst
        
        return inst        
    
    
    
    
    