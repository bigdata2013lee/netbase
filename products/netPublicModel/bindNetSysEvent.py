#coding=utf-8
'''
Created on 2013-3-18

@author: Administrator
'''
from products.netModel.org.webSiteClass import WebSiteClass
from products.netModel.templates.template import Template
import re
from products.netModel.user.engineerUser import EngineerUser



#--------------------------------handlers-------------------------------------

def add_new_device_bind_tpl_handler(dev):
    "add_new_device_bind_tpl_handler"
    tplMaps = {"linux": "BaseTpl_Linux", "windows":"BaseTpl_Window"}
    if not dev.deviceCls: return False
    devType = dev.deviceCls.uname
    
    if not devType: return
    tplName = tplMaps.get(devType)
    
    tpl = Template._loadObj(tplName) #基本模板
    dev.bindTemplate(tpl)
        

def add_new_website_handler(website):
        pass
                
def add_new_user_handler(user):
    wsc = WebSiteClass(uname=WebSiteClass.rootUname,title="站点")
    wsc.ownCompany = user.ownCompany
    defaultEngineerUser = EngineerUser._loadObj("netbase") #把netbase工程师设置为默认工程师
    user.linuxEngineer = defaultEngineerUser
    user.windowsEngineer = defaultEngineerUser
    wsc._saveObj()
       
def add_new_network_bind_tpl_handler(net):  
    
    from products.netPublicModel import devTemplateMaps
    productId = net.productId
    path = devTemplateMaps.getRootDir(productId)
    net_tpl_list = devTemplateMaps.networkDevice.get(path).get(productId,[])
    if not net_tpl_list:
        print "warn:can not bind the base template!"
        return
    tplName = net_tpl_list[0]
    tpl = Template._loadObj(tplName) #基本模板
    net.bindTemplate(tpl)
    return "绑定成功"

def add_new_middleware_bind_tpl_handler(mw):
    from products.netModel.middleware import baseTemplateMaps
    tplName = baseTemplateMaps.tplMaps.get(mw.__class__.__name__, "")
    tpl = Template._loadObj(tplName)
    mw.bindTemplate(tpl)
    return "绑定成功"

def delCollectorDatasForRemoveMonitorObj(obj):
    """
    删除监控对象时，删除收集器端的数据
    @note: 删除收集器端的数据表，仍会有残留，可能原因1.收集器不存在，2.数据库未打开 3.收集、分析进程插入新数据
    需要在后期维护过程中，使用工具去进一步清理
    """
    from products.netModel import  mongodbManager as dbManager
    if obj:
        print "long info: 要删除的对象不存在"
        return
    
    dbName = obj._getPerfDbName()
    db = dbManager.getNetPerfDB(dbName)
    uid = obj.getUid()
    for tableName in db.collection_names():
        #表都以uid:开头
        if re.search(r"^%s\:" %uid, tableName):
            db.drop_collection(tableName)
            

            
#--------------------------------bindDataRootEvents------------------------
def bindDataRootEvents():
    from products.netPublicModel.modelManager import ModelManager as MM
    dr = MM.getMod('dataRoot')
    dr.on('add_new_device', add_new_device_bind_tpl_handler)
    dr.on('add_new_website', add_new_website_handler)
    
    dr.on("add_new_user", add_new_user_handler)
    dr.on("add_new_network", add_new_network_bind_tpl_handler)
    dr.on("add_new_middleware", add_new_middleware_bind_tpl_handler)
    
    dr.on("removeMonitorObj", delCollectorDatasForRemoveMonitorObj)
    
