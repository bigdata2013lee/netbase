#coding=utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from products.netWebAPI.serviceNoteApi import ServiceNoteApi
from products.netUtils import xutils
from products.netModel.ticket.serviceNote import ServiceNote
from django.http import HttpResponseRedirect
from products.netModel.user.user import User


def loginPage(request):
    return render_to_response('login.html', RequestContext(request, {"userType": "EngineerUser"}))

def customers(request):
    return render_to_response("eng/customers.html", RequestContext(request, {})) 
        

def services(request):
    serviceNoteApi = ServiceNoteApi()
    status = xutils.parseInt(request.REQUEST.get("status", 0), 0)
    sortFiled=request.REQUEST.get("sortFiled", "eventLabel")
    sortType=xutils.parseInt(request.REQUEST.get("sortType",-1), -1)
    
    if sortType not in [1,-1]:sortType=-1
    if sortFiled not in ["eventLabel","monitorObjName","subject","engineer","startTime","endTime"]:sortFiled="eventLabel"
    if sortFiled:sortInfo={sortFiled:int(sortType)}
    if status not in [0,1]:status=0
    
    pn = request.REQUEST.get("pageNum", 1)
    if not (xutils.isOnlyContainNum(pn)):pn=1
    pn = int(pn)
    ps = 10

    rs = serviceNoteApi.getServiceNotes(conditions={"status":status}, sortInfo=sortInfo, skip=(pn-1)*ps, limit=ps)

    pageInfos = xutils.page(pn, rs.get("total"), ps=ps)
    context=dict(notes=rs.get("results"),pageInfos=pageInfos,sortType=sortType)
    return render_to_response("eng/services.html", RequestContext(request, context))

def customerIssues(request):
    return render_to_response("eng/customerIssues.html", RequestContext(request, {}))

def servicesNoteDetail(request):
    serviceNote=ServiceNote._loadObj(request.REQUEST.get("dataId"))
    serviceNoteApi=ServiceNoteApi()
    dialogs=serviceNoteApi.getDialogs(snUid=request.REQUEST.get("dataId"),toJson=False)
    customers=User._findObjects({"engineer":request.user._getRefInfo()})
    context=dict(serviceNote=serviceNote,dialogs=dialogs,customers=customers)
    return render_to_response("eng/servicesNoteDetail.html", RequestContext(request,context))

def postComment(request):
    serviceNoteApi=ServiceNoteApi()
    serviceNoteApi.request = request
    snid=request.REQUEST.get("snUid")
    context=request.REQUEST.get("context")
    status=request.REQUEST.get("status")
    serviceNote={"sid":snid,"status":int(status)}
    if serviceNoteApi.addDialog(snid,context) =="success":serviceNoteApi.changeTicketStatus(serviceNote)
    return HttpResponseRedirect("/engineer/servicesNoteDetail/?dataId=" + snid) 
    