#coding=utf-8
from products.netWebAPI.base import BaseApi, apiAccessSettings
from products.netPerData.perDataMerger import PerDataMerger
from products.netPublicModel.userControl import UserControl
from products.netModel.middleware.mwNginx import MwNginx
from products.netModel.middleware.mwApache import MwApache
from products.netModel.middleware.mwTomcat import MwTomcat
from products.netModel.collector import Collector
from products.netPublicModel.modelManager import ModelManager as MM



#--------获得Middleware 性能-----------------------------------------------------------------------
class Perf(object):
    def _getPerf(self, mid, timeUnit,  dpName):
        coll = mid.collector
        dbName = mid._getPerfDbName()
        baseTpl = mid.getBaseTemplate()
        if not baseTpl:
            print "warning: Can't find the base template on Middleware %s" %mid.getUid()
            return []
        tableName = mid._getPerfTablName(baseTpl.getUid(), "middlewareParser", dpName) 
        datas = PerDataMerger().getPerfDataByTimeUnit(coll, dbName, tableName, timeUnit)
        return datas

    def getNginxConnectionPerfs(self, mw, timeUnit):
        coll = mw.collector
        dbName = mw._getPerfDbName()
        baseTpl = mw.getBaseTemplate()
        if not baseTpl:
            print "warning: Can't find the base template on MW %s" %mw.getUid()
            return []
        tableName1 = mw._getPerfTablName(baseTpl.getUid(), "MwNginx", "connection")
        
        datas1 = PerDataMerger().getPerfDataByTimeUnit(coll, dbName, tableName1, mw.createTime, timeUnit)
        return datas1
    
    def getApacheConnectionPerfs(self, mw, timeUnit):
        coll = mw.collector
        dbName = mw._getPerfDbName()
        baseTpl = mw.getBaseTemplate()
        if not baseTpl:
            print "warning: Can't find the base template on MW %s" %mw.getUid()
            return []
        tableName1 = mw._getPerfTablName(baseTpl.getUid(), "MwApache", "connection")
        
        datas1 = PerDataMerger().getPerfDataByTimeUnit(coll, dbName, tableName1, mw.createTime, timeUnit)
        return datas1
    
    def getTomcatConnectionPerfs(self, mw, timeUnit):
        coll = mw.collector
        dbName = mw._getPerfDbName()
        baseTpl = mw.getBaseTemplate()
        if not baseTpl:
            print "warning: Can't find the base template on MW %s" %mw.getUid()
            return []
        tableName1 = mw._getPerfTablName(baseTpl.getUid(), "MwTomcat", "cThreadCount")
        
        datas1 = PerDataMerger().getPerfDataByTimeUnit(coll, dbName, tableName1, mw.createTime, timeUnit)
        return datas1

#-----------------------------------------------------------------------------------------------
class MiddlewareApi(BaseApi):
        
    def middlewareClsCounts(self):
        "分类统计各中间件实例数量"
        conditions={}
        UserControl.addCtrlCondition(conditions)
        mwClsList = [MwNginx,MwApache, MwTomcat]
        rs = {}
        for mwCls in  mwClsList:
            count= mwCls._countObjects(conditions=conditions)
            rs[mwCls.__name__] = count
        return rs
    
    def __addMiddleware(self, mwCls, host, port="80", title="", collector="", ssl=False, httpUsername="", httpPassword=""):
        coll = Collector._loadObj(collector)
        if not coll: return "warn:没有找到收集器"
        if not host: return "warn:没有找到主机"
        conditions={}
        ownCompany = UserControl.getUser().ownCompany
        UserControl.addCtrlCondition(conditions)
        if  mwCls._countObjects(conditions=conditions) > 100: return "warn:添加失败,您不能添加过多的服务器监控"
        mw = mwCls()
        mw.host = host
        mw.port = port
        mw.title = title
        mw.ssl = ssl
        mw.httpUsername = httpUsername
        mw.httpPassword = httpPassword
        
        mw.ownCompany=ownCompany
        mw.collector = coll
        
        mw._saveObj()
        
        dr = MM.getMod('dataRoot')
        dr.fireEvent("add_new_middleware", mw=mw)
        return "成功添加中间件"
#--------------------------------------------------------------------------------------------------------------

        
    def listNginxs(self):
        conditions={}
        UserControl.addCtrlCondition(conditions)
        mws = MwNginx._findObjects(conditions=conditions)
        return mws
    
    @apiAccessSettings("add")
    def addNginx(self, host, port="80", title="", collector="", ssl=False, httpUsername="", httpPassword=""):
        return self.__addMiddleware(MwNginx, host, port, title, collector, ssl, httpUsername, httpPassword)
            
    @apiAccessSettings("edit")            
    def editNginx(self, moUid, port="80", title="", ssl=False, httpUsername="", httpPassword=""):
        mw = MwNginx._loadObj(moUid)
        if not mw:return "warn:编辑失败"
        mw.port = port
        mw.title = title
        mw.ssl = ssl
        mw.httpUsername = httpUsername
        if  httpPassword: mw.httpPassword = httpPassword
        
        return "编辑成功"
        
    @apiAccessSettings("del")
    def removeNginx(self,uid):
        mw = MwNginx._loadObj(uid)
        if not mw: return "warn:删除失败，服务器已经不存在"
        mw.remove()
        return "删除成功"
    
    def getNginxConnPerfs(self, uid, timeUnit="day"):
        mw = MwNginx._loadObj(uid)
        connectionData = Perf().getNginxConnectionPerfs(mw, timeUnit)
        
        connectionPerfs={"name":"连接数", "type":"spline", "data":connectionData}
        return [connectionPerfs]
#--------------------------------------------------------------------------------------------------------------
    def listApaches(self):
        conditions={}
        UserControl.addCtrlCondition(conditions)
        mws = MwApache._findObjects(conditions=conditions)
        return mws
    
    @apiAccessSettings("add")
    def addApache(self, host, port="80", title="", collector="", ssl=False, httpUsername="", httpPassword=""):
        return self.__addMiddleware(MwApache, host, port, title, collector, ssl, httpUsername, httpPassword)
    
    @apiAccessSettings("edit")
    def editApache(self, moUid, port="80", title="", ssl=False, httpUsername="", httpPassword=""):
        mw = MwApache._loadObj(moUid)
        if not mw:return "warn:编辑失败"
        mw.port = port
        mw.title = title
        mw.ssl = ssl
        mw.httpUsername = httpUsername
        if  httpPassword: mw.httpPassword = httpPassword
        
        return "编辑成功"
    
    @apiAccessSettings("del")
    def removeApache(self,uid):
        mw = MwApache._loadObj(uid)
        if not mw: return "warn:删除失败，服务器已经不存在"
        mw.remove()
        return "删除成功"
        
    def getApacheConnPerfs(self, uid, timeUnit="day"):
        mw = MwApache._loadObj(uid)
        connectionData = Perf().getApacheConnectionPerfs(mw, timeUnit)
        
        connectionPerfs={"name":"连接数", "type":"spline", "data":connectionData}
        return [connectionPerfs]
    
#--------------------------------------------------------------------------------------------------------------
    def listTomcats(self):
        conditions={}
        UserControl.addCtrlCondition(conditions)
        mws = MwTomcat._findObjects(conditions=conditions)
        return mws
    
    @apiAccessSettings("add")
    def addTomcat(self, host, port="80", title="", collector="", ssl=False, httpUsername="", httpPassword=""):
        return self.__addMiddleware(MwTomcat, host, port, title, collector, ssl, httpUsername, httpPassword)
    
    @apiAccessSettings("edit")
    def editTomcat(self, moUid, port="80", title="", ssl=False, httpUsername="", httpPassword=""):
        mw = MwTomcat._loadObj(moUid)
        if not mw:return "warn:编辑失败"
        mw.port = port
        mw.title = title
        mw.ssl = ssl
        mw.httpUsername = httpUsername
        if  httpPassword: mw.httpPassword = httpPassword
        
        return "编辑成功"
    
    @apiAccessSettings("del")
    def removeTomcat(self,uid):
        mw = MwTomcat._loadObj(uid)
        if not mw: return "warn:删除失败，服务器已经不存在"
        mw.remove()
        return "删除成功"
        
    def getTomcatConnPerfs(self, uid, timeUnit="day"):
        mw = MwTomcat._loadObj(uid)
        connectionData = Perf().getTomcatConnectionPerfs(mw, timeUnit)
        
        connectionPerfs={"name":"连接数", "type":"spline", "data":connectionData}
        return [connectionPerfs]


        