#coding=utf-8

from django.conf.urls.defaults import patterns
from django.shortcuts import render_to_response
from django.template import RequestContext
from products.netswgl.webApi.swglApi import SwglApi
import json
from products.netswgl.model.sEngineer import SEngineer
from django.http import HttpResponseRedirect
from products.netswgl.model.feedback import SEngineerFeedback


def swglHtml(request, html):
    return render_to_response( "swgl/%s.html" %html, RequestContext(request, {"pageName":html}))


def search(request):
    swglApi = SwglApi()
    
    params = request.REQUEST.get("params", "{}")
    _ps = json.loads(params)
    limit = 10
    d0 = _ps.get("d0","")
    d1 = _ps.get("d1","")
    r0 = _ps.get("r0","")
    r1 = _ps.get("r1","")
    keywords = _ps.get("keywords","")
    sortField = _ps.get("sortField","")
    sortDir = int(_ps.get("sortDir",-1))
    pn = int(_ps.get("pageNum",1))
    skip = (pn - 1) * limit

    rs = swglApi.searchSEngineers(d0, d1, r0, r1, keywords, sortField, sortDir, skip, limit)
    
    from products.netUtils import xutils
    pager = xutils.page(pn, rs.get("total"), limit)
    return render_to_response( "swgl/search_list.html", RequestContext(request, {"rs":rs, "pager":pager}))
    
    
    
def favortes(request):
    swglApi = SwglApi()
    favortSengs = swglApi.favortes()
    return render_to_response( "swgl/favortes.html", RequestContext(request, {"favortSengs":favortSengs}))


def removeFavort(request, uid):
    swglApi = SwglApi()
    swglApi.removeFavort(uid)
    return HttpResponseRedirect("/swgl/favortes/")
    
        
def viewSEngineer(request, uid):
    swglApi = SwglApi()
    seng = SEngineer._loadObj(uid)
    feedbacks=[]
    serviceProvider={}
    allowFeedback=False
    allowReport=False
    if seng:
        feedbacks = seng._getRefMeObjects("sEngineer", SEngineerFeedback, sortInfo={"fbTime":-1}, limit=20)
        serviceProvider = seng.ownServiceProvider
        allowFeedback = swglApi.allowFeedbackSEngineer(uid)
        allowReport = swglApi.allowReportSEngineer(uid)
        
    return render_to_response( "swgl/sengineer.html", RequestContext(request, {
                            "seng":seng, 
                            "feedbacks":feedbacks, 
                            "serviceProvider":serviceProvider,
                            "allowFeedback":allowFeedback,
                            "allowReport":allowReport
            }))        
    

def feedbackSEngineer(request, uid):

    selects=[]
    selects.append(request.REQUEST.get("warmHeart", "warmHeart"))
    selects.append(request.REQUEST.get("technical", "technical"))
    selects.append(request.REQUEST.get("solve", "solve"))
    selects.append(request.REQUEST.get("timeEfficient", "timeEfficient"))
    
    summary = request.REQUEST.get("summary", "")
    swglApi = SwglApi()
    swglApi.feedbackSEngineer(uid, selects, summary)
    
    
    return HttpResponseRedirect("/swgl/viewseng/%s" %uid)
    
def reportSEngineer(request, uid):
    reason = request.REQUEST.get("reason", "1")
    summary = request.REQUEST.get("summary", "")
    swglApi = SwglApi()
    swglApi.reportSEngineer(uid, reason, summary)
    
    return HttpResponseRedirect("/swgl/viewseng/%s" %uid)

#-----------------------------------------------------------------------------------------------    
urlpatterns = patterns('',
    (r'^(?P<html>\w+)\.html$',swglHtml),
    (r'^search$', search),
    (r'^favortes', favortes),
    (r'^viewseng/(?P<uid>\w+)$', viewSEngineer),
    (r'^feedbackseng/(?P<uid>\w+)$', feedbackSEngineer),
    (r'^reportseng/(?P<uid>\w+)$', reportSEngineer),
    (r'^removeFav/(?P<uid>\w+)$', removeFavort),
    
)
