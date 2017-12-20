#coding=utf-8
import ConfigParser
from products.netBilling.Billing import Billing
from products.netUtils.xutils import nbPath as _p

def _getConf():
    cf=ConfigParser.ConfigParser()
    cf.read(_p("/products/netInitData/initdata.conf"))
    return cf

def initBillings():
    
    cf = _getConf()
    for  option in cf.options("billings"):
        try:
            info=eval(cf.get("billings", option))
        except:
            print "数据格式不正确!"
        
        b = Billing() 
        b._medata.update(info)
        b._saveObj()


if __name__ == "__main__":
    initBillings()
    
    
    
    