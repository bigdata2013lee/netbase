#coding=utf-8
from products.netUtils import xutils
import pickle

def __getRefDocObject():
    from products.netModel.baseModel import RefDocObject
    return RefDocObject


class MedataProperty(property):
    pass

def plain(name, default=None):
    
    def getx(self):
        return self._medata.get(name, default)
    
    def setx(self, val):
        self._saveProperty2(name, val)
    
    def delx(self):
        del self._medata[name]
        
    p = MedataProperty(fget=getx, fset=setx, fdel=delx)
    p.medataName = name
    p.defaultVal = default
    return p


def Dictproperty(name, default={}):
    
    def getx(self):
        return self._medata.get(name)
    
    def setx(self, val):
        self._medata.get(name).update(val)
        self._saveProperty(name)
    
    def delx(self):
        del self._medata[name]
        
    p = MedataProperty(fget=getx, fset=setx, fdel=delx)
    p.medataName = name
    p.defaultVal = default
    return p

def IPproperty(name, default=None):
    
    def getx(self):
        return self._medata.get(name)
    
    def setx(self, val):
        if not xutils.isValidIp(val): raise Exception("Ip[%s] is not valid.")
        self._saveProperty2(name, val)
    
    def delx(self):
        del self._medata[name]
        
    p = MedataProperty(fget=getx, fset=setx, fdel=delx)
    p.medataName = name
    p.defaultVal = default
    return p

def doc(name):
    
    def getx(self):
        return __getRefDocObject().getInstance(self._medata.get(name,None))
    
    def setx(self, val):
        self._saveProperty2(name,val)
    
    def delx(self):
        del self._medata[name]
        
    p = MedataProperty(fget=getx, fset=setx, fdel=delx)
    p.medataName = name
    p.defaultVal = None
    return p

def Pickleproterpy(name, default=None):    
    def getx(self):
        return pickle.loads(self._medata.get(name))

    def setx(self, val):
        _val = pickle.dumps(val)
        self._saveProperty2(name, _val)
        
    def delx(self):
        del self._medata[name]
        
    p = MedataProperty(fget=getx, fset=setx, fdel=delx)
    p.medataName = name
    p.defaultVal = default
    return p



