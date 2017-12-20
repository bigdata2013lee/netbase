#coding=utf-8
from products.netAlarm.alarmRule import AlarmRule
from products.netInitData import addComponentTemplate, addTemplateDb, addWebSiteTemplate, initCollectors, \
    initEngineerUsers, initSaleUsers, initIDCProviders, initDefaultBillings,addRaidTemplate,\
    addIpmiTemplate
from products.netInitData.devicecls import initDeviceClass
from products.netInitData.initCollectPoint import initCollectPoint
from products.netInitData import initCiscoTemplates
from products.netInitData.networkcls import initNetworkClass
from products.netInitData.middlewarecls import initMiddlewareClass
from products.netInitData.addTomcatTemplate import startCreateTomcatTemplate
from products.netInitData.addApacheTemplate import startCreateApacheTemplate
from products.netInitData.addIIStemplate import startCreateIISWMITemplate
from products.netInitData.addNginxTemplate import startCreateNginxTemplate
from products.netInitData.ciscoCatalystTpls import CiscoCatalyst
from products.netInitData import check_point
from products.netInitData.networkTpl import addNetworkTpls
from products.netInitData import juniperTemplate
from products.netInitData import addAdminUser
from products.netModel.user.user import User
from products.netModel.company import Company
from time import time
from products.netModel.org.webSiteClass import WebSiteClass
from products.netUtils.settings import ManagerSettings
from products.netBilling.levelPolicy import LevelPolicy
from products.netInitData.createLevelPolicy import initLevelPolicies
from products.netModel.org.location import Location
from products.netModel.user.engineerUser import EngineerUser
from products.netModel.user.saleUser import SaleUser
from products.netModel.idcProvider import IdcProvider
from products import sysStaticConf

settings = ManagerSettings.getSettings()
class InitData(object):
    
    
        
    def addAlarmRule(self,title,description,condition):
        """
        增加告警规则
        """
        rule = AlarmRule()
        rule._medata["title"] = title
        rule._saveObj()
        rule.conditions = condition
        rule.description = description
        
    def addDemoUser(self):
        username = sysStaticConf.get("demo", "demoUserName")
        pwd = sysStaticConf.get("demo", "demoPwd")
        email = sysStaticConf.get("demo", "demoEmail")
            
        u = User(username)
        u.password = pwd
        u.email = email
        u.contactPhone = ''
        u.createTime = time()
        u._saveObj()
        u._saveProperty2("is_active", True)
        
        cpy = Company()
        cpy.title = "demo"
        cpy._saveObj()
        u.ownCompany = cpy

        u.ownCompany = cpy
        loc = Location()
        loc.locType = "default"
        loc.title="默认分组"
        loc.ownCompany = cpy
        loc._saveObj()
                            
        wsc = WebSiteClass(uname=WebSiteClass.rootUname,title="站点")
        wsc.ownCompany = u.ownCompany
        wsc._saveObj()
        u.levelPolicy = LevelPolicy._loadObj("enterprise")
        
        IdcProviders = IdcProvider._findObjects()
        u.idcProvider = IdcProviders and  IdcProviders[0] or  None
        
        engineerUsers = EngineerUser._findObjects()
        u.engineer = engineerUsers and  engineerUsers[0] or  None
        
        saleUsers = SaleUser._findObjects()
        u.saleUser = saleUsers and  saleUsers[0] or None
        
        
        return "success"
    
    def initData(self):
        """
                初始化数据
        """
        #初始化运维商
        initIDCProviders.initProviders()
        #初始化默认认购单位
        initDefaultBillings.initBillings()
         
        #创建销售
        initSaleUsers.initSaleUsers()
        
        #创建工程师
        initEngineerUsers.initEngineers()
        
        #创建超级管理员
        addAdminUser.addAdminUser()
        
        #初始化用户级别策略
        initLevelPolicies()
         
        #创建一个demo用户
        self.addDemoUser()
         
        #创建设备类型
        initDeviceClass()
        #创建网络设备类型，生成目录树
        initNetworkClass()
        #创建中间件设备类型，生成目录树
        initMiddlewareClass()
        #初始化收集器
        initCollectors.initCollectors()
        
        #初始化收集点对象
        initCollectPoint()
        
        #创建中间件模板
        #创建中间件tomcat模板
        startCreateTomcatTemplate()
        #创建中间件apache模板
        startCreateApacheTemplate()
        #创建中间件IIS模板
        startCreateIISWMITemplate()
        #创建中间件nginx模板
        startCreateNginxTemplate()
         
        #创建设备模板
        #SNMP Linux性能模板
        addTemplateDb.startCreateLinuxSNMPTemplate()
        #SNMP Window性能模板
        addTemplateDb.startCreateWindowSNMPTemplate()
        #命令行性能模板
        addTemplateDb.startCreatCmdTemplate()
        #接口模板
        addComponentTemplate.createInterfaceTemplate()
        #进程模板
        addComponentTemplate.createProcessTemplate()
        #文件系统模板
        addComponentTemplate.createFileSystemTemplate()
        #raid模板
        addRaidTemplate.startCreatRaidTemplate()
        #ipmi监控Linux机箱温度与风扇情况
        addIpmiTemplate.startCreatIpmiTemplate()
        #增加web站点模板
        addWebSiteTemplate.startCreateWebSiteTemplate()
        #增加思科系列模板
        initCiscoTemplates.initCiscoTemplates()
        CiscoCatalyst.createCiscoCatalystTemplate()
        #增加Juniper系列模板
        juniperTemplate.startCreateJuniperTemplate()
        #增加网络设备各系列模板
        addNetworkTpls.createNetworkTpls()
        #增加checkpoint模板
        check_point.createCheckPointTemplate()
if __name__== "__main__":
    InitData().initData()
