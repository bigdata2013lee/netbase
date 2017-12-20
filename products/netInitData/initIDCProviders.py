#coding=utf-8
import ConfigParser
from products.netUtils.xutils import nbPath as _p
from products.netModel.idcProvider import IdcProvider

def _getConf():
    cf=ConfigParser.ConfigParser()
    cf.read(_p("/products/netInitData/initdata.conf"))
    return cf


def initProviders():
    cf = _getConf()
    for  option in cf.options("IdcProviders"):
        try:
            info=eval(cf.get("IdcProviders", option))
        except:
            print "数据格式不正确!"
            continue
        
        p = IdcProvider()
        p.__extMedata__(info)
        p._saveObj()
    
    
    
if __name__ == "__main__":
    initProviders()
    
    
    
    