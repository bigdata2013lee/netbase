# -*- coding: utf-8 -*-
from django.http import HttpResponse
import json

from products.netPublicModel.userControl import UserControl
from products.netWebAPI.admin.engineerApi import EngineerApi
from products.netWebAPI.admin.saleApi import SaleApi
from products.netWebAPI.serviceNoteApi import ServiceNoteApi
from products.netWebAPI.admin.adminUserApi import AdminUserApi
from products.netWebAPI.messageApi import MessageApi
from products.netWebAPI.admin.operationApi import OperationApi
from products.netWebAPI.communityApi.topicApi import TopicApi


apiClasses = [
              EngineerApi,
              SaleApi,
              MessageApi,
              ServiceNoteApi,
              AdminUserApi,
              OperationApi,
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


def remoteView(request, apiClsName, methodName):
    cls = getApiClasses(apiClsName)
    if not cls:raise Exception("Can't find remote api class [%s]" % apiClsName)
    
    user = request.user
    UserControl.setUser(user)
    
    if cls and hasattr(cls, methodName):
        params = _loadParams(request, 'params')
        inst = cls()
        inst.request = request
        m = getattr(inst, methodName)
        params = dict([[str(k), v] for k, v in params.items()])
        rs = m(**params)
        return HttpResponse(json.dumps(rs))
    
    raise Exception("Can't find remote method[%s] with api class [%s]" % (methodName, apiClsName))
