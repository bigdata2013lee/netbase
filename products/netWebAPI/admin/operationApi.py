#coding=utf-8
import time
import md5
from products.netUtils import xutils
from products.netModel.user.user import User
from products.netWebAPI.base import BaseApi
from products.netUtils.validator import Validator
from products.netBilling.levelPolicy import LevelPolicy
from products.netBilling.extendDevice import ExtendDevice
from products.netModel.ticket.serviceNote import ServiceNote
from products.netPublicModel.userControl import UserControl
from products.netModel.user.engineerUser import EngineerUser
from products.netModel.operation.deviceDtail import DeviceDtail
from products.netModel.operation.operationer import Operationer
from products.netModel.operation.operationServiceCustomer import OperationServiceCustomer
from products.netModel.operation.operationerFavoriteCustomer import OperationFavoriteCustomer
from products.netPublicModel.emailTemplates import extend_device_mail_html, confirm_extend_device_mail_html

'''
time:2014-12-22
@version: netbase4.0
@author: julian
'''

class OperationApi(BaseApi):    
    '''
    time:2014-12-23
    @author: julian
    @todo: 运营商的API接口类
    '''
    
    def listServiceCustomers(self, conditions={}, sortInfo=None, skip=0, limit=None):
        """
        time:2014-12-23
        @author: julian
        @todo: 列出运维商的服务客户列表
        @param conditions: <dict>检索运维商服务客户的条件，默认是空字典
        @param sortInfo: <String>对检索结果进行排序的字段，默认为None
        @param skip: <int>跳过的记录数，默认为0
        @param limit: <int>限制检索结果的记录数，默认是None
        @return: <dict>返回运维商服务的客户的字典
        @note: 根据运维商检索其服务的客户
        """
        operationer = UserControl.getUser()
        conditions = {"operationer":operationer._getRefInfo()}
        oscObjs = {}
        oscObjs["result"] = OperationServiceCustomer._findObjects(conditions=conditions, sortInfo=sortInfo, skip=skip, limit=limit)
        oscObjs["total"] = OperationServiceCustomer._countObjects(conditions=conditions)
        return oscObjs
    
    def listFavoriteCustomers(self, conditions={}, sortInfo=None, skip=0, limit=None):
        '''
        time:2014-12-23
        @author: julian
        @todo: 列出运维商收藏客户列表
        @param conditions: <dict>检索运维商收藏客户的条件，默认是空字典
        @param sortInfo: <String>对检索结果进行排序的字段，默认为None
        @param skip: <int>跳过的记录数，默认为0
        @param limit: <int>限制检索结果的记录数，默认是None
        @return: <dict>返回运维商收藏的客户的字典
        @note: 根据运维商检索其收藏的客户
        '''
        operationer = UserControl.getUser()
        conditions = {"operationer":operationer._getRefInfo()}
        ofcObjs = {}
        ofcObjs["result"] = OperationFavoriteCustomer._findObjects(conditions=conditions, sortInfo=sortInfo, skip=skip, limit=limit)
        ofcObjs["total"] = OperationFavoriteCustomer._countObjects(conditions=conditions)
        return ofcObjs
        
    def addServiceCustomer(self, customerUsername):
        """
        time:2014-12-23
        @author: julian
        @todo: 运维商添加自己的服务客户
        @param customerUsername: <string>客户帐号
        @return: <string> 添加客户成功的提示信息或失败警告信息
        @note: 1.检查该客户是否存在，如果不存在，则添加失败
                    2.检查该客户是否被添加，如果已经添加，则添加失败
        """
        operationer = UserControl.getUser()
        customer = User._loadByUserName(customerUsername)
        if not customer:
            return "warn:该客户已经不存在，添加服务客户失败"
        oscs = OperationServiceCustomer._findObjects({"customer":customer._getRefInfo()})
        if len(oscs) > 0:return "warn:您已经添加该客户"
        customer.operationer = operationer
        osc = OperationServiceCustomer()
        osc.customer = customer
        osc.operationer = operationer        
        osc._saveObj()
        return "添加服务客户成功"
    
    def getOperationerEngineers(self):
        """
        time:2014-12-23
        @author: julian
        @todo: 获取运维商的工程师列表
        @return:<list> 返回运维商的工程师列表
        @note: 如果运维商不存在则返回空列表，否则返回运维商的工程师列表
        """
        operationer = UserControl.getUser()
        if not operationer: return []
        return operationer.engineers
    
    
    def appointServiceEngineer(self, engineerId, operationServiceCustomerId):
        """
        time:2014-12-23
        @author: julian
        @todo: 指派服务工程师
        @param engineerId: <string>工程师ID
        @param operationServiceCustomerId:<string> 运维商的服务客户ID
        @return: <string>返回操作成功与否的提示
        @note: 1.更改服务客户的工程师
                    2.更改服务客户的打开的工单的工程师
        """
        osc = OperationServiceCustomer._loadObj(operationServiceCustomerId)
        engineer = EngineerUser._loadObj(engineerId)
        if not engineer:return "warn:找不到指定的工程师"
        osc.engineer = engineer
        osc.customer.engineer = engineer
        serviceNotes = ServiceNote._findObjects({"user":osc.customer._getRefInfo(), "status":0})
        for serviceNote in serviceNotes:
            serviceNote.engineer = engineer
        return "指派成功！"
    
        
    def searchFavoriteCustomers(self, companyName=""):
        """
        time:2014-12-23
        @author: julian
        @todo: 查找收藏的客户
        @param companyName: <string>公司名称
        @return: <list>返回运维商收藏的客户的详细信息列表
        @note: 如果没有给出查询条件，就默认获取所有的收藏的客户
        """
        operationer = UserControl.getUser()
        ofcs = operationer._getRefMeObjects("operationer", OperationFavoriteCustomer)
        if companyName:
            companyName = companyName.strip()
        if not companyName: return ofcs
        favoriteCustomers = []
        for ofc in ofcs:
            customer = ofc.customer
            if not customer: continue
            if customer.ownCompany.title.find(companyName) >= 0:
                favoriteCustomers.append(ofc)            
        return favoriteCustomers
       
    def addFavoriteCustomer(self, customerId):      
        """
        time:2014-12-23
        @author: julian
        @todo: 添加收藏的客户
        @param customerId: <string>客户ID
        @return: <string>返回操作成功与否的提示
        @note: 1.在合约有效期内才能收藏
                    2.该客户的账号是否存在
                    3.不能重复收藏
        """  
        operationer = UserControl.getUser()
        customer = User._loadObj(customerId)
        if not customer:
            return "warn:客户信息不存在！"
        count = OperationFavoriteCustomer._countObjects(conditions={"customer":customer._getRefInfo(), "operationer":operationer._getRefInfo()})
        if count:
            return "warn:您已经收藏，不能再收藏了！"
        ofc = OperationFavoriteCustomer()
        ofc.customer = customer
        ofc.operationer = operationer
        ofc._saveObj()
        return "客户收藏成功！"
        
        
    def removeFavoriteCustomer(self, favoriteCustomerId):
        """
        time:2014-12-23
        @author: julian
        @todo: 移除收藏的客户
        @param favoriteCustomerId: <string>要被移除客户的ID
        @return: <string>返回操作成功与否的提示
        """
        ofc = OperationFavoriteCustomer._loadObj(favoriteCustomerId)
        if not ofc:
            return "此收藏客户不存在！"
        ofc.remove()
        return "成功移除此收藏客户！"
    
    def removeCustomer(self, serviceCustomerId):
        """
        time:2014-12-23
        @author: julian
        @todo: 移除服务的客户
        @param serviceCustomerId: <string>要删除的服务客户ID
        @return: <string>返回操作成功与否的提示
        @note: 1.将该客户的服务工程师和运营商置空
                    2.置空工单的工程师，并将该客户所有的打开的工单关闭
                    3.删除服务的客户
        """
        osc = OperationServiceCustomer._loadObj(serviceCustomerId)
        if not osc:
            return "此服务客户不存在！"
        osc.customer.engineer = None
        osc.customer.operationer = None
        conditions = {}
        conditions.update({"user":osc.customer._getRefInfo()})
        serviceNotes = ServiceNote._findObjects(conditions)
        for sn in serviceNotes:
            sn.engineer = None
            if sn.status == 0:
                sn.status = 1
                sn.endTime = int(time.time())
        osc.remove()
        return "成功移除此服务客户！"
        
    def  addEngineer(self, username, password, originalName, email):
        """
        time:2014-12-23
        @author: julian
        @todo: 添加工程师
        @param username: <string>要添加的工程师的账号，必须为邮箱格式
        @param password: <string>要添加的工程师的登录密码
        @param originalName: <string>要添加的工程师的真实姓名
        @return: <string>返回操作成功与否的提示
        @note: 1.已存在帐号不能添加
                    2.最多只能注册50个工程师的账号
        """
        rules = {
           "username":"email", "password":{"rule":"regex", "regex":r"^\w{6,20}$"}, "originalName":"required", "email":"email"
        }
        messages = {
               "username":"帐号请使用一个正确的邮箱",
               "password":"密码请使用 数字、字母、下划线6~20个字符",
               "originalName":"姓名是必填项",
               "email":"请填写有效联系邮箱"
        }
        params = dict(username=username, password=password, originalName=originalName, email=email)
        vrs = Validator(rules=rules, messages=messages).v(params)
        if not vrs[0]:  return "warn:%s" % vrs[1]
        operationer = UserControl.getUser()
        count = EngineerUser._countObjects(conditions={"username":username})
        if count > 0:
            return "warn:您所输入的账号已存在，不能创建"
        if len(operationer.engineers) >= 50:
            return "warn:不能添加过多的工程师帐号"        
        engineerUser = EngineerUser()
        engineerUser.username = username
        engineerUser.email = email
        engineerUser.password = md5.new(password).hexdigest()
        engineerUser.originalName = originalName
        engineerUser.operationer = operationer
        engineerUser.email = email
        engineerUser.createTime = time.time()
        engineerUser._saveProperty2("is_active", True)
        engineerUser._saveObj()
        return "成功添加工程师！"
    
    
    def modifyEngineerPWD(self, engineerId, password):
        """
        time:2014-12-23
        @author: julian
        @todo: 修改工程师的秘密
        @param engineerId: <string>被修改密码的工程师的ID
        @param password: <string>被修改密码的工程师的密码
        @return: <string>返回操作是否成功的提示
        """
        engineerUser = EngineerUser._loadObj(engineerId)
        if not password: return "warn:密码不能设置为空"
        if not engineerUser: return "warn:操作不成功！"
        engineerUser.password = md5.new(password).hexdigest()              
        return "修改成功！"
    
    
    def deleteEngineer(self, engineerId):
        """
        time:2014-12-23
        @author: julian
        @todo: 删除注册的工程师账号
        @param engineerId: <string>要被删除的工程师的ID
        @return: <string>返回操作成功与否的提示
        @note: 1.该工程师是否存在
                    2.尚未解除服务客户的工程师不能删除
        """
        engineerUser = EngineerUser._loadObj(engineerId)
        if not engineerUser:
            return "warn:操作不成功！"        
        customers = engineerUser.users
        if len(customers) > 0:
            return "warn:请先解除此工程师的服务客户！"
        engineerUser.remove()
        return "删除成功！"

    def showServiceCustomers(self, engineerId):
        """
        time:2014-12-23
        @author: julian
        @todo: 显示工程师服务的客户列表
        @param engineerId: <string>工程师ID
        @return: <list>返回该工程师所服务的客户列表
        """
        engineerUser = EngineerUser._loadObj(engineerId)
        customers = engineerUser.users
        return customers
    
        
    def editPersonalInfo(self, companyName, bussinessLicenseNum, phoneNum, address, companydescription, icon="",
                     technologyFileds=[], technologyForte="", serviceAreas=[]):
        """
        @author: julian
        @todo: 编辑运维商的个人资料
        @param companyName: <string>运维商的公司
        @param bussinessLicenseNum: <string>运维商的营业执照编号
        @param phoneNum: <string>运维商的联系电话
        @param address: <string>运维商的地址
        @param companydescription: <string>公司简介
        @param technologyFileds: <list>运维商的技术领域
        @param technologyForte: <string>运维商的技术特长
        @param serviceAreas: <list>运维商的服务领域
        @return: <string>返回操作成功与否的提示
        """
        op = UserControl.getUser()
        op.icon = icon
        baseInfo = op.baseInfo
        baseInfo["companyName"] = companyName;
        baseInfo["bussinessLicenseNum"] = bussinessLicenseNum
        baseInfo["phoneNum"] = phoneNum
        baseInfo["address"] = address
        op.baseInfo = baseInfo
        serviceInfo = op.serviceInfo  
        serviceInfo["technologyFileds"] = technologyFileds;
        serviceInfo["technologyForte"] = technologyForte
        serviceInfo["serviceAreas"] = serviceAreas
        op.serviceInfo = serviceInfo    
        op.companydescription = companydescription
        return "您的资料已经成功修改"
    
    def searchOperationers(self, technologyFileds=[], skip=0, limit=None):
        """
        time:2014-12-23
        @author: julian
        @todo: 查找运维商
        @param technologyFileds: <list>技术领域(查询条件)
        @param skip:<string> 当前所展示记录数
        @param limit: <string>每页显示多少条信息
        @return: <dict>返回运维商的信息列表和页数
        """
        conditions = {}
        if technologyFileds: 
            conditions = {"serviceInfo.technologyFileds":{"$in":technologyFileds}}
        operationers = Operationer._findObjects(conditions=conditions, sortInfo=None, skip=skip, limit=limit)
        objectCount = Operationer._countObjects(conditions=conditions)
        return {"total":objectCount, "results": operationers}

    def searchCustomers(self, conditions={}, sortInfo=None, skip=0, limit=None):
        '''
        time:2014-12-23
        @author: julian
        @todo: 搜索客户
        @param conditions: <dict>搜索条件
        @param sortInfo: <String>对检索结果的排序信息
        @param skip: <int>跳过的记录数
        @param limit: <int>限制最多列出的记录数
        @return: 检索的客户字典
        '''
        customers = User._findObjects(conditions=conditions, sortInfo=sortInfo, skip=skip, limit=limit)
        objectCount = User._countObjects(conditions=conditions)
        return {"total":objectCount, "results": customers}
    
    def extendDevice(self, host, website, network):
        '''
        time:2014-12-23
        @author: julian
        @todo: 扩展设备
        @param host: 要扩展的主机数
        @param website: 要扩展的站点数
        @param network: 要扩展的网络数
        @return: 扩展设备的提示信息
        @note: 1.验证要添加的主机，站点，网络数目是否合法
                    2.计算总费用
                    3.保存充值记录
                    4.发送通知邮件
        '''
        user = UserControl.getUser()
        if not user:return "warn:请先登录"
        if not xutils.isValiedNum(host):return "warn:主机数目只能为非负数,且不能以0开头"
        if not xutils.isValiedNum(website):return "warn:站点数目只能为非负数,且不能以0开头"
        if not xutils.isValiedNum(network):return "warn:网络数目只能为非负数,且不能以0开头"
        host = int(host)
        website = int(website)
        network = int(network)
        if host > 0 and host < 10:return "warn:请至少购买10台主机"
        if website > 0 and website < 10:return "warn:请至少购买10个站点"
        if network > 0 and network < 10:return "warn:请至少购买10台网络设备"
        money_host = xutils.countMoney(host, 4.0, xutils.setDiscount(host))
        money_website = xutils.countMoney(website, 4.0, xutils.setDiscount(website))
        money_network = xutils.countMoney(network, 4.0, xutils.setDiscount(network))
        money = money_host + money_website + money_network
        if int(money) == 0:return "请至少选择一种需要扩充的设备类型"
        extendDevice = ExtendDevice()
        extendDevice.user = user
        extendDevice.deviceCount = host
        extendDevice.websiteCount = website
        extendDevice.networkCount = network
        extendDevice.money = money
        extendDevice._saveObj()
        try:
            self.extendDeviceMail(extendDevice, "网脊运维商")
        except:
            return "您的请求已提交，虽然未能正确发送邮件，但是稍后我们会主动联系您，多谢您的支持"
        return "您的请求已提交，稍后我们会主动联系您，多谢您的支持"
    
    def extendDeviceMail(self, ed, st):
        '''
        time:2014-12-23
        @author: julian
        @todo: 扩充设备发送通知邮件
        @param ed: <ExtendDevice>设备扩充对象
        @param st: <ServiceNote>工单对象
        '''
        subject = st + "设备扩充通知"
        message = extend_device_mail_html % {
                   "deviceCount":ed.deviceCount,
                   "websiteCount":ed.websiteCount,
                   "networkCount":ed.networkCount,
                   "user":ed.user.username,
                   "email":ed.user.email,
                   "contactPhone":ed.user.contactPhone,
                   "originalName":ed.user.originalName,
                   "money":ed.money
                }
        xutils.sendMail(subject, message, recipient_list=[ed.user.username], attachments=[]) 
    
    def getAvailableDevice(self, operationer):
        '''
        time:2014-12-23
        @author: julian
        @todo: 获得可用的设备
        @param operationer: <Operationer>运营商对象
        @return: <dict>可用设备字典
        '''
        deviceTotal = {"host":0, "website":0, "network":0}
        deviceUsed = {"host":0, "website":0, "network":0}
        deviceAvailable = {"host":0, "website":0, "network":0}
        
        deviceTotal["host"] = operationer.levelPolicy.deviceCount
        deviceTotal["website"] = operationer.levelPolicy.websiteCount
        deviceTotal["network"] = operationer.levelPolicy.networkCount
        
        deviceUsed["host"] = operationer.deviceDtail.deviceCount
        deviceUsed["website"] = operationer.deviceDtail.websiteCount
        deviceUsed["network"] = operationer.deviceDtail.networkCount      
        
        deviceAvailable["host"] = deviceTotal["host"] - deviceUsed["host"]
        deviceAvailable["website"] = deviceTotal["website"] - deviceUsed["website"]
        deviceAvailable["network"] = deviceTotal["network"] - deviceUsed["network"]        
        return deviceAvailable
   
    def extendDeviceByOperationer(self, host, website, network, userid=""):
        '''
        time:2014-12-23
        @author: julian
        @todo: 运营商为他的客户添加设备
        @param host: <int>要添加的主机数
        @param website: <int>要添加的站点数
        @param network: <int>要添加的网络设备数
        @param userid: <String>客户的uid
        @return: 添加成功与否的提示信息
        @note: 1.验证host,website,network数目是否符合规则
                    2.检查运维商可用的设备数是否充足
                    3.执行添加动作
                    4.给用户发送通知邮件
        '''
        operationer = UserControl.getUser()
        if userid:user = User._loadObj(userid)
        if not operationer:return "warn:请先登录"
        if not user:return "warn:该用户已不存在"
        if not xutils.isValiedNum(host):return "warn:主机数目只能为非负数,且不能以0开头"
        if not xutils.isValiedNum(website):return "warn:站点数目只能为非负数,且不能以0开头"
        if not xutils.isValiedNum(network):return "warn:网络数目只能为非负数,且不能以0开头"
        if not operationer.levelPolicy:
            levelPolicy = LevelPolicy()
            levelPolicy._saveObj()
            operationer.levelPolicy = levelPolicy
        if not operationer.deviceDtail:
            deviceDtail = DeviceDtail()
            deviceDtail._saveObj()
            operationer.deviceDtail = deviceDtail
        if not user.levelPolicy:
            user = LevelPolicy()
            user._saveObj()
            user.levelPolicy = levelPolicy
        host = int(host)
        website = int(website)
        network = int(network)
        if host == 0 and website == 0 and network == 0:return "warn:请至少选择一种需要扩充的设备类型"
        deviceAvailable = self.getAvailableDevice(operationer)
        _host = host - deviceAvailable["host"]
        _website = website - deviceAvailable["website"]
        _network = network - deviceAvailable["network"]
        if _host > 0:return "warn:您的可用主机数量为 %d台，还需要扩充 %d台才可以做此操作" % (deviceAvailable["host"], _host)
        if _website > 0:return "warn:您的可用站点数量为 %d个，还需要扩充 %d个才可以做此操作" % (deviceAvailable["website"], _website)
        if _network > 0:return "warn:您的可用网络设备数量为 %d台，还需要扩充 %d台才可以做此操作" % (deviceAvailable["network"], _network)
        operationer.deviceDtail.deviceCount += host
        operationer.deviceDtail.websiteCount += website
        operationer.deviceDtail.networkCount += network
        user.levelPolicy.deviceCount += host
        user.levelPolicy.websiteCount += website
        user.levelPolicy.networkCount += network        
        try:
            self.extendDeviceByOperationMail(host, website, network, user, money="")
        except:
            return "虽然未能正确发送邮件，但是已成功为用户添加设备，多谢您的支持"
        return "已成功为用户添加设备，感谢您对网脊运维通的支持"        
    
    
    def extendDeviceByOperationMail(self, host, website, network, user, money=""):
        '''
        time:2014-12-23
        @author: julian
        @todo: 运营商为客户添加设备后，为客户发送通知邮件
        @param host: <int>要添加的主机数
        @param website: <int>要添加的站点数
        @param network: <int>要添加的网络设备数
        @param user: <User>要通知的用户
        @param money: 总金额        
        '''
        subject = "设备扩充通知"
        firstSentence = "已为您扩充设备信息如下："
        message = confirm_extend_device_mail_html % {
                   "deviceCount":host,
                   "websiteCount":website,
                   "networkCount":network,
                   "user":user.username,
                   "money":money,
                   "firstSentence":firstSentence
                }
        xutils.sendMail(subject, message, recipient_list=[user.username], attachments=[]) 
    
    

            
            
        
        
        
        
        
            
        
    
        
        
        
        
        
        
    
    
    
        
    
