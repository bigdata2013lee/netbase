#coding=utf-8
from products.netModel.monitorObj import MonitorObj
from products.netModel.baseModel import RefDocObject
from products.netUtils.cycleSettings import cycleTimes
from products.netModel import medata
import types
from products.netModel.collectPoint import CollectPoint
from products.netUtils.xutils import nbPath as _p
import time

class Website(MonitorObj):
    dbCollection = 'Website'
    
    def __init__(self, uid=None):
        MonitorObj.__init__(self)
        self._medata.update(dict(
            webSiteClass = None, #站点org
            collectPoints=[],#收集点
            commConfig=dict(
                        netCommandCommandTimeout=15
                ), 
        ))
    
    hostName = medata.plain("hostName") #域名
    ipAddress = medata.IPproperty("ipAddress")
    port = medata.plain("port", 80)
    timeout = medata.plain("timeout", 10)
    useSsl = medata.plain("useSsl", False)
    regex = medata.plain("regex", "")
    caseSensitive = medata.plain("caseSensitive", False)
    invert = medata.plain("invert", False)
    onRedirect = medata.plain("onRedirect", "")    
    url = medata.plain("url", "/")    
    httpUsername = medata.plain("httpUsername", "")
    httpPassword = medata.plain("httpPassword", "")
     
    @property
    def commConfig(self):
        "commConfig"
        return self._medata['commConfig']
    
    @commConfig.setter
    def commConfig(self, conf):
        """
        常规配置项目
        """
        self._medata.get("commConfig").update(conf)
        self._saveProperty('commConfig')
        
    @property
    def webSiteClass(self):
        "get webSiteClass"
        return RefDocObject.getInstance(self._medata['webSiteClass'])
    
    @webSiteClass.setter
    def webSiteClass(self, webSiteClass):
        "set webSiteClass"
        self._saveDocProperty(webSiteClass, 'webSiteClass')
        
        
    @property
    def collectPoints(self):
        "get collectPoints"
        collectPoints=RefDocObject.instRefList(self._medata["collectPoints"])
        return collectPoints
    
    def bindCollectPoint(self, cpt):
        """
            添加一个收集点
        """
        if not cpt: return self
        if cpt._getRefInfo in self._medata['collectPoints']: return self
        self._medata['collectPoints'].append(cpt._getRefInfo())
        self._saveProperty2('collectPoints', list(set(self._medata['collectPoints'])))
        return self

    
    def unbindCollectPoint(self, cpt):
        """
            删除一个收集点
        """
        if not cpt: return self
        if type(cpt) in types.StringTypes:
            cptName = cpt 
            cpt = CollectPoint._loadObj(cptName)
            if not cpt: return self
        
        cptRefInfo = cpt._getRefInfo() 
        if cptRefInfo in self._medata['collectPoints']: self._medata['collectPoints'].remove(cptRefInfo)
        self._saveProperty('collectPoints')
        return self
    
    def getManageId(self):
        """
        获取站点对象的管理Id
        """
        webSiteId=[]
        if self.hostName:
            webSiteId.append(self.hostName)
        else:
            webSiteId.append(self.ipAddress or "")
        if self.port and self.port!=80:webSiteId.append(":%s"%self.port)
        if self.url and self.url!="/":webSiteId.append(self.url)
        return "".join(webSiteId)
    
    def  getStatus(self):
        """
        获取当前站点的状态
        @note: 存在up，认为正常，否则，存在down认为异常，否则认为未知
        """
        collectPoints = self.collectPoints
        sts = [self.getCptStatus(cpt) for cpt in collectPoints]
        if "up" in sts: return "up"
        if "down" in sts: return "down"
        return "unknown"
    
    def getCptStatus(self,cpt):
        """
         得到站点的收集点状态
        """
        if  not cpt: return "unknown"
        val = self._getCptEventStatusValue(cpt)
        status = {1:"up", 0: "down"}
        return status.get(val, "unknown")
    
    def getCptsStatusSummary(self):
        """
        收集点状态摘要
        @return: {up:number, down:number, unknown:number}
        """
        rs = {"up":0, "down":0, "unknown":0}
        collectPoints = self.collectPoints
        for cpt in collectPoints:
            cptSt = self.getCptStatus(cpt)
            rs[cptSt]+=1
            
        return rs
    
    def getReponseTime(self):
        """
        获取当前响应时间
        @note: 结果是所有的收集点的当前响应时间之平均
        """
        collectPoints = self.collectPoints
        responseTimes = []
        for cpt in   collectPoints:
            responseTime = self.getCptCurrentResponseTime(cpt)
            if responseTime is not None: responseTimes.append(responseTime)
        if not responseTimes: return None
        return sum(responseTimes)/len(responseTimes)
    
    def getAvailabilityRatio(self):
        """
        获取站点可用性/近一小时
        @note: 结果是所有的收集点的可用性之平均
        """
        collectPoints = self.collectPoints
        ratios = []
        for cpt in   collectPoints:
            ratio = self.getCptAvailabilityRatio(cpt)
            if ratio is not None: ratios.append(ratio)
        if not ratios: return 0
        rs = sum(ratios)/len(ratios)
        return rs
    
    def _getCptEventStatusValue(self,cpt,NoneVal=-1):
        """
        获取收集点事件状态值
        @note: 容差时间 默认3周期时间 具体配置在products/netUtils/cycleSettings.py
        """
        from products.netPerData import manager as perDataManager
        dbName = self._getPerfDbName()
        tableName = self._getStatusTableName(cptUid = cpt.getUid())
        timeRange = cycleTimes.get(self.getComponentType(), 180) * 3; #默认3周期时间 
        return perDataManager.getEventStatusValue(dbName, tableName, timeRange=timeRange, NoneVal=NoneVal)
    
    

            
    def getCptCurrentResponseTime(self, cpt):
        """
        获取收集点当前响应时间
        @param cpt: 收集点
        """
        if not cpt: return None
        tpl=self.getBaseTemplate()
        val = self.getPerfValue(tpl.getUid(),  "http", "time", cptUid=cpt.getUid())
        if val is not None:
            val = int(val *1000)
        return val
    
    def getCptAvgResponseTime(self, cpt, timeRange=3600):
        "收集点1小时内的平均响应时间"
        if not cpt: return None
        tpl=self.getBaseTemplate()
        sTime = time.time() - timeRange
        vals = self.getPerfValues(tpl.getUid(),  "http", "time", sTime, eTime=None, cptUid=cpt.getUid())
        
        if not vals: return None
        x2list = filter(lambda x: x.get("val", None) is not None, vals)
                
        if not x2list: return None
        x3list = [x.get("val") for x  in x2list]

        rs = sum(x3list)/len(x3list)
        rs = int(rs*1000)
        return rs
    
    def getCptCurrentStatus(self, cpt):
        "获取收集点状态"
        if not cpt: return "unknown"
        val = self._getCptEventStatusValue(cpt)
        status = {1:"up", 0: "down"}
        return status.get(val, "unknown")
        
    def  getCptAvailabilityRatio(self, cpt):
        "获取收集点近一小时可用性"
        if not cpt: return 0
        from products.netPerData import manager as perDataManager
        now = time.time()
        statusVals = perDataManager.getCptEventStatusValues(self, cpt, now - 3600, endTime=now)
        upStatusVals = filter(lambda x: x.get("value", 0) == 1, statusVals)
        return len(upStatusVals)*100/(len(statusVals) or 1)
    
    def getCmd(self):
        """
        得到站点的命令
        """
        parts = [_p("/libexec/check_http")]
        if self.hostName:
            parts.append('-H %s' % self.hostName)
        if self.ipAddress:
            parts.append('-I %s' % self.ipAddress)
        if self.port:
            parts.append('-p %s' % self.port)
        if self.timeout:
            parts.append('-t %s' % self.timeout)
        if self.useSsl:
            parts.append('-S')
        if self.url:
            parts.append('-u %s' % self.url)
        if self.regex:
            if self.caseSensitive:
                parts.append('-r %s' % self.regex)
            else:
                parts.append('-R %s' % self.regex)
            if self.invert:
                parts.append('--invert-regex')
        if self.httpUsername or self.httpPassword:
            parts.append('-a %s:%s' % (self.httpUsername, self.httpPassword))
        if self.onRedirect:
            parts.append('-f %s' % self.onRedirect) 
        cmd = ' '.join(parts)
        return cmd
    
           
