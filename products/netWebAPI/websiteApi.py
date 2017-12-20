#coding=utf-8
from products.netModel.templates.template import Template

from products.netWebAPI.base import BaseApi, apiAccessSettings
from products.netPublicModel.modelManager import ModelManager as MM
from products.netUtils import jsonUtils
from products.netHome.webSiteHome import WebSiteHome
from products.netModel.org.webSiteClass import WebSiteClass
from products.netModel.website import Website
from products.netPublicModel.userControl import UserControl
from products.netModel.collector import Collector
from products.netEvent.monitorObjEvent import MonitorObjEvent
from products.netBilling.billingSys import BillingSys
from products.netUtils.mcClient import availabilityCacheDecorator
from products.netModel.collectPoint import CollectPoint
from products.netPerData.perDataMerger import PerDataMerger

def checkWebsiteManageIdExisted(manageId, website=None):
    """
    检查站点的manageId是否已经存在
    
    @param manageId: <string> 要检测的manageId
    @param website: <Website> 被忽略的站点
    @return: boolean
    
    @note: 业务要求同一用户不允许添加重复的站点
    """
    root = WebSiteClass.getRoot()
    websites = root.getAllMonitorObjs()
    for ws in websites:
        if website == ws: continue
        elif manageId == ws.getManageId(): return True
        
    return False    
            

class Perf(object):
    
    def getCptResponseTimePerfs(self, website, cpt, timeUnit):
        """
        获取站点response time 性能
        """
        coll = website.collector
        dbName = website._getPerfDbName()
        baseTpl = website.getBaseTemplate()
        if not baseTpl:
            print "warning: Can't find the base template on Website %s" %website.getUid()
            return []
        tableName = website._getPerfTablName(baseTpl.getUid(), "http", "time",cpt.getUid()) #
        
        datas = PerDataMerger().getPerfDataByTimeUnit(coll, dbName, tableName, website.createTime, timeUnit)
        for d in datas:
            if d[1] is not None: 
                d[1] = int(d[1]*1000)
            
        return datas
    
class WebsiteApi(BaseApi):
    
    def _getWebSite(self, uid):
        dr = MM.getMod("dataRoot")
        website = dr.findWebsiteByUid(uid)
        return website
    
    
    def getWebsiteClsRecentlyEvents(self, websiteClsUid=None):
        org = None
        if not websiteClsUid:
            org =  WebSiteClass.getRoot()
        else:
            org =  WebSiteClass._loadObj(websiteClsUid)
            
        if not org: return []
        conditions = {"severity":{"$gte":3}}
        evts = org.events(conditions=conditions, limit=10)
        igs = ["collectPointUid", "agent", "companyUid", "historical","moUid","evtKeyId", "clearId",
               "eventClass", "clearKey", "eventState", "collector"]
        return jsonUtils.jsonDocList(evts, ignoreProperyties=igs)
    
    
    def responseTimeTopN(self, n=5):
        conditions={}
        UserControl.addCtrlCondition(conditions)
        objs = Website._findObjects(conditions=conditions)
        xxList = []
        for  ws in objs:
            rt = ws.getReponseTime()
            if not rt: continue
            xxList.append(dict(title=ws.titleOrUid(), responseTime=rt)) 
            
        xxList.sort(key=lambda x: x.get("responseTime", 0), reverse=True)
        xxList=xxList[:n]
        
        series=[
                {"data":[x.get("responseTime", 0) for x in xxList]},
        ]
        
        categories=[x.get("title", "") for x in xxList]
        return dict(series=series,categories=categories)
    
    def getCptsResponseTimePerfs(self, websiteUid, timeUnit="day"):
        """
        获取站点所有收集点的响应时间性能数据
        """
        ws = Website._loadObj(websiteUid)
        if not ws: return []
        rs = []
        for cpt in ws.collectPoints:
            if not cpt: continue
            perfs = {"name":cpt.titleOrUid(), "type":"spline", "data":Perf().getCptResponseTimePerfs(ws, cpt, timeUnit)}
            rs.append(perfs)
        
        return rs
    
    def  listCptsInfos(self, websiteUid):
        ws = Website._loadObj(websiteUid)
        if not ws: return []
        rs = []
        for cpt in ws.collectPoints:
            if not cpt: continue
            cptInfo = {
                       "title":cpt.titleOrUid, 
                       "ss":cpt.ss,
                       "currentResponseTime": ws.getCptCurrentResponseTime(cpt),
                       "avgResponseTime": ws.getCptAvgResponseTime(cpt),
                       "availability":ws.getCptAvailabilityRatio(cpt),
            }
            
            rs.append(cptInfo)
            
        return rs
    
    @availabilityCacheDecorator
    def listAvailability(self, websiteClsUid, timeRange=3600):
        if not websiteClsUid:return "warn:无法获得站点ID，请添加站点"
        websiteCls =  WebSiteClass._loadObj(websiteClsUid)
        if not websiteCls:return "warn:该站点不存在" 
        webSiteHome  = WebSiteHome(websiteCls)
        rs = webSiteHome.getWebSiteStatusAvailability()
        #rs = testData.testData1
        return rs
        

    @availabilityCacheDecorator
    def getAvailabilityData(self, websiteClsUid, timeRange=3600):
        if not websiteClsUid:return "warn:无法获得站点ID，请添加站点"
        websiteCls =  WebSiteClass._loadObj(websiteClsUid) 
        if not websiteCls:return "warn:该站点不存在"  
        webSiteHome  = WebSiteHome(websiteCls)
        rs = webSiteHome.getAvailabilitysTops(timeRange=timeRange)
        series = []  
        for key, value in rs["rs"].items():
            series.append(dict(name=key, data=value))
            
        return dict(series=series, categories=rs["strTime"])
        
    @availabilityCacheDecorator
    def getResponesTimeTopsData(self, websiteClsUid, timeRange=3600):
        if not websiteClsUid:return "warn:无法获得站点ID，请添加站点" 
        websiteCls =  WebSiteClass._loadObj(websiteClsUid)
        if not websiteCls:return "warn:该站点不存在"
        webSiteHome  = WebSiteHome(websiteCls)
        rs = webSiteHome.getResponesTimeTops(timeRange=timeRange)
        series = []
        for key, value in rs["rs"].items():
            series.append(dict(name=key, data=value))
        return dict(series=series, categories=rs["strTime"])
    
    def listWebSiteReponseTime(self, websiteClsUid, timeRange=3600):
        if not websiteClsUid:return "warn:无法获得站点ID，请添加站点"
        websiteCls =  WebSiteClass._loadObj(websiteClsUid)
        if not websiteCls:return "warn:该站点不存在" 
        webSiteHome  = WebSiteHome(websiteCls)
        rs = webSiteHome.getWebSiteReponseTime(timeRange=timeRange)
        #rs = testData.testData2
        return rs
        
    def webSiteDistributionData(self,websiteClsUid,timeRange=3600):
        if not websiteClsUid:return "warn:无法获得站点ID，请添加站点"
        websiteCls =  WebSiteClass._loadObj(websiteClsUid)
        if not websiteCls:return "warn:该站点不存在" 
        webSiteHome  = WebSiteHome(websiteCls)
        rs = webSiteHome.getWebSiteDistribution(limit=5, timeRange=timeRange)
        return rs
        
        
    def getFavoritesData(self, websiteClsUid, timeRange=1):
        return []    
        
        
    ################################################################
    
    
    
    @apiAccessSettings("add")
    def addWebsiteClass(self, uname, title=""):
        rootWebsiteCls =  WebSiteClass.getRoot()
        if not rootWebsiteCls: 
            print "Can't find the website class root node."
            return "warn:操作失败,无法找到分类根节点"
        
        websiteCls= WebSiteClass(uname=uname, title=title)
        websiteCls._saveObj()
        rootWebsiteCls.addChild(websiteCls)
        return "添加站点分类成功"
        
    def delWebsiteClass(self, clsId):
        rootWebsiteCls =  WebSiteClass.getRoot()
        websiteCls = WebSiteClass._loadObj(clsId)
        if not rootWebsiteCls: 
            print "Can't find the website class root node."
            return "fail"
        
        if not websiteCls: return "warn:操作失败"
        objs = websiteCls.getAllMonitorObjs()
        
        for website in objs:
            website.webSiteClass = rootWebsiteCls
        
        websiteCls.remove();
        return "成功删除站点分类"
    
    @apiAccessSettings("edit")
    def renameWebsiteClass(self, clsId, title=""):
        websiteCls = WebSiteClass._loadObj(clsId)
        if not websiteCls: return "warn:操作失败"
        websiteCls.title=title
        return "成功重命名站点"
        
        
    def listWebsites(self):
        conditions={}
        UserControl.addCtrlCondition(conditions)
        objs = Website._findObjects(conditions=conditions)
        return objs
    
    @apiAccessSettings("add")
    def addWebsite(self, medata):
        user = UserControl.getUser()
        if BillingSys.hasEnoughPolicyForAdd(Website):
            return "warn:你的站点监控项目权限不足，请购买服务后再试."
        
        websiteCls = WebSiteClass.getRoot()
        ownCompany = user.ownCompany
        coll = Collector.getFreeCollector(Website.getComponentType())
        if not coll: return "warn:暂未分配到空间收集器，请稍后再试"
        if not websiteCls: return "warn:站点分类不存在，添加失败"
            
        website = Website()
        website.title = medata.get("title","")
        website.hostName = medata.get("hostName","")
        website.port = medata.get("port",80)
        website.url = medata.get("url","/")
        website.useSsl = medata.get("useSsl",False)
        website.httpUsername = medata.get("httpUsername","")
        website.httpPassword = medata.get("httpPassword","")
        
        
        newManageId = website.getManageId()
        checked = checkWebsiteManageIdExisted(newManageId)
        if checked: return "warn:无法保存站点，相同的站点已经存在，请检查站点的域名或ip!"
        
        website.webSiteClass = websiteCls
        website.ownCompany=ownCompany
        tpl = Template._loadObj("BaseTpl_CmdWebSite")
        website._saveObj()
        website.collector = coll
        website.bindTemplate(tpl)
        
        #绑定收集点
        for cptUid in medata.get("cptUids",[]):
            cpt = CollectPoint._loadObj(cptUid)
            if  not cpt: continue
            website.bindCollectPoint(cpt)
        
        dr = MM.getMod('dataRoot')
        dr.fireEvent("add_new_website", website=website)
        return "成功添加站点.  "
    
    
    @apiAccessSettings("edit")
    def editWebsite(self, medata):
            
        website = Website._loadObj(medata.get("wsUid",""))
        if not website: return "warn:编辑站点监控配置失败,站点对象已经不存在"
        website.title = medata.get("title","")
        website.port = medata.get("port",80)
        website.url = medata.get("url","/")
        website.useSsl = medata.get("useSsl",False)
        website.httpUsername = medata.get("httpUsername","")
        if  medata.get("httpPassword",""):
            website.httpPassword = medata.get("httpPassword","")
        
        
       
        website._medata['collectPoints']=[]
        website._saveObj()
        
        #绑定收集点
        for cptUid in medata.get("cptUids",[]):
            cpt = CollectPoint._loadObj(cptUid)
            if  not cpt: continue
            website.bindCollectPoint(cpt)
        
        return "成功编辑站点监控配置"
    
    @apiAccessSettings("del")
    def delWebsite(self, uid):
        website = Website._loadObj(uid)
        if not website: return "fail"
        website.remove()
        return "成功删除站点"
    
    
    def getWebsite(self, uid):
        website = Website._loadObj(uid)
        if not website: return None
        
        return jsonUtils.jsonDoc(website, ignoreProperyties=["collector", "commConfig", "templates", "webSiteClass", "ownCompany"])
    
        
    def getSummaryInfo(self):
        scores = 0 #总分
        root = WebSiteClass.getRoot()
        mos = root.getAllMonitorObjs()
        normalMosCount = 0 #正常站点数
        issueMosCount = 0 #问题站点数
        unknownMosCount = 0 #未知站点数
        allMosCount = len(mos) #站点总数
        
        moe = MonitorObjEvent()
        for mo in mos:
            s = moe.monitorObjScore(mo)
            scores += s or 0
            if s is None: unknownMosCount+=1
            elif s >= 100: normalMosCount+=1
            elif s < 100: issueMosCount+=1
        return dict(allMosCount=allMosCount, normalMosCount=normalMosCount, \
                    issueMosCount=issueMosCount, unknownMosCount=unknownMosCount, scores=scores)
        