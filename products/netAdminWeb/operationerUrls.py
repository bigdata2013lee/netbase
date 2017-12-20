#coding=utf-8
'''
time:2014-12-23
@version: netbase4.0
@author: julian
'''
import re
import datetime
from products.netUtils import xutils
from django.template import RequestContext
from django.conf.urls.defaults import patterns
from products.netCommunity.share import Share
from django.shortcuts import render_to_response
from products.netCommunity.question import Question
from products.netAdminWeb.userLocal import UserLocal
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from products.netPublicModel.userControl import UserControl
from products.netWebAPI.serviceNoteApi import ServiceNoteApi
from products.netWebAPI.communityApi.topicApi import TopicApi
from products.netWebAPI.admin.operationApi import OperationApi

_userType="Operationer"

def remenberLoginPath(loginFun):
    def xfun(*v, **kw):
        response = loginFun(*v, **kw)
        dt = datetime.datetime.now() + datetime.timedelta(hours = int(24))
        response.set_cookie("remenber_login_path","/operation/",expires=dt)
        return response
    return xfun
        
@remenberLoginPath
def view_login(request):
    "系统用户登入"
    userType=_userType
    UserLocal.setUserType(userType)
    
    
    user = authenticate(username=request.REQUEST.get("username"), password=request.REQUEST.get("password"))
    message = {}
    message["userType"] = userType
    if user is not None:
            if not user.is_active:
                message["message_info"] = "您的账户未激活！"
                return render_to_response( "login.html", RequestContext(request, message))
            user.id = user.getUid()

            login(request, user)
            
            request.session['userType'] = userType
            return HttpResponseRedirect("/operation/serviceUsers/")
    
    if request.method == "POST":
        message["message_info"] = "用户名或密码错误，原因可能是:忘记密码!"
    return render_to_response("login.html",RequestContext(request, message))

def view_loginout(request):
    logout(request)
    return HttpResponseRedirect("/operation/")


def  loginPage(request):
    return render_to_response('login.html', RequestContext(request, {"userType": "Operationer"}))

def serviceUsers(request):
    '''
    time:2014-12-23
    @author: julian
    @todo: 服务客户视图函数
    @param request: request对象
    @return: serviceUsers.html页面
    '''
    #获取服务客户列表和收藏客户列表，并进行分页
    operationer=UserControl.getUser()
    operationApi = OperationApi()
    ps = 10
    fpn = xutils.dealPageNum(request.REQUEST.get("fpageNum",1))
    cpn = xutils.dealPageNum(request.REQUEST.get("cpageNum",1))
    _serviceCustomers = operationApi.listServiceCustomers(conditions={},sortInfo=None,skip=(cpn-1)*ps,limit=ps)
    serviceCustomers=_serviceCustomers["result"]
    _favoriteCustomers = operationApi.listFavoriteCustomers(conditions={},sortInfo=None,skip=(fpn-1)*ps,limit=ps)
    favoriteCustomers = _favoriteCustomers["result"]
    cpageInfos=xutils.page(cpn, _serviceCustomers["total"], ps)
    fpageInfos=xutils.page(fpn, _favoriteCustomers["total"], ps)
    
    #获取运营商的工程师和可用的设备
    engineers = operationApi.getOperationerEngineers()
    deviceAvailable=operationApi.getAvailableDevice(operationer)
    
    #构造context字典，并返回html页面
    context=dict(serviceCustomers=serviceCustomers, engineers=engineers,fpageInfos=fpageInfos,
                 favoriteCustomers=favoriteCustomers,deviceAvailable=deviceAvailable,cpageInfos=cpageInfos)
    return render_to_response('operation/serviceUsers.html', RequestContext(request,context))

def favoriteCustomers(request):
    '''
    time:2014-12-23
    @author: julian
    @todo: 收藏客户视图函数
    @param request: request对象
    @return: favoriteCustomers.html页面    
    '''
    #获取收藏客户列表，并进行分页
    operationApi = OperationApi()
    pn = request.REQUEST.get("pageNum", 1)
    pn = xutils.dealPageNum(pn)
    ps=10
    companyName = request.REQUEST.get("companyName", "")
    _favoriteCustomers = operationApi.searchFavoriteCustomers(companyName=companyName)
    favoriteCustomers = _favoriteCustomers[(pn-1)*ps:pn*ps]
    pageInfos = xutils.page(pn, len(_favoriteCustomers), ps=ps)
    
    #构造context字典，并返回html页面
    context=dict(favoriteCustomers=favoriteCustomers, pageInfos=pageInfos) 
    return render_to_response('operation/favoriteCustomers.html', RequestContext(request,context))

def searchCustomers(request):
    '''
    time:2014-12-23
    @author: julian
    @todo: 搜索客户视图函数
    @param request: request对象
    @return: searchCustomers.html页面    
    '''
    #获取客户列表，并进行分页    
    conditions={}
    operationApi=OperationApi()
    email = request.REQUEST.get("email","")
    if email != "":
        conditions={"email":re.compile(email,re.IGNORECASE)}  
    pn = request.REQUEST.get("pageNum","1")
    pn = xutils.dealPageNum(pn)
    ps = 10
    cust=operationApi.searchCustomers(conditions=conditions, sortInfo=None, skip=(pn-1)*ps, limit=ps)
    pageInfos=xutils.page(pn, cust.get("total"), ps) 
    
    #构造context字典，并返回html页面    
    context=dict(customers=cust.get("results"),pageInfos=pageInfos)  
    return render_to_response("operation/searchCustomers.html",RequestContext(request,context))

def engineers_management(request):
    '''
    time:2014-12-23
    @author: julian
    @todo: 工程师管理视图函数
    @param request: request对象
    @return: engineersManagement.html页面    
    '''
    #获取工程师列表     
    operationApi = OperationApi()
    engineers = operationApi.getOperationerEngineers()
    
    #构造context字典，并返回html页面     
    context=dict(engineers=engineers)
    return render_to_response('operation/engineersManagement.html', RequestContext(request,context))

def operationerPersonal(request):  
    '''
    time:2014-12-23
    @author: julian
    @todo: 工程师管理视图函数
    @param request: request对象
    @return: engineersManagement.html页面    
    '''    
    operationer = UserControl.getUser()
    context=dict(operationer=operationer)
    return render_to_response('operation/operationerPersonal.html', RequestContext(request,context))

def contractCenter(request):
    '''
    time:2014-12-23
    @author: julian
    @todo: 合约服务视图函数
    @param request: request对象
    @return: contractCenter.html页面
    '''
    operationer = UserControl.getUser()
    deviceTotal={"host":0,"website":0,"network":0}
    deviceUsed={"host":0,"website":0,"network":0}
    deviceAvailable={"host":0,"website":0,"network":0}
    if operationer.levelPolicy:
        deviceTotal["host"]=operationer.levelPolicy.deviceCount
        deviceTotal["website"]=operationer.levelPolicy.websiteCount
        deviceTotal["network"]=operationer.levelPolicy.networkCount
    if operationer.deviceDtail:
        deviceUsed["host"]=operationer.deviceDtail.deviceCount
        deviceUsed["website"]=operationer.deviceDtail.websiteCount
        deviceUsed["network"]=operationer.deviceDtail.networkCount
    deviceAvailable["host"]=deviceTotal["host"]-deviceUsed["host"]
    deviceAvailable["website"]=deviceTotal["website"]-deviceUsed["website"]
    deviceAvailable["network"]=deviceTotal["network"]-deviceUsed["network"]
    context=dict(operationer=operationer,deviceTotal=deviceTotal,deviceUsed=deviceUsed,deviceAvailable=deviceAvailable)
    return render_to_response('operation/contractCenter.html', RequestContext(request,context))

def customerQuestions(request):
    context=dict()
    return render_to_response('operation/customerQuestions.html', RequestContext(request,context))

def searchQuestions(request):
    topicApi=TopicApi()
    
    pn = request.REQUEST.get("pageNum", 1)
    pn = xutils.dealPageNum(pn)
    ps = 20
    
    keywords = request.REQUEST.get("keywords")
    d0 = request.REQUEST.get("d0")
    d1 = request.REQUEST.get("d1")
    fields = request.REQUEST.get("fields","")
    fields = fields.strip()
    _fields=[]
    if(fields):_fields=fields.split(",")
    
    
    searchResult = topicApi.searchQuestions(text=keywords, area={"d0":d0,"d1":d1},
                                            fields=_fields,sortInfo={"replyNum":-1},skip=(pn-1)*ps ,limit=ps)
    pageInfos = xutils.page(pn, searchResult.get("total",0), ps=ps)

    context=dict(searchResult=searchResult, pageInfos=pageInfos, topicType="Question")
    return render_to_response("operation/search_results.html", RequestContext(request, context))
    
def viewQuestion(request, questionId):
    topic=Question._loadObj(questionId)
    sortFiled = request.REQUEST.get("sort", "ctime")
    if  sortFiled not in ["approveNum","ctime"]: sortFiled = "approveNum"
    sortInfo={sortFiled:-1}
    pn = request.REQUEST.get("pageNum", 1)
    pn = xutils.dealPageNum(pn)
    ps = 20
    ptotal=topic.replyNum
    commentList=topic.getComments(sortInfo=sortInfo, skip=(pn-1)*ps,  limit=ps)
    pageInfos = xutils.page(pn, ptotal, ps=ps)
    context=dict(commentList=commentList,topic=topic,pageInfos=pageInfos)
    return render_to_response("operation/viewQuestion.html", RequestContext(request, context))


def viewShare(request, shareId):
    topic=Share._loadObj(shareId)
    sortFiled = request.REQUEST.get("sort", "ctime")
    if  sortFiled not in ["approveNum","ctime"]: sortFiled = "approveNum"
    sortInfo={sortFiled:-1}
    pn = request.REQUEST.get("pageNum", 1)
    pn = xutils.dealPageNum(pn)
    ps = 20
    
    ptotal=topic.replyNum
    commentList=topic.getComments(sortInfo=sortInfo, skip=(pn-1)*ps,  limit=ps)
    
    pageInfos = xutils.page(pn, ptotal, ps=ps)
    context=dict(commentList=commentList,topic=topic,pageInfos=pageInfos)
    return render_to_response("operation/viewShare.html", RequestContext(request, context))


def myShare(request):
    topicApi=TopicApi()
    myShares = topicApi.listShares()
    context=dict(myShares=myShares)
    return render_to_response("operation/myShare.html", RequestContext(request, context))
    
def showServiceCustomers(request, engineerId):
    operationApi = OperationApi()
    custormers = operationApi.showServiceCustomers(engineerId=engineerId)
    context=dict(custormers=custormers)
    return render_to_response("operation/listEngServiceCustomers.html", RequestContext(request, context))

def listServiceNotes(request):
    serviceNoteApi = ServiceNoteApi()
    status = xutils.parseInt(request.REQUEST.get("status", 0), 0)
    sortFiled=request.REQUEST.get("sortFiled", "startTime")
    sortType=xutils.parseInt(request.REQUEST.get("sortType",-1), -1)
    if sortType not in [1,-1]:sortType=-1
    if sortFiled not in ["subject","eventLabel","monitorObjName","content","engineer","startTime","endTime","emergencyDegree"]:sortFiled="startTime"
    sortInfo = {sortFiled:sortType}
    if status not in [0,1]:status=0
    pn = request.REQUEST.get("pageNum", 1)
    pn = xutils.dealPageNum(pn)
    ps = 10
    rs = serviceNoteApi.getServiceNotes(conditions={"status":status}, sortInfo=sortInfo, skip=(pn-1)*ps, limit=ps)
    pageInfos = xutils.page(pn, rs.get("total"), ps=ps)
    context=dict(notes=rs.get("results"),pageInfos=pageInfos,sortType=sortType)
    return render_to_response("operation/listSeviceNotes.html", RequestContext(request, context)) 


def downloadServiceNotesFile(request):
    serviceNoteApi = ServiceNoteApi()
    status = xutils.parseInt(request.REQUEST.get("status", 0), 0)
    sortFiled=request.REQUEST.get("sortFiled", "startTime")
    sortType=xutils.parseInt(request.REQUEST.get("sortType",-1), -1)
    if sortType not in [1,-1]:sortType=-1
    if sortFiled not in ["subject","eventLabel","monitorObjName","content","engineer","startTime","endTime","emergencyDegree"]:sortFiled="startTime"
    sortInfo = {sortFiled:sortType}
    if status not in [0,1]:status=0    
    csvfile = serviceNoteApi.checkoutServiceNotesAsCVS(conditions={"status":status}, sortInfo=sortInfo)
    csvfile.seek(0)
    data = csvfile.read()
    csvfile.close()
    
    response = HttpResponse(data,mimetype='application/octet-stream') 
    response['Content-Disposition'] = 'attachment; filename=service_notes.csv'
    return response
    
def downloadAppraisementsFile(request):
    serviceNoteApi=ServiceNoteApi()
    sortFiled=request.REQUEST.get("sortFiled", "startTime")
    sortType=xutils.parseInt(request.REQUEST.get("sortType",-1), -1)
    if sortType not in [1,-1]:sortType=-1
    if sortFiled not in ["engineer","appraisement.good","appraisement.common","appraisement.bad","goodRate"]:sortFiled="engineer"
    sortInfo={sortFiled:int(sortType)} 
    csvfile = serviceNoteApi.checkoutAppraisementsAsCVS(sortInfo,conditions={})
    csvfile.seek(0)
    data = csvfile.read()
    csvfile.close()
    response = HttpResponse(data,mimetype='application/octet-stream') 
    response['Content-Disposition'] = 'attachment; filename=Appraisements_file.csv'
    return response


def downloadEngAppraisementsFile(request):
    serviceNoteApi=ServiceNoteApi()
    engId = request.REQUEST.get("engId","")
    sortFiled=request.REQUEST.get("sortFiled", "endTime")
    sortType=xutils.parseInt(request.REQUEST.get("sortType",-1), -1)
    if sortType not in [1,-1]:sortType=-1    
    if sortFiled not in ["endTime","serviceNote","user","engineer","attitude","techLevel","responseSpeed","appraiseContent"]:sortFiled="endTime"
    if not engId:return "warn:无法获得工程师对象"
    sortInfo={sortFiled:int(sortType)} 
    csvfile = serviceNoteApi.checkoutEngAppraisementsAsCVS(engId,sortInfo)
    csvfile.seek(0)
    data = csvfile.read()
    csvfile.close()
    response = HttpResponse(data,mimetype='application/octet-stream') 
    response['Content-Disposition'] = 'attachment; filename=EngAppraisements_file.csv'
    return response

    
def listAppraisements(request):
    serviceNoteApi=ServiceNoteApi()
    sortFiled=request.REQUEST.get("sortFiled", "username")
    sortType=request.REQUEST.get("sortType","-1")
    if sortType not in ["1","-1"]:sortType="-1"
    if sortFiled not in ["username","appraisement.good","appraisement.common","appraisement.bad","goodRate"]:sortFiled="username"
    conditions={"operationer":UserControl.getUser()._getRefInfo()}
    if sortFiled:sortInfo={sortFiled:int(sortType)} 
    pn = request.REQUEST.get("pageNum", "1")
    pn = xutils.dealPageNum(pn)
    ps = 10
    _engs=serviceNoteApi.getAppraisements(conditions=conditions,sortInfo=sortInfo)
    if (pn-1) > len(_engs)/ps:pn=1
    engs=_engs[(pn-1)*ps:pn*ps]
    pageInfos = xutils.page(pn, len(_engs), ps=ps)
    context=dict(engs=engs,pageInfos=pageInfos,sortType=sortType)
    return render_to_response("operation/listAppraisements.html", RequestContext(request, context))

def listEngAppraisements(request):
    serviceNoteApi=ServiceNoteApi()
    sortFiled=request.REQUEST.get("sortFiled", "serviceNote")
    sortType=request.REQUEST.get("sortType","-1")
    if sortType not in ["1","-1"]:sortType="-1"    
    if sortFiled not in ["serviceNote.endTime","serviceNote","user","engineer","attitude","techLevel","responseSpeed","appraiseContent"]:sortFiled="serviceNote"
    if sortFiled:sortInfo={sortFiled:int(sortType)} 
    pn = request.REQUEST.get("pageNum", "1")
    engId=request.REQUEST.get("engId")
    if not engId:return "warn:无法获得工程师对象"
    pn = xutils.dealPageNum(pn)
    ps = 10
    _apts=serviceNoteApi.getEngineerAppr(engId,sortInfo)
    if (pn-1) > len(_apts)/ps:pn=1
    apts=_apts[(pn-1)*ps:pn*ps]
    pageInfos = xutils.page(pn, len(_apts), ps=ps)    
    context=dict(apts=apts,pageInfos=pageInfos)
    return render_to_response("operation/listEngAppraisements.html",RequestContext(request, context))

    
urlpatterns = patterns('',
    (r'^login/$',view_login),
    (r'^logout/$',view_loginout),
    (r'^serviceUsers/$',serviceUsers), 
    (r'^favoriteCustomers/$',favoriteCustomers),
    (r'^searchCustomers/$',searchCustomers),
    (r'^engineers_management/$',engineers_management),
    (r'^operationerPersonal/$',operationerPersonal),
    (r'^contractCenter/$',contractCenter),
    (r'^customerQuestions/$',customerQuestions),
    (r'^searchQuestions/$',searchQuestions),
    (r'^viewQuestion/(?P<questionId>\w+)/$',viewQuestion),
    (r'^viewShare/(?P<shareId>\w+)/$',viewShare),
    (r'^myShare/$',myShare),
    (r'^listServiceNotes/$',listServiceNotes),
    (r'^listAppraisements/$',listAppraisements),
    (r'^listEngAppraisements/$',listEngAppraisements),
    (r'^showServiceCustomers/(?P<engineerId>\w+)/$',showServiceCustomers),
    (r'^downloadServiceNotesFile/$',downloadServiceNotesFile),
    (r'^downloadAppraisementsFile/$',downloadAppraisementsFile),
    (r'^downloadEngAppraisementsFile/$',downloadEngAppraisementsFile),
    (r'^$',loginPage),
)
