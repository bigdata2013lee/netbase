#coding=utf-8
import time
import logging
log = logging.getLogger('django.request')
from products.netModel.company import Company
from products.netWebAPI.base import BaseApi
from products.netModel.user.user import User
from products.netUtils import jsonUtils
from products.netPublicModel.userControl import UserControl
from products.netBilling.Billing import Billing
from products.netModel.baseModel import RefDocObject
from products.netUtils import xutils
from products.netModel.device import Device
from products.netModel.website import Website
from products.netModel.network import Network
from products.netModel.shortcutCmd import ShortcutCmd
from products.netModel.bootpo import Bootpo
from products.netPublicModel.emailTemplates import user_add_billing_success_mail_html
import time


class BillingApi(BaseApi):
  
  
    def getUnitPrices(self):
        "单价表"
        prices = dict(
            Device = 20,
            Website = 10,
            Bootpo = 50,
            ShortcutCmd = 5,
            Network = 20,
          )
        
        return prices
    
    def _getTotalPrice(self, counts={},months=1):
        unitPrices = self.getUnitPrices()
        total = 0
        for name in unitPrices.keys():
            total += unitPrices.get(name,0) * counts.get(name,0)
        return total * months
    
    def _getStartTimeEndTime(self,months):
        "计算开始时间，结束时间"
        aDay = 86400
        now  = time.time()
        startTime = int(now/aDay)*aDay-28800 #当天00:00
        endTime = startTime + 30 * aDay * months #截止某天24点，即下一天的00:00
        return startTime, endTime
    
    def _formatTimeStamp(self, ts):
        return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(ts))

    def __sendSuccessAddBillingMail(self, user, billing):
        subject = "Netbase 用户购买认购单通知"
        stamp = time.time()
        message = user_add_billing_success_mail_html % {
             "user":user.username,
             "_id": billing.getUid(),
             "startTime": self._formatTimeStamp(time.time()),
             "endTime": self._formatTimeStamp(billing.endTime),
             "totalPrice": billing.totalPrice,
             "Device": billing.counts.get("Device", 0),
             "Website": billing.counts.get("Website", 0),
             "Network": billing.counts.get("Network", 0),
             "Bootpo": billing.counts.get("Bootpo", 0),
             "ShortcutCmd": billing.counts.get("ShortcutCmd", 0)      
        }
        
        xutils.sendMail(subject=subject, message=message, recipient_list=[user.email])
        
    def addBilling(self, counts={}, months=3):
        """
            
        """
        user = UserControl.getUser()
        ownCompany = user.ownCompany
        if not ownCompany: return "warn:购买失败！"
            
        SET = self._getStartTimeEndTime(months)
        
        totalPrice = self._getTotalPrice(counts,months)
        if user.money < totalPrice:
            return "warn:购买失败, 您的帐户余额不足，请及时充值!"
        
        billing = Billing()
        billing.startTime = SET[0]
        billing.endTime = SET[1]
        billing.counts = counts
        billing.totalPrice = self._getTotalPrice(counts,months)
        
        billing.isvalid = True
        billing.ownCompany = ownCompany
        billing._saveObj()
        
        user.money-=totalPrice
        try:
            self.__sendSuccessAddBillingMail(user, billing)
        except Exception, e:
            msg = "无法发送认购单到你的邮箱，可能您的邮箱不存在"
            log.warn("邮件发送失败")
            print e
            log.exception(e)
            return msg

        
        
        return "认购成功！本次购买金额%s元, 截止有效期%s" %(billing.totalPrice, xutils.formartTime(billing.endTime-1))
    
    
    @classmethod
    def countItemOnDay(cls, ts=None, itemType=None):
        """
        计算某时间点(某天内的任意一时间点)，可以添加项目最大个数
        @param ts: 时间点， ts=None, 则ts=now
        @itemType:itemType=None,求复合项目，itemType为特定项目名称时,求单个项目
        """
        if  not  ts: ts = time.time()
        conditions = {}
        UserControl.addCtrlCondition(conditions)
        conditions["endTime"] = {"$gt": time.time()}
        conditions["isvalid"] = True
        conditions["endTime"] = {"$gt": ts}
        conditions["startTime"] = {"$lte": ts}
        
        billings = Billing._findObjects(conditions=conditions)
        billings.append(Billing._loadObj("wanjee001"))
        
        totalCounts = {"Device":0, "Network":0, "Website":0, "Bootpo":0,"ShortcutCmd":0}
        if  itemType:
            totalCount = 0
            for bil in billings:
                totalCount +=bil.counts.get(itemType,0)
            
            return totalCount
                
        for bil in billings:
            for  name in  totalCounts.keys():
                totalCounts[name] +=bil.counts.get(name,0)
            
            
        return  totalCounts
            
    
    @classmethod
    def  isOverCount(cls, typeCls):
        "判断当前时间，当前用户的某类项目，是否到达最大数目限制" 
        conditions = {}
        UserControl.addCtrlCondition(conditions)
        usedCount= typeCls._countObjects(conditions=conditions)
        maxCount = cls.countItemOnDay(itemType = typeCls.__name__)
        return usedCount >= maxCount
        
    def getChartData(self, days=30):
        
        now = time.time()
        tsList=[]
        
        categories=[]
        series=[]
        
        for x  in range(days):
            ts = now + x * 86400
            tsList.append(ts)
            label = xutils.formartTime(ts, fm="%m/%d")
            categories.append(label)
            
        
        nameMap = dict(Device=[],Website=[],Network=[],Bootpo=[],ShortcutCmd=[])
        for ts in tsList:
            totalCounts = self.__class__.countItemOnDay(ts)
            for name in nameMap.keys():
                nameMap[name].append(totalCounts.get(name,0))
                
        for name in nameMap.keys():
            item = dict(name=name, data=nameMap.get(name,[]))
            series.append(item)
        
        return  dict(series=series, categories=categories)
         
            

        
    def listAvailableBillings(self, btype=""):
        """
        列出有效的、可用的购买单
        """
        user = UserControl.getUser()
        conditions = {}
        UserControl.addCtrlCondition(conditions)
        conditions["endTime"] = {"$gt": time.time()}
        conditions["type"]=btype
        conditions["isvalid"] = True
        
        billings = Billing._findObjects(conditions=conditions)
        billings = filter(lambda b: b.count > b.usedCount, billings)
        
        return jsonUtils.jsonDocList(billings)
        
    
    def  listBillings(self):
        
        conditions = {}
        UserControl.addCtrlCondition(conditions)
        conditions["endTime"] = {"$gt": time.time()}
        conditions["isvalid"] = True
        sortInfo = {"_id":-1}
        billings = Billing._findObjects(conditions=conditions,sortInfo=sortInfo)
        defaultBilling = Billing._loadObj("wanjee001")
        rs = []
        rs.append({"_id":"wanjee001", "totalPrice":0, "counts": defaultBilling.counts})
        rs.extend(jsonUtils.jsonDocList(billings))
        return rs
    
    
    def getCurrentSourcesUsedCounts(self):
        "计算当前资源使用情况"
        
        conditions = {}
        UserControl.addCtrlCondition(conditions)
        counts={}
        counts["Device"] = Device._countObjects(conditions=conditions)
        counts["Website"] = Website._countObjects(conditions=conditions)
        counts["Network"] = Network._countObjects(conditions=conditions)
        counts["Bootpo"] = Bootpo._countObjects(conditions=conditions)
        counts["ShortcutCmd"] = ShortcutCmd._countObjects(conditions=conditions)
        
        return counts
        
        
    def listBillingsByUser(self, userId):
        
        def updict(obj):
            return  {
                     "ownCompany": obj.ownCompany.titleOrUid() or ""
                    }
        
        user = User._loadObj(userId)
        if not user: return "warn:用户不存在！"
        ownCompany = user.ownCompany
        sortInfo = {"startTime":-1}
        rs = Billing._findObjects({"ownCompany":RefDocObject.getRefInfo(ownCompany)},sortInfo)
        rs.append(Billing._loadObj("wanjee001"))
        return jsonUtils.jsonDocList(rs, updict = updict)

    
    
    
  