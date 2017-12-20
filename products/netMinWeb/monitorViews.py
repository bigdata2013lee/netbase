#coding=utf-8
import json
import random
import time
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from products.netModel.org.deviceClass import DeviceClass
from products.netWebAPI.deviceApi import DeviceApi
from products.netUtils.xutils import nbPath as _p
from products.netModel.org.location import Location
from products.netModel.device import Device
from products.netModel.baseModel import RefDocObject
from products.netPublicModel.userControl import UserControl

def _loadParams(request, pname):
    q = request.REQUEST.get(pname, "{}")
    q = json.loads(q)
    return q

def _getMo(mtype, uid):
    from products.netModel.device import Device
    from products.netModel.website import Website
    
    mTypes = { "Device":Device, 'Website':Website  }
    mcls = mTypes.get(mtype)
    return mcls._loadObj(uid)
    
    
#-------------------------------------------------------------------------------------------    
def index(request):
        org=DeviceClass.findByPath("/devicecls/linux")
        loc = Location.getDefault()
        return HttpResponseRedirect( "/monitor/deviceCls/%s/%s/" %(org.getUid(), loc.getUid()))
        
def deviceClsIndex(request, orgUid, locUid):
        return render_to_response("monitor/monitor_index.html", RequestContext(request, {"orgUid":orgUid, "locUid":locUid})) 
        
def deviceIndex(request, moUid):
    dev = Device._loadObj(moUid)
    if dev:
        locUid = dev.location.getUid()
        orgUid = dev.deviceCls.getUid()
    return render_to_response("monitor/device_index.html", RequestContext(request, {"moUid":moUid, "orgUid":orgUid, "locUid":locUid})) 
    
    
def devicesList(request):
        return render_to_response("monitor/devicesList.html",
                      RequestContext(request, {
                     })) 


def devicesConfigOp(request, moUid):
    dev = Device._loadObj(moUid)
    return render_to_response("monitor/devicesConfigOp.html", RequestContext(request, {"moUid":moUid, "device":dev})) 
    
def configGridIndex(request):
    org=DeviceClass.findByPath("/devicecls/linux")
    loc = Location.getDefault()
    return HttpResponseRedirect( "/monitor/configGrid/%s/%s/" %(org.getUid(), loc.getUid()))
        
def configGrid(request,orgUid, locUid):
    user=UserControl.getUser()
    ownCompany=user.ownCompany
    conditions={"ownCompany":RefDocObject.getRefInfo(ownCompany)}
    usedNum = Device._countObjects(conditions)
    count=user.levelPolicy.deviceCount
    availableNum=count - usedNum
    numDic={"usedNum":usedNum,"count":count,"availableNum":availableNum}
    context=dict(numDic=numDic,orgUid=orgUid,locUid=locUid)
    return render_to_response("monitor/configGrid.html",context) 

def device_adds(request):
        return render_to_response("monitor/device_adds.html", RequestContext(request, {}))

def device_addssusscess(request):
    content = {"error":1,"info":"执行失败","detail":[]}
    return render_to_response("monitor/device_adds_susscess.html", RequestContext(request, content))

def uploadXlsUsersFile(request):

    """
    上传xls文件
    """
    content = {"error":1,"info":"执行失败","detail":[]}
    if request.method == 'POST':
        content = {"error_message":""};
        collector = request.REQUEST.get("collector2")
        deviceclass = request.REQUEST.get("deviceclass")
        if "file" not in  request.FILES :
            content["error_message"] = "文件不能为空"
            return render_to_response("monitor/device_adds.html", RequestContext(request, content))

        uploadFile = request.FILES['file']
        size = uploadFile.size

        if size > 1024 * 1024 * 4:
            content["error_message"] = "上传文件过大(size<=4M)"
            return render_to_response("monitor/device_adds.html", RequestContext(request, content))

        f = _handle_uploaded_file(uploadFile)
        t = {"deviceclass":deviceclass,"collector":collector,"UpLoadFile":f.name}
        api = DeviceApi();
        msg = api.batchFileAddDevice(t)
        content = json.loads(msg)
    return render_to_response("monitor/device_adds_susscess.html", RequestContext(request, content))


def _handle_uploaded_file(f):
    dirName = _p("/nbfiles/temp/") +time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+str(random.randint(0,99))
    with open(dirName + f.name, 'wb+') as info:
        for chunk in f.chunks():
            info.write(chunk)
    return info