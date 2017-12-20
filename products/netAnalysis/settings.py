#coding=utf-8
import ConfigParser
from products.netUtils.xutils import nbPath as _p

_vars = dict(_isLoaded = False, cf = None)


def _loadConf():
    cf=ConfigParser.ConfigParser()
    cf.read(_p("/etc/netAnalysis.conf"))
    _vars["cf"] = cf
    _vars["_isLoaded"] = True
    
def get(section, option):
        if not _vars["_isLoaded"]: _loadConf()
        return _vars['cf'].get(section, option)

def getAsInt(section, option):
        if not _vars["_isLoaded"]: _loadConf()
        num = _vars['cf'].get(section, option)
        
        return int(num)
        