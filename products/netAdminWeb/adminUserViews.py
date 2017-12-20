#coding=utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from products.netWebAPI.admin.adminUserApi import AdminUserApi
from products.netUtils.excelParser import ExcelError
from products.netUtils import xutils

from products.netUtils.excelParser import excelParser
from products.netUtils.xutils import nbPath as _p
from products.netBilling.extendDevice import ExtendDevice

def loginPage(request):
    return render_to_response('login.html', RequestContext(request, {"userType": "AdminUser"}))

def customers(request):
    return render_to_response("admin/customers.html", RequestContext(request, {}))

def sendmail(request):
    return render_to_response("admin/sendmail.html", RequestContext(request, {}))

def createAccounts(request):
    return render_to_response("admin/createAccounts.html", RequestContext(request, {}))

def recharge(request):
    return render_to_response("admin/recharge.html", RequestContext(request, {}))

def hasCheckedRecharge(request):
    return render_to_response("admin/checkedRecharge.html", RequestContext(request, {}))
            
def adminOp(request):
    return render_to_response("admin/adminOp.html", RequestContext(request, {}))

def listFeedBackInfos(request):
    adminUserApi=AdminUserApi()
    opinions=adminUserApi.listFeedBackInfos()
    context=dict(opinions=opinions)
    return render_to_response("admin/listFeedBackInfos.html", RequestContext(request, context))


def uploadXlsUsersFile(request):
    
    """
    上传xls文件，并生成创建用户
    """
    content = {"error_message":""}
    content.update({"userType":"AdminUser"})
    if request.method == 'POST':
        if "file" not in  request.FILES :
            content["error_message"] = "文件不能为空"
            return render_to_response("admin/createAccounts.html", RequestContext(request, content))
        
        uploadFile = request.FILES['file']
        size = uploadFile.size
        
        if size > 1024 * 1024 * 2:
            content["error_message"] = "上传文件过大(size<=2M)"
            return render_to_response("admin/createAccounts.html", RequestContext(request, content))
        
        f = _handle_uploaded_file(uploadFile)
        try:
            accountInfos = excelParser(f.name)
        except ExcelError,e:
            content["error_message"] =e.message
            return render_to_response("admin/createAccounts.html", RequestContext(request, content))
        
        api = AdminUserApi()
        api.request = request
        users = api.createAccounts(accountInfos)
        #users = User._findObjects()
        content["users"] = users
    return render_to_response("admin/createAccounts.html", RequestContext(request, content))
   
def _handle_uploaded_file(f):
    dirName = _p("/nbfiles/temp/")
    with open(dirName + f.name, 'wb+') as info:
        for chunk in f.chunks():
            info.write(chunk)
    return info

def listOperationers(request):
    api = AdminUserApi();
    pn = request.REQUEST.get("pageNum", 1)
    pn = int(pn)
    ps=10  
    operationer = request.REQUEST.get("operationer", "")
    
    _operationers = api.getOperationers(operationer = operationer);
    operationers = _operationers[(pn-1)*ps:pn*ps]
    pageInfos = xutils.page(pn, len(_operationers), ps=ps)
    
    context=dict(operationers=operationers, pageInfos=pageInfos) 
        
    return render_to_response("admin/listOperationers.html", RequestContext(request,context))


def getExtendDevices(request):
    status=request.REQUEST.get("status",0)
    if status not in ["0","1"]:status = "0"
    status = int(status)
    pn = request.REQUEST.get("pageNum", "1")
    if not pn:pn=1
    if not (xutils.isOnlyContainNum(pn)):pn="1"
    pn = int(pn)    
    ps = 10
    _eds=ExtendDevice._findObjects({"status":status})
    pageInfos=xutils.page(pn, len(_eds), ps)
    eds=_eds[(pn-1)*ps:pn*ps]
    context=dict(eds=eds,pageInfos=pageInfos)
    return render_to_response("admin/getExtendDevices.html",RequestContext(request, context))

    
    
    
    