#coding=utf-8
'''
time:2014-12-24
@version: netbase4.0
@author: julian
'''
import md5
import time
import random
import datetime
from products.netUtils import jsonUtils
from products.netBilling.Billing import Billing
from products.netUtils import xutils, validator
from products.netModel.user.user import User
from products.netWebAPI.base import BaseApi
from products.netModel.company import Company
from products.netBilling.levelPolicy import LevelPolicy
from products.netUtils.settings import ManagerSettings
from products.netBilling.extendDevice import ExtendDevice
from products.netModel.feedBackInfo import FeedBackInfo
from products.netModel.rechargeForm import RechargeForm
from products.netModel.org.webSiteClass import WebSiteClass
from products.netModel.operation.deviceDtail import DeviceDtail
from products.netModel.operation.operationer import Operationer
from products.netPublicModel.emailTemplates import user_sys_new_active_mail_html,confirm_extend_device_mail_html

settings = ManagerSettings.getSettings()


def  _sc2datetime(sn):
    if not sn: return None 
    ltime = time.localtime(sn)
    return datetime.datetime(ltime[0],ltime[1],ltime[2],ltime[3],ltime[4],ltime[5])
    
class AdminUserApi(BaseApi):
    '''
    time:2014-12-24
    @author: julian
    @todo: admin的API接口类
    '''    
    def getAllUsers(self, conditions={}):
        users = User._findObjects()
        objs = []
        _fillters = []
        
        if conditions.get("username",""):
            _fillters.append({"name":"username", "val":conditions.get("username","")})
            
        if conditions.get("company",""):
            _fillters.append({"name":"company", "val":conditions.get("company","")})
        
        def xfillter(user, ft):
            if ft["name"] == "username":
                v = user.username.find(ft['val'])
                if v == -1: return False
            
            if ft["name"] == "company":
                v = user.ownCompany.titleOrUid().find(ft['val'])
                if v == -1: return False
                
            return True

        if _fillters:
            for user in users:
                for ft in _fillters:
                    v = xfillter(user, ft)
                    if not v: break
                    if _fillters[-1] == ft: objs.append(user)
                    break
        else:
            objs = users
            
        def updict(u):
            lastLoginTime = u.last_login
            if lastLoginTime and type(lastLoginTime) == datetime.datetime:
                lastLoginTime=lastLoginTime.strftime('%Y-%m-%d %H:%M')
            else:
                lastLoginTime=""
                
            return {
                        "company": u.ownCompany and u.ownCompany.titleOrUid(),
                        "lastLoginTime":lastLoginTime
                    }
        rs = jsonUtils.jsonDocList(objs,updict=updict, ignoreProperyties=['password','ownCompany','idcProvider','levelPolicy','engineer','last_login'])
        return rs
    
    def getNotCheckedRechargeForm(self, conditions={}, sortInfo=None, skip=0, limit=None):
        sortInfo = {"submitTime":-1}
        conditions["status"] = 0
        rechargeForms = RechargeForm._findObjects(conditions, sortInfo, skip, limit)
        def updict(obj):
            userMoney = obj.customer.money
            saleUser = obj.saleUser._medata.get("_id")
            customer = obj.customer._medata.get("username")
            return  {"userMoney":userMoney, "saleUser": saleUser, "customer": customer, "company": obj.customer.ownCompany.titleOrUid()}
        return jsonUtils.jsonDocList(rechargeForms, updict = updict)
    
    def getAllRechargeForm(self,conditions={}, sortInfo=None, skip=0, limit=None):
        sortInfo = {"submitTime":-1}
        def updict(obj):
            saleUser = obj.saleUser._medata.get("_id")
            customer = obj.customer._medata.get("username")
            email = obj.customer._medata.get("email")
            contactPhone = obj.customer._medata.get("contactPhone")
            return  {"email": email, "contactPhone":contactPhone,  "saleUser": saleUser, "customer": customer, 
                     "ownCompany": obj.customer.ownCompany.titleOrUid()}

        rs = []
        _conditions = {}
        if conditions.has_key("status") and int(conditions["status"]) !=3 :
            _conditions["status"] = int(conditions["status"])
        rform = RechargeForm._findObjects(_conditions, sortInfo, skip, limit)
        rsbefore = User.filterUsersByUserCompanyAndUserName(conditions, rform)
        if not rsbefore:return []
        if not conditions.get("_id", ""): 
            rs = rsbefore
            return jsonUtils.jsonDocList(rs, updict = updict)
        for rf in rsbefore:
            uid = rf.getUid()
            if uid.find(conditions["_id"]) !=-1:
                rs.append(rf) 
        
        return jsonUtils.jsonDocList(rs, updict = updict)
    
    def changeRechargeFormStatus(self, uids, flag):
        for uid in uids:
            rf = RechargeForm._loadObj(uid)
            if not rf: return "warn:更改状态失败，没有对应的表单"
            if flag == 2:
                rf.status = 2
            else:
                try:
                    rs = self._remoteAddUserMoney(rf.customer.getUid(), rf.money)
                except:
                    return "rpyc没有启动， 充值失败！"
                if not rs:
                    return "充值失败"
                rf.status = 1
            
            rf.completeTime = time.time()
            rf._saveObj()
        return "更改状态成功"
    
    
    def _remoteAddUserMoney(self, uid, money=0):
        """
        充值方法
        """
        from products.rpcService.client import Client
        rpycHost = settings.get('rpycConnection', 'rpcHost')
        rpycPort = settings.getAsInt('rpycConnection', 'rpcPort')
        if rpycHost == "0.0.0.0":
            rpycHost = '127.0.0.1'
    
        rpcServiceClient = Client(rpycHost, rpycPort) #rpyc客户端
        dr = rpcServiceClient.getServiceObj().getDataRoot()
        flag = dr.addUserMoney(uid, money)  
        return flag
        
    
    def getOperationers(self,operationer=""):
        operationers = []
        if operationer:
            operationers = Operationer._findObjects({"originalName":operationer});
            return operationers
        operationers = Operationer._findObjects();
        return operationers
    
    
    def toIdcUser(self, userId):
        "转为IDC类型"
        u = User._loadObj(userId)
        if not u: return "warn:操作失败，用户不存在"
        u.billing=u.billing.idcFree
        u.status="Normal"
        u.group = "idc"
        u._saveObj()
        return "操作成功"

    def createAccounts(self, accountInfos=[]):
        """
        根据帐户信息列表，批量生成帐号
        """
        users = []
        for userInfo in accountInfos:
            username = User.getVaildSysUerName()
            pwd = "%06d" %random.randint(10000, 99999)
            
            u = User(username)
            u.group = "idc"
            u.password = pwd
            u.email = userInfo.get('email', '')
            u.contactPhone = userInfo.get('contactPhone', '')
            u.createTime = time.time()
            u._saveObj()
            u._saveProperty2("is_active", True)
            
            users.append(u)
            
            
            cpy = Company()
            cpy.title = userInfo.get("company",'')
            cpy._saveObj()
            u.ownCompany = cpy
            
            
            wsc = WebSiteClass(uname=WebSiteClass.rootUname,title="站点")
            wsc.ownCompany = u.ownCompany
            billing = Billing()
            billing=billing.idcFree
            billing._saveObj()
            wsc._saveObj()
            u.billing = billing
        
        for user in users:
            self.__sendNewAccountActiveMail(user)
            
        return users
        
    def __sendNewAccountActiveMail(self, user):
        """
        发送新帐号通知邮件
        """
        url = settings.get("mainServer", "hostUrl") #服务器端的主路径url
        subject = "Netbase 系统用户注册"
        message = user_sys_new_active_mail_html %{
             "url":"http://%s/" %url,
             "user":user.username,"pwd":user.password
        }
        
        xutils.sendMail(subject=subject, message=message, recipient_list=[user.email])
        
    def listFeedBackInfos(self, conditions={},skip=None,limit=None):
        sortInfo = {"infoTime":-1}
        _conditions = {}
        if conditions.has_key("feedBackContent"):
            _conditions["feedBackContent"] = { "$regex":conditions["feedBackContent"]}
        rs = FeedBackInfo._findObjects(_conditions, sortInfo=sortInfo,skip=skip,limit=limit)
        return rs
#        return jsonUtils.jsonDocList(rs)
   
        
    '''
                    获得查询条件
    ''' 
    def _getFilterConditions(self, loginTime1=None, loginTime2=None,registTime1=None,registTime2=None, username=""):   
        conditions={}   
        loginTime1 = _sc2datetime(loginTime1)
        loginTime2 = _sc2datetime(loginTime2)  
        if loginTime1 and loginTime2:
            conditions.update({"last_login":{"$gte":loginTime1, "$lt":loginTime2}})    
        elif loginTime1: 
            conditions.update({"last_login":{"$gte":loginTime1}})         
        elif loginTime2: 
            conditions.update({"last_login":{"$lt":loginTime2}})          
        if registTime1 and registTime2:
            conditions.update({"createTime":{"createTime":{"$gte":registTime1,"$lt":registTime2}}})       
        elif registTime1:
            conditions.update({"createTime":{"$gte":registTime1}}) 
        elif registTime2:
            conditions.update({"createTime":{"$lt":registTime2}})          
        if username: 
            username = username.strip()
            if username:
                conditions.update({"$where" : 'this.email.indexOf("'+username+'") >= 0' })  
        return conditions               

    '''
                    根据查询条件，测试符合条件的用户数目
    ''' 
    def testFilter(self,loginTime1=None, loginTime2=None,registTime1=None,registTime2=None, username=""):
        conditions = self._getFilterConditions(loginTime1=loginTime1, loginTime2=loginTime2,
                                  registTime1=registTime1,registTime2=registTime2, username=username)
        users = User._findObjects(conditions=conditions)
        return "共找到 %d 用户" % len(users)

    '''
                    根据查询条件，向符合条件的用户发送邮件
    '''
    def sendMailToUsersForFilter(self, emailContext, subject, loginTime1=None, loginTime2=None,
                                  registTime1=None,registTime2=None, username=""): 
        conditions = self._getFilterConditions(loginTime1=loginTime1, loginTime2=loginTime2,
                                  registTime1=registTime1,registTime2=registTime2, username=username)
        users = User._findObjects(conditions=conditions)
        emails=[]
        for u in users:
            emails.append(u.email)
        rs = self.sendMailToUsersForSpecified(emailContext,subject,emails=emails)   
        return rs
    
    '''
                    向指定的邮箱列表，依次发送邮件
    '''
    def sendMailToUsersForSpecified(self, emailContext,subject,emails=[]):
        for email in emails:
            try:
                xutils.sendMail(subject=subject, message=emailContext, recipient_list=[email])
            except Exception, e:
                print e        
        return "发送邮件完成"
    
    def addOperation(self,originalName,username,password,companyName,bussinessLicenseNum,phoneNum,
                     address,companydescription,email,technologyFileds=[],serviceAreas=[],technologyForte=""):
        '''
        time:2014-12-24
        @author: julian
        @todo: 添加运营商
        @param originalName: <String> 名字
        @param username: <String> 用户名
        @param password: <String> 密码
        @param companyName: <String> 公司名
        @param bussinessLicenseNum: <String> 商业license数量
        @param phoneNum: <String> 电话号码
        @param address: <String> 地址
        @param companydescription: <String> 公司描述
        @param email: <String> 邮箱
        @param technologyFileds: <list> 技术领域
        @param serviceAreas: <list> 服务领域
        @param technologyForte: <String> 擅长的技术
        @return: 添加成功与否的提示
        '''
        rules={
           "username":"email", "password":{"rule":"regex","regex":r"^\w{6,20}$"},"originalName":"required",
           "companyName":"required","bussinessLicenseNum":"required",
           "phoneNum":{"rule":"regex","regex":r"((\d{11})|^((\d{7,8})|(\d{4}|\d{3})-(\d{7,8})|(\d{4}|\d{3})-(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1})|(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1}))$)"},
           "address":"required","email":"email"
        }
    
        messages={
               "username":"帐号请使用一个正确的邮箱",
               "password":"密码请使用 数字、字母、下划线6~20个字符",
               "originalName":"姓名是必填项",
               "companyName":"公司名称不能为空",
               "bussinessLicenseNum":"营业执照编号不能为空",
               "phoneNum":"联系电话不能为空",
               "address":"地址不能为空",
               "email":"请使用一个正确的邮箱"
        }
        params=dict(username=username,password=password,originalName=originalName,companyName=companyName,email=email,
                    bussinessLicenseNum=bussinessLicenseNum,phoneNum=phoneNum,address=address,companydescription=companydescription,
                     technologyFileds=technologyFileds,technologyForte=technologyForte,serviceAreas=serviceAreas)
        vrs  = validator.Validator(rules=rules, messages=messages).v(params)
        if not vrs[0]:  return "warn:%s" %vrs[1]
        operationer = Operationer();
        levelPolicy=LevelPolicy()
        deviceDtail = DeviceDtail()
        levelPolicy._saveObj()
        deviceDtail._saveObj()
        operationer.levelPolicy=levelPolicy
        operationer.createTime=time.time()
        operationer.deviceDtail=deviceDtail             
        operationer.username = username
        operationer.email = email
        operationer.contactPhone = phoneNum
        operationer.password = md5.new(password).hexdigest()
        operationer.originalName = originalName
        operationer.baseInfo["companyName"] = companyName
        operationer.baseInfo["bussinessLicenseNum"] = bussinessLicenseNum
        operationer.baseInfo["address"] = address
        operationer.companydescription =companydescription
        operationer.serviceInfo["technologyFileds"] = technologyFileds
        operationer.serviceInfo["technologyForte"] = technologyForte
        operationer.serviceInfo["serviceAreas"] = serviceAreas
        operationer._saveProperty2("is_active", True)
        operationer._saveObj()
        return "运维商添加成功"
    
    
    def delOpertioner(self,opId):
        '''
        time:2014-12-24
        @author: julian
        @todo: 删除运营商
        @param opId: <String>运营商ID
        @return: 删除成功与否的提示
        '''
        operationer=Operationer._loadObj(opId)
        if not operationer:return "warn:该运营商不存在"
        Operationer.remove(operationer)
        return  "成功删除运营商%s" % operationer.username.split("@")[0]
      
    def extendDeviceAdmin(self,edId):
        '''
        time:2014-12-24
        @author: julian
        @todo: admin扩展设备
        @param edId: <String>设备扩展对象的ID
        @return: 设备添加成功与否的提示
        '''
        ed=ExtendDevice._loadObj(edId)
        user=ed.user
        host=ed.deviceCount
        website=ed.websiteCount
        network=ed.networkCount
        if host>0:user.levelPolicy.deviceCount+=host
        if website>0:user.levelPolicy.websiteCount+=website
        if network>0:user.levelPolicy.networkCount+=network
        user.levelPolicy.bootpoCount=user.levelPolicy.deviceCount+user.levelPolicy.networkCount
        ed.status=1
        try:
            self.extendDeviceMail(ed)
        except:
            return "扩展设备数成功"
        return "发送邮件成功，扩展设备数成功"
    
        
    def extendDeviceMail(self,ed):
        '''
        time:2014-12-24
        @author: julian
        @todo: 设备扩展发送通知邮件
        @param ed: <ExtendDevice>ExtendDevice对象
        '''
        subject = "设备扩充通知"
        firstSentence = "收到您的扩充设备信息如下："
        message = confirm_extend_device_mail_html %{
                   "deviceCount":ed.deviceCount,
                   "websiteCount":ed.websiteCount,
                   "networkCount":ed.networkCount,
                   "user":ed.user.username,   
                   "money":ed.money,
                   "firstSentence":firstSentence
                }
        xutils.sendMail(subject, message, recipient_list=[ed.user.username], attachments=[]) 
    
        
    def deleteExtendInfo(self,edId):
        '''
        time:2014-12-24
        @author: julian
        @todo: 删除设备扩展信息
        @param edId: <String> 设备扩展对象的ID
        @return: 删除成功与否的提示信息
        @note: 1.验证设备扩展对象的ID值是否取到，取到则去获取其对应的对象
                    2.验证设备扩展对象是否存在，存在则删除
        '''
        if not edId:return "warn:没有获得设备扩展对象的ID"
        extendDevice=ExtendDevice._loadObj(edId)
        if not extendDevice:return "warn:该设备扩展对象不存在"
        ExtendDevice.remove(extendDevice)
        return "删除成功"        
        
        
        
        
        
        
    








