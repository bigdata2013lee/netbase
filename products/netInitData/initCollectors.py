#coding=utf-8
import ConfigParser
from products.netModel.collector import Collector
from products.netUtils.xutils import nbPath as _p

def _getConf():
    cf=ConfigParser.ConfigParser()
    cf.read(_p("/products/netInitData/initdata.conf"))
    return cf

def initCollectors():
    
    cf = _getConf()
    for  option in cf.options("collectors"):
        try:
            info=eval(cf.get("collectors", option))
        except:
            print "数据格式不正确!"
            
        col = Collector() 
        col._medata.update(info)
        col._saveObj()


if __name__ == "__main__":
    initCollectors()
    
    
    
    