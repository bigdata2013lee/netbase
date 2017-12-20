#coding=utf-8
import ConfigParser
from products.netModel.collectPoint import CollectPoint
from products.netUtils.xutils import nbPath as _p

def _getConf():
    cf=ConfigParser.ConfigParser()
    cf.read(_p("/products/netInitData/initdata.conf"))
    return cf

def initCollectPoint():
    cf = _getConf()
    for  option in cf.options("collectPoint"):
        try:
            info=eval(cf.get("collectPoint", option))
        except:
            print "数据格式不正确!"
            continue
        cpt=CollectPoint()
        cpt._medata.update(info)
        cpt._saveObj()