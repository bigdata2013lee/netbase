#coding=utf-8
from products.netModel.user.baseUser import BaseUser 
from products.netModel import medata
from products.netAlarm.alarmRule import AlarmRule
import time
from products.netUtils import xutils

class User(BaseUser):
    dbCollection = 'netusers'

    def __init__(self, username=None):
        BaseUser.__init__(self)
        self._medata.update(dict(
            is_active=False,
            username=username,
            alarmRules=[],
        ))


    def save(self):
        "Do not del this method, it's created for django"

    def is_authenticated(self):
        "Do not del this method, it's for django"
        return True

    @property
    def is_active(self):
        return self._medata["is_active"]
    
    ownCompany = medata.doc("ownCompany")
    status = medata.plain("status","Normal")#Expired|Normal
    saleUser = medata.doc("saleUser")
    engineer=medata.doc("engineer")
    operationer=medata.doc("operationer")
    money=medata.plain("money",0)
    #用户新的级别两个字段 levelPolicy 是用户选择的级别策略，levelPolicyEndTime 是用户使用对应级别策略有效时间
    levelPolicy = medata.doc("levelPolicy")
    deviceDtail = medata.doc("deviceDtail")
    levelPolicyEndTime = medata.plain("levelPolicyEndTime", 9000000000000) #后面接十二个零，可以代表时间代表无穷大
    newCommentTopicList=medata.plain("newCommentTopicList", [])
    awardNum=medata.plain("awardNum", 100)
    
    @classmethod    
    def _loadByEmail(cls, email):
        conditions = {"email": email}
        users = cls._findObjects(conditions=conditions)
        if users: return users[0]
        return None
    
    @classmethod
    def isVaildUserName(cls,username):
        """
        检测用户名是否可用，或是否有效
        """
        if not username: return False
        if not xutils.isValidEmail(username): return False
        u = cls._loadByUserName(username)
        if u: return False
        return True
    
    @classmethod
    def isVaildPhone(cls, phone):
        """
        检测手机号是否可用，或是否有效
        """
        if not phone:
            print "not phone" 
            return False
        if not xutils.isValidPhone(phone):
            print "not match" 
            return False
        users = cls._findObjects({"contactPhone":phone})
        if users:
            print "user exits" 
            return False
        return True
    
    @classmethod
    def getVaildSysUerName(cls):
        """
        系统生成帐号
        @return s19026565575n010 
        """
        dt = int(time.time()*1000)
        count = cls._countObjects()
        return "s%sn%03d" %(dt, count)
        
        
    
    def getAlarmRules(self, enable=True):
        """
        获取用户的告警规则，默认为已启用的规则
        @param enable: 是否启用 enable==None,查询所有的规则
        """
        ownCompany = self.ownCompany
        if not ownCompany: return []
        _alarmRules = ownCompany._getRefMeObjects("ownCompany", AlarmRule)
        
        if enable is True:
            _alarmRules = filter(lambda x: x.enable is True, _alarmRules)
        elif enable is False:
            _alarmRules = filter(lambda x: x.enable is False, _alarmRules)
        elif enable is None:
            return  _alarmRules
           
        return _alarmRules

    def addAlarmRule(self, rule):
        rule.ownCompany = self.ownCompany
        rule._saveObj()
        
    def removeAlarmRule(self, rule):
        rule.remove()

        
    @staticmethod    
    def filterUsersByUserCompanyAndUserName(conditions={}, users={}):
        _fillters = []
        rs = []
        
        if conditions.get("customer",""):
            _fillters.append({"name":"customer", "val":conditions.get("customer","")})
            
        if conditions.get("ownCompany",""):
            _fillters.append({"name":"ownCompany", "val":conditions.get("ownCompany","")})
        
        def xfillter(user, ft):
            if ft["name"] == "customer":
                v = user.customer.username.find(ft['val'])
                if v == -1: return False
            
            if ft["name"] == "ownCompany":
                from products.netModel.rechargeForm import RechargeForm
                if  isinstance(user, RechargeForm):
                    v = user.customer.ownCompany.titleOrUid().find(ft['val'])
                else:
                    v = user.ownCompany.titleOrUid().find(ft['val'])
                if v == -1: return False
                
            return True
                
                
        if _fillters:
            for user in users:
                for ft  in _fillters:
                    v = xfillter(user, ft)
                    if not v: break
                    if _fillters[-1] != ft:
                        continue
                    rs.append(user)
                    
        else:
            rs = users
        return rs
    
    def  isExpired(self):
        #todo...
        return False
    
    def getExpireTime(self):
        """
        获取用户有效期截止时间
        @note: 针对普通测试用户
        """
        stime = r"N/A"
        return stime
    
    
    def getUserName(self):
        """
        获取用户名
        """
        return self._medata["username"]
    
    def getAllMonitorsByUser(self):
        """
        得到用户的所有监控对象
        """
        from products.netModel.device import Device
        from products.netModel.website import Website
        from products.netModel.network import Network
        monitors = []
        ownCompany = self.ownCompany
        if ownCompany:
            ownCompanyRefInfo = ownCompany._getRefInfo()
        else:return []
        conditions = {"ownCompany":ownCompanyRefInfo}
        devices = Device._findObjects(conditions)
        websites = Website._findObjects(conditions)
        networks = Network._findObjects(conditions)
        monitors.extend(devices)
        monitors.extend(websites)
        monitors.extend(networks)
        return monitors

    

    

    
        
