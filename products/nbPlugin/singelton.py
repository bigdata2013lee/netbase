'''
Created on 2013-3-26

@author: Administrator
'''
class Singleton(object):
    def __new__(cls,*args,**kw):
        if not hasattr(cls,"_instance"):
            org = super(Singleton,cls)
            cls._instance = org.__new__(cls,*args,**kw)
        return cls._instance

class ConfigObject(Singleton):
        running = True
        pluginDict = {}
        configDict = {}
