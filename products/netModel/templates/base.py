#coding=utf-8

class BaseObj(object):
    
    @property
    def uname(self):
        return self._medata.get("uname", None)
        
    def get(self, name, default=None):
        return self._medata.get(name, default)
    
    def set(self, name, value):
        self._medata[name]= value