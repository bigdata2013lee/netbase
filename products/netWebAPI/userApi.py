#coding=utf-8
from products.netModel.company import Company
from products.netWebAPI.base import BaseApi, apiAccessSettings
from products.netModel.user.user import User
import time
import hashlib
from products.netUtils import xutils
from products.netUtils import jsonUtils
from products.netAlarm.alarmRule import AlarmRule
from products.netPublicModel.modelManager import ModelManager as MM
from products.netPublicModel.userControl import UserControl
from products.netModel.collector import Collector
from products.netPublicModel.collectorClient import ColloectorCallClient
from products.netPublicModel.emailTemplates import user_active_mail_html
from products.netUtils.xutils import nbPath as _p
import logging
from products.netBilling.levelPolicy import LevelPolicy
from products.netModel.org.location import Location
log = logging.getLogger('django.request')

from products.netUtils.settings import ManagerSettings
settings = ManagerSettings.getSettings()

class UserApi(BaseApi):
    
    def activeUser(self, hash_userName):
        if not hash_userName: return ''
        userObjs = User._findObjects({'is_active': False})
        for u in userObjs:
            username = u.username
            if hash_userName == hashlib.md5(username).hexdigest():
                u._saveProperty2("is_active", True)
                return "ok"
            
        return "fail"
    
    def validatePassword(self, pwd):
        pwd = pwd.strip()
        if not pwd: return False
        user = UserControl.getUser()
        if not user: return False
        
        if user.password == pwd: return True
        return False
        
    def __sendActiveMail(self, user):
        active_url = settings.get("mainServer", "hostUrl") #服务器端的主路径url
        hash_userName = hashlib.md5(user.username).hexdigest()
        subject = "Netbase 系统用户注册激活"
        stamp = time.time()
        message = user_active_mail_html % {
             "url":"%s/accounts/active/%s/?stamp=%s" % (active_url, hash_userName, stamp),
             "user":user.username
        }
        
        xutils.sendMail(subject=subject, message=message, recipient_list=[user.email])
        
    def userActive(self,user):
        """
                用户激活
        """
        try:
            self.__sendActiveMail(user)
        except Exception, e:
            msg = "无法发送激活邮件到您注册的邮箱，可能您的邮箱不存在"
            log.warn("邮件发送失败")
            log.exception(e)
            return msg
        
        
    def registerUser(self, userInfo):
        """
                用户注册
        """
        password = userInfo.get('password', '')
        if not (password and password == userInfo.get('confirmPassword', '')):
            return  "密码不一致"
        user = User()
        user.password = password
        user.email = userInfo.get('email', '')
        user.username = userInfo.get('email', '')
        user.contactPhone = userInfo.get("phoneNum", "")
        user.createTime = time.time()
        
        #绑定公司
        cpy = Company()
        cpy.title = userInfo.get('email', '').split("@")[0]
        cpy._saveObj()
        user.ownCompany = cpy
        
        loc = Location()
        loc.title = "默认分组"
        loc.locType = "default"
        loc.ownCompany = cpy
        loc._saveObj()
            
        #绑定用户级别策略
#        lp = LevelPolicy._loadObj("free")
        lp = LevelPolicy()
        lp._saveObj()
        user.levelPolicy = lp
        user.levelPolicyEndTime = "0"
        
        #发送激活邮件
        msg=self.userActive(user)
        if msg is not None:return msg
        
        user._saveObj()
        dr = MM.getMod('dataRoot')
        dr.fireEvent("add_new_user", user=user)
        #成功信息
        successMsg = "恭喜你已经成功注册了，请稍后登陆系统，我们的工作人员正在为你分配系统资源。"
        return successMsg
        
    def getUserInfo(self, uid):
        #user = User._loadObj(uid)
        user = UserControl.getUser()
        igs = ["last_login", "password", "webserverEngineer", "windowsEngineer", "networkEngineer", "alarmModel", "linuxEngineer", "createTime", "is_active", "saleUser", "serverID", "idcUser"]
        updict = {
                  "ownCompany": user.ownCompany.title, "levelPolicy": user.levelPolicy.title
        }
        return jsonUtils.jsonDoc(user, updict=updict, ignoreProperyties=igs)
    
    def checkUsernameValid(self, username):
        "检测用户名是否可用"
        username = username or ""
        username = username.strip()
        if not username: return False
        if not User.isVaildUserName(username): return False
        user = User._loadByUserName(username)
        if not user: return True
        return False
    
    @apiAccessSettings("edit")
    def  changeUsername(self, uid, username):
        username = username or ""
        username = username.strip()
        vaild = self.checkUsernameValid(username)
        if not vaild:
            return "warn:你申请的用户名[%s]不可用，可能原因此用户名已被使用" %username
        
        user = UserControl.getUser()
        user.username = username
        return "成功修改登陆名，请及时注销，并使用新的登陆名进行登陆"
    
    @apiAccessSettings("edit")
    def changePassword(self, uid, oldPassword, newPassword, confirmPassword):
        user = UserControl.getUser()
        if oldPassword != user.password:
            msg = "旧密码不正确"
            return msg
            
        user.password = newPassword
        
        return "修改密码成功"
    
    @apiAccessSettings("edit")
    def changeEmailAandPhone(self, uid, email, contactPhone):
        user1 = UserControl.getUser()
        username = user1.username
        conditions={"email": email}
        user = User._findObjects(conditions)

        if user and user[0].username != username:
            return "warn:修改邮件及电话失败！填写的邮箱已经注册！"
            return
        user1.email = email
        user1.contactPhone = contactPhone
        return "成功修改邮件及电话..."
    
    def getUsedAlarmRules(self, userId):
        user = User._loadObj(userId)
        rules = user.alarmRules
        return jsonUtils.jsonDocList(rules)
    
    
    def getAllAlarmRules(self):
        user = UserControl.getUser()
        alarmRules = user.getAlarmRules(enable=None)
        return jsonUtils.jsonDocList(alarmRules)
    
    @apiAccessSettings("add")
    def addAlarmRule(self, ruleMedata):
        user = UserControl.getUser()
        rule = AlarmRule()
        rule.__extMedata__(ruleMedata)
        user.addAlarmRule(rule)
        return "成功新增一个告警规则"
    
    @apiAccessSettings("edit")
    def editAlarmRule(self, ruleMedata):
        user = UserControl.getUser()
        rule = AlarmRule._loadObj(ruleMedata.get("_id", ""))
        if not rule: return "fail"
        del ruleMedata["_id"]
        rule.__extMedata__(ruleMedata)
        user.addAlarmRule(rule)
        return "成功更新一个告警规则"
    
    @apiAccessSettings("del")
    def delAlarmRule(self, ruleId):
        user = UserControl.getUser()
        rule = AlarmRule._loadObj(ruleId)
        if not rule: return "fail"
        user.removeAlarmRule(rule)
        return "成功删除一个告警规则"
            
    def checkEmail(self, email):
        user = User._loadByEmail(email)
        if user:
            return False
        return True
    
    def getCollector(self):
        """
        用于管理收集器
        """
        igs = []
        user = UserControl.getUser()
        ownCompany = user.ownCompany
        if ownCompany:
            ownCompanyRefInfo = ownCompany._getRefInfo()
        else:return []
        conditions = {"ownCompany":ownCompanyRefInfo}
        rs = Collector._findObjects(conditions=conditions)
        if not rs: return []
        def updict(doc):
            return {
                  "title": doc.title or doc.getUid(),
                  "ownCompany": doc.title or doc.getUid()
            }
        return jsonUtils.jsonDocList(rs ,  updict=updict, ignoreProperyties=igs)
    
    def _delRefMeObjs(self, coll):
        """
        删除与这个收集器相关联的监控对象
        @param coll:收集器对象 
        @return: 布尔值
        """
        monitorObjs = coll.getAllMonitorObjs()
        for mObj in monitorObjs:
            try:
                mObj.remove()
            except Exception, e:
                return False
        return True
        
    @apiAccessSettings("del")
    def delCollector(self, uids):
        """
        删除收集器
        """
        for uid in uids:
            coll = Collector._loadObj(uid)
            if not coll: return "warn:删除失败，没有找到对应的收集器！"
            if not self._delRefMeObjs(coll):return "warn:删除收集器失败！删除监控对象出错！"
            coll.remove()
            #还要处理收集器的设备
        return "删除收集器成功！"
    
    @apiAccessSettings("edit")
    def editCollector(self, title, mac, bootpoPort, tcpServerPort, uid):
        user = UserControl.getUser()
        ownCompany = user.ownCompany
        if not ownCompany:return "warn:添加失败"
        coll = Collector._loadObj(uid)
        if not coll: return "warn:修改失败，没有找到对应的收集器！"

        
        #if not self.isValidCollector(host):
        #    return "warn:修改失败，验证收集器失败，请先开启收集器的tcp服务"
        coll.title = title
        coll.mac = mac
        coll.bootpoPort = bootpoPort
        coll.tcpServerPort = tcpServerPort      
        coll._saveObj()
        return "修改成功！"
    
    def isValidCollector(self,host="192.168.2.84"):
        try:
            cCall = ColloectorCallClient(host)
            result = cCall.call("CollVerify")
        except:return False
        if result == True:return True
        else:return False
        
    
    @apiAccessSettings("edit")
    def addCollector(self, title, mac, bootpoPort, tcpServerPort):
        """
        同一个公司，MAC不能相同 
        """
        user = UserControl.getUser()
        ownCompany = user.ownCompany
        if not ownCompany:return "warn:添加失败，owncompany"

        exitCollCount = Collector._countObjects({"ownCompany":ownCompany._getRefInfo()})
        maxCollCount = user.levelPolicy.privateCollectorCount
        if exitCollCount >= maxCollCount:
            return "warn:用户最多只能添加%s个私有收集器！" %maxCollCount
        

        coll = Collector()
        coll.title = title
        coll.collType = "private"
        coll.ownCompany = ownCompany
        coll.mac = mac
        coll.bootpoPort = bootpoPort
        coll.tcpServerPort = tcpServerPort
        coll._saveObj()

        return "添加成功！"
    

    def getCollectorSn(self, collUid):
        """
        下载收集器签名证书
        """
        coll = Collector._loadObj(collUid)
        if not coll: return ""
        from products.netPublicModel.collectorLicense import CollectorLicense
        sn = CollectorLicense.createSn(coll.mac, coll.ownCompany.getUid(), collUid)
        return sn
    
    
    def andriodUpdate(self,usrVersion=""):
        update = False
        downloadPath = "/media/android/update.apk"
        versionPath = _p('/products/netMinWeb/media/android/version.txt')
        vf = open(versionPath)
        curVersion = vf.readline().strip()
        vf.close()
        
        if usrVersion.strip() < curVersion: update = True
        return {"update":update,"version":curVersion,"path":downloadPath}	
    
    
    def editInfos(self,originalName,companyName,sign="",icon=""):
        user = UserControl.getUser()
        user.icon=icon
        user.sign = sign
        user.originalName=originalName
        user.ownCompany.title=companyName
        
        return "修改资料成功"
    
  