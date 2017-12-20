#coding=utf-8
import ConfigParser
from products.netModel.user.engineerUser import EngineerUser
from products.netUtils.xutils import nbPath as _p
from products.netModel.idcProvider import IdcProvider

def _getConf():
    cf=ConfigParser.ConfigParser()
    cf.read(_p("/products/netInitData/initdata.conf"))
    return cf

def initEngineers():
    
    cf = _getConf()
    for  option in cf.options("enginners"):
        try:
            info=eval(cf.get("enginners", option))
        except:
            print "数据格式不正确!"
        idcProviderId = info.get("idcProviderId")
        idcProvider = IdcProvider._loadObj(idcProviderId)
        del info["idcProviderId"]
        eu = EngineerUser() 
        eu._medata.update(info)
        eu.idcProvider = idcProvider
        eu._saveObj()


if __name__ == "__main__":
    initEngineers()
    
    
    
    