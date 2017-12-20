#coding=utf-8
import ConfigParser
from products.netModel.user.saleUser import SaleUser
from products.netUtils.xutils import nbPath as _p
from products.netModel.idcProvider import IdcProvider

def _getConf():
    cf=ConfigParser.ConfigParser()
    cf.read(_p("/products/netInitData/initdata.conf"))
    return cf


def initSaleUsers():
    cf = _getConf()
    for  option in cf.options("saleUsers"):
        try:
            info=eval(cf.get("saleUsers", option))
        except:
            print "数据格式不正确!"
            continue
        idcProviderId = info.get("idcProviderId")
        idcProvider = IdcProvider._loadObj(idcProviderId)
        del info["idcProviderId"]
        su = SaleUser() 
        su._medata.update(info)
        su.idcProvider = idcProvider
        su._saveObj()
    
    
    
if __name__ == "__main__":
    initSaleUsers()
    
    
    
    