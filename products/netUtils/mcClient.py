#coding=utf-8
import memcache
from products.netUtils.settings import MemCacheSettings



_clients={}
   

class TimeoutConf(object):
    perfvalueTimeout=60 #性能值过期时间
    statusValueTimeout=60 #事件状态值过期时间
    perfImgDatasTimeout=300 #性能图数据过期时间（天|周|月）
    objectsTimeout=600
    availabilityTimeout=120 #

class McClient(object):
    
    @classmethod
    def getClient(cls, name):
        mc =  _clients.get(name,None)
        if not mc:
            settings = MemCacheSettings.getSettings()
            host = settings.get(name, "host")
            port = settings.get(name, "port")
            print "log: conn to memcache %s:%s" %(host,port)
            mc = memcache.Client(['%s:%s' %(host,port)], debug=0)
            _clients[name]=mc
            
        return mc
#--------------------------------------------------------    
    
def availabilityCacheDecorator(func):
    """
    可用性图像缓存装饰器,主要装饰后台 API方法
    """
    def new_func(*args, **argkw):
        from products.netPublicModel.userControl import UserControl
        user =  UserControl.getUser()
        _mc = McClient.getClient("perfs")
        if "websiteClsUid" in argkw:
            _cacheKey=str("availabilityCache:%s_%s_%s_%s" %(user.getUid(), func.__name__, argkw["websiteClsUid"], argkw.get("timeRange","")))
        else: 
            _cacheKey=str("availabilityCache:%s_%s_%s_%s_%s_%s" %(user.getUid(), func.__name__, argkw["orgType"], argkw["orgUid"], argkw.get("locUid",""), argkw["timeRange"]))
        _cacheDatas = _mc.get(_cacheKey)
        if _cacheDatas is not None:
            return _cacheDatas
        data = func(*args, **argkw)
        _mc.set(_cacheKey, data, TimeoutConf.availabilityTimeout)
        return data

    return new_func


def getPerfDataByTimeUnitCacheDecorator(func):
    """
    性能数据缓存装饰器
    """
    
    def new_func(*args, **argkw):
        _mc = McClient.getClient("perfs")
        _cacheKey =str("perf_img_%s[%s_%s]" %(args[5],args[2],args[3]))
        _cacheDatas = _mc.get(_cacheKey)
        if _cacheDatas is not None:
            return _cacheDatas
        data = func(*args, **argkw)
        _mc.set(_cacheKey, data, TimeoutConf.perfImgDatasTimeout)
        return data

    return new_func



def getPerfValueCacheDecorator(func):
    """
    性能数据缓存装饰器
    """
    
    def new_func(*args, **argkw):
        _mc = McClient.getClient("perfs")
        _cacheKey = "%s_%s" %(args[0], args[1])
        _cacheVal = _mc.get(_cacheKey)
        if _cacheVal is not None:
            #print "log: get data in cache perfval=%s" %_cacheVal
            if _cacheVal == "NA": return None
            else: return _cacheVal
        val = func(*args, **argkw)
        #print "log: get data in mongod perfval=%s" % val
        if val is None:
            _mc.set(_cacheKey, "NA", TimeoutConf.perfvalueTimeout)
        else:
            _mc.set(_cacheKey, val, TimeoutConf.perfvalueTimeout)
        return val
                
    return new_func


def getEventStatusValueCacheDecorator(func):
    """
    """
    
    def new_func(*args, **argkw):
        _mc = McClient.getClient("perfs")
        _cacheKey = "%s_%s" %(args[0], args[0])
        #print "_cacheKey:%s" %_cacheKey
        _cacheVal = _mc.get(_cacheKey)
        if _cacheVal is not None:
            #print "log: get data in cache statusval=%s" %_cacheVal
            if _cacheVal == "NA": return None
            else: return _cacheVal
        val = func(*args, **argkw)
        #print "log: get data in mongod statusval=%s" % val
        if val is None:
            _mc.set(_cacheKey, "NA", TimeoutConf.perfvalueTimeout)
        else:
            _mc.set(_cacheKey, val, TimeoutConf.perfvalueTimeout)
        return val
                
    return new_func



def getSummaryInfo_DeviceClass(func):
    "装饰获取概要，综合评分方法"
    def new_func(*args, **argkw):
        from products.netPublicModel.userControl import UserControl
        user =  UserControl.getUser()
        _mc = McClient.getClient("perfs")
        _cacheKey =str("%s:getSummaryInfo_DeviceClass" %user.getUid())
        _cacheDatas = _mc.get(_cacheKey)
        if _cacheDatas is not None:
            return _cacheDatas
        data = func(*args, **argkw)
        _mc.set(_cacheKey, data, 30)
        return data

    return new_func



