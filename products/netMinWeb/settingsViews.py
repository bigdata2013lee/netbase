#coding=utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from products.netWebAPI.serviceNoteApi import ServiceNoteApi
from products.netModel.ticket.serviceNote import ServiceNote
from django.http import HttpResponseRedirect
from products.netUtils import xutils

#-------------------------------------------------------------------------------------------    
def index(request):
    return render_to_response("settings/settings_index.html", RequestContext(request)) 
    
def alarm(request):
    return render_to_response("settings/alarm.html", RequestContext(request)) 

def services(request):
    if not request.user.engineer: return HttpResponseRedirect("/events/index/")
    serviceNoteApi = ServiceNoteApi() 
    status = xutils.parseInt(request.REQUEST.get("status", 0), 0)
    sortFiled=request.REQUEST.get("sortFiled", "eventLabel")
    sortType=xutils.parseInt(request.REQUEST.get("sortType",-1), -1)
    if sortType not in [1,-1]:sortType=-1
    if sortFiled not in ["eventLabel","monitorObjName","subject","engineer","startTime","endTime"]:sortFiled="eventLabel"
    if sortFiled:sortInfo={sortFiled:int(sortType)}
    if status not in [0,1]:status=0
    if not request.user.engineer:status=1
    pn = request.REQUEST.get("pageNum", 1)
    pn = int(xutils.dealPageNum(pn))
    ps = 10
    rs = serviceNoteApi.getServiceNotes(conditions={"status":status}, sortInfo=sortInfo, skip=(pn-1)*ps, limit=ps)
    pageInfos = xutils.page(pn, rs.get("total"), ps=ps)
    context=dict(notes=rs.get("results"),pageInfos=pageInfos,sortType=sortType)
    return render_to_response("settings/services.html", RequestContext(request, context)) 
    
def collector(request):
    return render_to_response("settings/collector_index.html", RequestContext(request))

def userBilling(request):
    return render_to_response("settings/userBilling_index.html", RequestContext(request))

def servicesNoteDetail(request):
    serviceNote=ServiceNote._loadObj(request.REQUEST.get("dataId"))
    serviceNoteApi=ServiceNoteApi()
    dialogs=serviceNoteApi.getDialogs(snUid=request.REQUEST.get("dataId"),toJson=False)
    context=dict(serviceNote=serviceNote,dialogs=dialogs)
    return render_to_response("settings/servicesNoteDetail.html", RequestContext(request,context))

def editAudit(request):
    return render_to_response("settings/userBilling_index.html", RequestContext(request))

def postComment(request):
    serviceNoteApi=ServiceNoteApi()
    serviceNoteApi.request = request
    snid=request.REQUEST.get("snUid")
    context=request.REQUEST.get("context")
    serviceNoteApi.addDialog(snid,context)
    return HttpResponseRedirect("/settings/servicesNoteDetail/?dataId=" + snid) 
