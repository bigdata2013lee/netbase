#coding=utf-8
from products.netWebAPI.base import BaseApi
from products.netUtils import jsonUtils
from products.netModel.user.user import User 
from products.netModel.user.adminUser import AdminUser
from products.netModel.user.engineerUser import EngineerUser
from products.netModel.saleOpRecord import SaleOpRecord
from products.netModel.rechargeForm import RechargeForm
from products.netModel.user.user import User
import time
import types
import re
from products.netModel.user.saleUser import SaleUser

def _getLoginUser(api):
    return api.request.user


class SaleApi(BaseApi):
    
    #根据销售列出操作记录
    def listSaleOpRecords(self):
        sale = _getLoginUser(self)
        sors = sale.findOpRecords(sortInfo={"opTime":-1})
        def updict(obj):
            sale = obj.sale._medata.get("_id")
            return {"sale": sale, "opTime": time.strftime( "%Y-%m-%d %H:%M:%S",time.localtime(obj.opTime)) }
        return jsonUtils.jsonDocList(sors, updict = updict)
        
    #记录操作记录
    def recordOp(self, opType, opDesc=""):
        sale = _getLoginUser(self)
        sor = SaleOpRecord()
        sor.sale = sale
        sor.opTime = time.time()
        sor.operation = opType
        sor.opDetail = opDesc
        sor._saveObj()
  
    def _updateUserEngineer(self, customer, engId, etype):
        if not customer: return "fail"
        eng = EngineerUser._loadObj(engId)
        oldEngineer = getattr(customer, etype, None)
        setattr(customer, etype, eng)
        customer._saveObj()
        
        if oldEngineer and not eng: #删除工程师
            self.recordOp(u"删除客户工程师", u"删除客户(%s)工程师  工程师类型：%s: UID: %s" %(customer.getUid(), etype, oldEngineer))
             
        elif oldEngineer and eng and oldEngineer != eng:
            self.recordOp(u"修改客户工程师", u"更改客户(%s)工程师  工程师类型：%s ：从 %s -> %s"  
                          %(customer.getUid(), etype, oldEngineer.getUid(), eng.getUid()))
        elif not oldEngineer and eng:
            self.recordOp(u"添加客户工程师", u"添加客户(%s)工程师  工程师类型：%s ：UID:%s" 
                           %(customer.getUid(), etype , eng.getUid()))
        return "ok"
        

    def setCustomerEngineer(self, customerUid, engineerUid):
            customer = User._loadObj(customerUid)
            eng = EngineerUser._loadObj(engineerUid)
            if  not  customer or  not eng:
                return "warn: 修改用户技术工程师失败"
            
            
            customer.engineer = eng
            return "成功保存修改用户技术工程师"
    

        
    def getUsers(self, conditions={}):
        """ 
        """
        sale = _getLoginUser(self)
        users =sale._getRefMeObjects("saleUser",User, {})
        def updict(obj):   
            company = obj.ownCompany
            provider = obj.idcProvider
            engineer = obj.engineer
            return {
                    "ownCompany": company and company.titleOrUid(), 
                    "idcUser": provider and provider.titleOrUid(),
                    "idcProviderId":provider and provider.getUid(),
                    "engineer": engineer and engineer.titleOrUid(),
                    }
        rs =  jsonUtils.jsonDocList(users, updict = updict, ignoreProperyties=["password", "last_login"])
        searchCompany = conditions.get("ownCompany","").strip()
        if searchCompany:
            rs = filter(lambda x: x.get("ownCompany","").find(searchCompany)>=0, rs)
        return rs
    
    
    def rechargeForCustomer(self, customerUid, rechargeMoney, rechargeInstructions=None):
        """
        销售为用户提交充值单
        @param customerUid: 
        """
        customer = User._loadObj(customerUid)
        if not customer: return "提交充值单失败，用户不存在！"
        rf = RechargeForm()
        rf.customer = customer
        rf.saleUser = _getLoginUser(self)
        rf.submitTime = time.time()
        rf.money = int(rechargeMoney)
        rf.rechargeInstructions = rechargeInstructions
        adminUser = AdminUser._findObjects()[0]
        rf.adminUser = adminUser.titleOrUid()
        rf._saveObj()
        self.recordOp("提交充值单", "为客户(%s) 提交充值%s￥" %(customer.getUid(), int(rechargeMoney)))
        return "提交充值单成功！"  
    


    
    
    def getAllRechargeForm(self,conditions={}, sortInfo=None, skip=0, limit=None):
        
        sortInfo = {"submitTime":-1}
        
        def updict(obj):
            saleUser = str(obj.saleUser._medata.get("_id"))
            customer = obj.customer.username
            email = obj.customer._medata.get("email")
            contactPhone = obj.customer._medata.get("contactPhone")
            return  {"email": email, "contactPhone":contactPhone,  "saleUser": saleUser, "customer": customer, 
                     "ownCompany": obj.customer.ownCompany.titleOrUid()}

        
        rs = []
        saleUser = _getLoginUser(self)
        from products.netModel.baseModel import RefDocObject
        _conditions = {}
        _conditions["saleUser"] =  RefDocObject.getRefInfo(saleUser)
        if conditions.has_key("status") and int(conditions["status"]) !=3  :
            _conditions["status"] = int(conditions["status"])
        users = RechargeForm._findObjects(_conditions, sortInfo, skip, limit)
        rsbefore = User.filterUsersByUserCompanyAndUserName(conditions, users)
        if not rsbefore:return[]
        if not conditions.get("_id", ""): 
            rs = rsbefore
            return jsonUtils.jsonDocList(rs, updict = updict)
        for rf in rsbefore:
            uid = rf.getUid()
            if uid.find(conditions["_id"]) !=-1:
                rs.append(rf)        
                
        return jsonUtils.jsonDocList(rs, updict = updict)
    
         
    
