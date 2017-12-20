#coding=utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from products.netModel.org.networkClass import NetworkClass
from products.netModel.network import Network
import json
from products.netModel.baseModel import RefDocObject



def _loadParams(request, pname):
    q = request.REQUEST.get(pname, "{}")
    q = json.loads(q)
    return q


    
#-------------------------------------------------------------------------------------------    
def index(request):
    root = NetworkClass.getRoot()
    return render_to_response("network/cls_index.html",RequestContext(request, {"orgUid":root.getUid()})) 

def networkClsIndex(request, orgUid):
    
    return render_to_response("network/cls_index.html", RequestContext(request, {"orgUid":orgUid}))
    
def networkIndex(request, moUid):
    
    networkType = Network._loadObj(moUid).networkCls.parent.uname
    return render_to_response("network/network_index.html", RequestContext(request, {"moUid":moUid, "networkType": networkType})) 

    
def configGrid(request):
    user=request.user
    ownCompany=user.ownCompany
    conditions={"ownCompany":RefDocObject.getRefInfo(ownCompany)}
    usedNum = Network._countObjects(conditions)
    count=user.levelPolicy.networkCount
    availableNum=count - usedNum
    numDic={"usedNum":usedNum,"count":count,"availableNum":availableNum}
    context=dict(numDic=numDic)
    return render_to_response("network/configGrid.html",RequestContext(request, context)) 
    
def devicesConfigOp(request, moUid):
    return render_to_response("network/devicesConfigOp.html", RequestContext(request, {"moUid":moUid })) 

    

