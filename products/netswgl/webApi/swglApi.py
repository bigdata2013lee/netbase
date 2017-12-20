#coding=utf-8
from products.netWebAPI.base import BaseApi
from products.netUtils import jsonUtils
from products.netswgl.model.sEngineer import SEngineer
import re
from products.netPublicModel.userControl import UserControl
from products.netswgl.model.feedback import SEngineerFeedback, SEngineerReport
import time
from products.netUtils import xutils
from products.netswgl.model.sengineerFavorit import SEngineerFavorit
from products.netswgl.model.category import CpcAddr, Domain


ignoreProperyties1 = ["pljl","personalID"]

class SwglApi(BaseApi):
    
    
    def searchSEngineers(self, d0="", d1="", r0="", r1="", keywords="", sortField="goodRate", sortDir=-1, skip=0, limit=20):
        """
        搜索专家
        """
        sortInfo={sortField:sortDir}
        conditions={}
        if d1:
            conditions.update({"domain.d1":d1})
        elif d0:
            conditions.update({"domain.d0":d0})
            
        if r1:
            conditions.update({"cpcAddr.r1":r1})
        elif r0:
            conditions.update({"cpcAddr.r0":r0})
            
        if keywords:
            keywordsRegex = re.compile(r"%s" %keywords, re.IGNORECASE)
            conditions.update({"goodKillsAt": keywordsRegex})

        engineers = SEngineer._findObjects(conditions, sortInfo, skip=skip, limit=limit)
        count = SEngineer._getDbTable().find(conditions).count()
        def updict(doc):
            obj={"ownServiceProvider":{}}
            osp =   doc.ownServiceProvider
            obj["uid"] = doc.getUid()
            if osp:
                obj["ownServiceProvider"]["_id"] = osp.getUid()
                obj["ownServiceProvider"]["title"] = osp.titleOrUid()
                
            return obj
                 
            
        ret = {"total":count, "results":jsonUtils.jsonDocList(engineers,updict=updict, ignoreProperyties=ignoreProperyties1)}
        return ret
        
        
    def viewSEngineer(self, uid):
                
        seng = SEngineer._loadObj(uid)
        
        return jsonUtils.jsonDoc(seng)
    
    
    def feedbackSEngineer(self, uid, selects=[], summary=""):
        """
        评论专家
        @param uid: 专家ID
        @param selects: 用户评论的各项好坏指标
        @param summary: 评论文字内容
        """
        
        seng = SEngineer._loadObj(uid)
        if not seng:return
        u = UserControl.getUser()
        sengFeedback = SEngineerFeedback()
        
        sengFeedback.fbTime = int(time.time())
        sengFeedback.sEngineer = seng
        sengFeedback.summary = summary
        sengFeedback.userID = u.getUid()
        sengFeedback.userLabelName = xutils.ellipsisText(u.username, 10)
        sengFeedback._saveObj()
        
        #更新各项评论指标次数
        pljl = seng.pljl
        for selectRateKey in selects:
            if not selectRateKey in pljl: continue
            pljl[selectRateKey]+=1
            
        #更新各项评论指标值
        seng.updateRates()
        
        return ""    
    
    
    
    
    def allowFeedbackSEngineer(self, uid):
        """
        判断是否能够评论某一专家
        @note: 要求两天内不能重复评论
        """
        limitTime=24*60*60 * 2 #2天 24*60*60 * 2
        seng = SEngineer._loadObj(uid)
        if not seng:return False
        
        u = UserControl.getUser()
        if not u: return False
        
        conditions={}
        conditions["userID"] = u.getUid()
        conditions["fbTime"] = {"$gte": int(time.time()) - limitTime}
        feedbacks = seng._getRefMeObjects("sEngineer", SEngineerFeedback, conditions=conditions, limit=1)
        if feedbacks: return False
        
        return True
    
    
    def allowReportSEngineer(self, uid):
        """
        判断是否能够举报某一专家
        @note: 要求两天内不能重复举报
        """
        limitTime=24*60*60 * 2 #2天 24*60*60 * 2
        seng = SEngineer._loadObj(uid)
        if not seng:return False
        
        u = UserControl.getUser()
        if not u: return False
        
        conditions={}
        conditions["userID"] = u.getUid()
        conditions["fbTime"] = {"$gte": int(time.time()) - limitTime}
        reports = seng._getRefMeObjects("sEngineer", SEngineerReport, conditions=conditions, limit=1)
        if reports: return False
        
        return True
    
    
        
    def reportSEngineer(self, uid, reason="1", summary=""):
        """
        举报专家
        @param uid: 专家ID
        @param reason: 举报类型、原因
        @param summary: 具体原因，补充说明
        """
        seng = SEngineer._loadObj(uid)
        if not seng:return
        u = UserControl.getUser()
        sengReport = SEngineerReport()
        
        sengReport.fbTime = int(time.time())
        sengReport.fbType = reason
        sengReport.sEngineer = seng
        sengReport.summary = summary
        sengReport.userID = u.getUid()
        sengReport.userLabelName = xutils.ellipsisText(u.username, 10)
        sengReport._saveObj()
        
        return ""    
        
            
    def  favortSEngineer(self, uid):
        """
        添加收藏
        @param uid: 专家ID
        """
        seng = SEngineer._loadObj(uid)
        if not seng:return "warn:无法收藏此专家"
        u = UserControl.getUser()
        
        sefUid = "%s_%s" %(u.getUid(), seng.getUid()) #收藏ID由 "用户ID_专家ID" 构建
        if SEngineerFavorit._loadObj(sefUid): return "此专家已被收藏"
        sengFavorit = SEngineerFavorit(sefUid)
        sengFavorit.sEngineer = seng
        sengFavorit.user = u
        sengFavorit.time = time.time()
        sengFavorit._saveObj()
        
        return "成功收藏"
        
    def favortes(self):
        "用户获取收藏列表"
        u = UserControl.getUser()
        sengs=[]
        favortes = u._getRefMeObjects("user", SEngineerFavorit, sortInfo={"time":-1}, limit=100)
        for  fav in favortes:
            seng = fav.sEngineer
            if not seng: continue
            sengs.append(seng)
        return sengs
    
    
    def removeFavort(self, uid):
        "删除收藏对象"
        fav = SEngineerFavorit._loadObj(uid)
        if not fav: return "warn:删除收藏失败"
        fav.remove()
        return "删除收藏成功"
        

    def getCpcR1s(self, r0):
        "获取二级地域"
        conditions={"pid":r0}
        cpcAddrs = CpcAddr._findObjects(conditions=conditions)
        return jsonUtils.jsonDocList(cpcAddrs)
        
    def getDomain1s(self, d0):
        "获取二级领域"
        conditions={"pid":d0}
        domains = Domain._findObjects(conditions=conditions)
        return jsonUtils.jsonDocList(domains)        
        