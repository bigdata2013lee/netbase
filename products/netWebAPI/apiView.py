# -*- coding: utf-8 -*-
from django.http import HttpResponse
import json

from products.netWebAPI.eventApi import EventApi
from products.netWebAPI.userApi import UserApi
from products.netWebAPI.managerApi import  ManagerApi
from products.netWebAPI.monitorApi import  MonitorApi
from products.netWebAPI.websiteApi import WebsiteApi  
from products.netWebAPI.treeViewApi import  TreeViewApi
from products.netWebAPI.deviceApi import DeviceApi
from products.netWebAPI.bootpoApi import BootpoApi
from products.netWebAPI.serviceNoteApi import ServiceNoteApi
from products.netWebAPI.userMessageApi import UserMessageApi
from products.netWebAPI.networkApi import NetworkApi
from products.netWebAPI.middlewareApi import MiddlewareApi
from products.netWebAPI.feedBackInfoApi import FeedBackInfoApi
from products.netWebAPI.shortcutCmdApi import ShortcutCmdApi
from products.netWebAPI.thresholdApi import ThresholdApi
#from products.netWebAPI.vmhostApi import VmhostApi
from products.netWebAPI.locationApi import LocationApi
from products.netWebAPI.messageApi import MessageApi
from products.netWebAPI.reportApi import ReportApi
from products.netWebAPI.billingApi import BillingApi
from products.netWebAPI.customerMapApi import CustomerMapApi
from products import sysStaticConf
from products.netWebAPI.communityApi.topicApi import TopicApi
#from products.netswgl.webApi.swglApi import SwglApi


apiClasses = [
        UserApi,
        EventApi,
        ManagerApi,
        MonitorApi,
        TreeViewApi,
        WebsiteApi,
        DeviceApi,
        BootpoApi,
        ServiceNoteApi,
        UserMessageApi,   
        NetworkApi,
        MiddlewareApi,
        FeedBackInfoApi,
        ShortcutCmdApi,
        ThresholdApi,
        #VmhostApi,
        ReportApi,
        MessageApi,
        LocationApi,
        BillingApi,
        CustomerMapApi,
        #SwglApi,
        TopicApi,
    ]

def getApiClasses(clsName):
    for apiCls in apiClasses:
        if apiCls.__name__ == clsName:
            return apiCls
    return None

def _loadParams(request, pname):
    q = request.REQUEST.get(pname, "{}")
    q = json.loads(q)
    return q

def allowDemoUserAccess(m):
    "demo 用户访问控制"
    from products.netPublicModel.userControl import UserControl
    user = UserControl.getUser()
    if  not m: return True
    if not user: return True
    if user.username != sysStaticConf.get("demo", "demoUserName"): return True
    
    accessSettings = getattr(m, "accessSettings",{})
    if accessSettings.get("name","") in  ["add","del","edit"]: return False
    
    return True
    
        

def remoteView(request, apiClsName, methodName):
    cls = getApiClasses(apiClsName)
    if not cls:raise Exception("Can't find remote api class [%s]" % apiClsName)
    
    if cls and hasattr(cls, methodName):
        params = _loadParams(request, 'params')
        inst = cls()
        inst.request = request
        m = getattr(inst, methodName)
        if not allowDemoUserAccess(m):
            return HttpResponse(json.dumps("warn:Demo用户禁访问!"))
        
        params = dict([[str(k), v] for k, v in params.items()])
        rs = m(**params)
        return HttpResponse(json.dumps(rs))
    
    raise Exception("Can't find remote method[%s] with api class [%s]" % (methodName, apiClsName))
