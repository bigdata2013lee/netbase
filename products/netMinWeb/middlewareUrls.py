#coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.conf.urls.defaults import patterns
from products.netWebAPI.middlewareApi import MiddlewareApi
from products.netModel.middleware.mwNginx import MwNginx
from products.netModel.middleware.mwApache import MwApache
from products.netModel.middleware.mwTomcat import MwTomcat

#---------------------------------------------------------------------------------------------------
def listNginx(request):
    mwApi = MiddlewareApi()
    mwClsCounts = mwApi.middlewareClsCounts()
    wms = mwApi.listNginxs()
    context=dict(mwClsCounts=mwClsCounts, wms=wms, pageName="nginx_list")
    return render_to_response("middleware/nginx_list.html", RequestContext(request, context)) 


def addNginx(request):
    mwApi = MiddlewareApi()
    mwClsCounts = mwApi.middlewareClsCounts()
    context=dict(mwClsCounts=mwClsCounts)
    return render_to_response("middleware/nginx_add.html", RequestContext(request, context)) 

def editNginx(request, uid):
    mwApi = MiddlewareApi()
    mwClsCounts = mwApi.middlewareClsCounts()
    mw = MwNginx._loadObj(uid)
    context=dict(moUid=uid, mw=mw, mwClsCounts=mwClsCounts)
    return render_to_response("middleware/nginx_conf.html", RequestContext(request, context)) 

def viewNginx(request, uid):
    mwApi = MiddlewareApi()
    mw = MwNginx._loadObj(uid)
    context=dict(moUid=uid, mw=mw)
    return render_to_response("middleware/nginx_detail.html", RequestContext(request, context)) 


def delNginx(request, uid):
    MiddlewareApi().removeNginx(uid)
    return HttpResponseRedirect("/middleware/nginx_list/")


#---------------------------------------------------------------------------------------------------
def listApache(request):
    mwApi = MiddlewareApi()
    mwClsCounts = mwApi.middlewareClsCounts()
    wms = mwApi.listApaches()
    context=dict(mwClsCounts=mwClsCounts, wms=wms, pageName="apache_list")
    return render_to_response("middleware/apache_list.html", RequestContext(request, context)) 


def addApache(request):
    mwApi = MiddlewareApi()
    mwClsCounts = mwApi.middlewareClsCounts()
    context=dict(mwClsCounts=mwClsCounts)
    return render_to_response("middleware/apache_add.html", RequestContext(request, context)) 


def editApache(request, uid):
    mwApi = MiddlewareApi()
    mwClsCounts = mwApi.middlewareClsCounts()
    mw = MwApache._loadObj(uid)
    context=dict(moUid=uid, mw=mw, mwClsCounts=mwClsCounts)
    return render_to_response("middleware/apache_conf.html", RequestContext(request, context)) 


def viewApache(request, uid):
    mwApi = MiddlewareApi()
    mw = MwApache._loadObj(uid)
    context=dict(moUid=uid, mw=mw)
    return render_to_response("middleware/apache_detail.html", RequestContext(request, context)) 


def delApache(request, uid):
    MiddlewareApi().removeApache(uid)
    return HttpResponseRedirect("/middleware/apache_list/")

#---------------------------------------------------------------------------------------------------
def listTomcat(request):
    mwApi = MiddlewareApi()
    mwClsCounts = mwApi.middlewareClsCounts()
    wms = mwApi.listTomcats()
    context=dict(mwClsCounts=mwClsCounts, wms=wms, pageName="tomcat_list")
    return render_to_response("middleware/tomcat_list.html", RequestContext(request, context)) 


def addTomcat(request):
    mwApi = MiddlewareApi()
    mwClsCounts = mwApi.middlewareClsCounts()
    context=dict(mwClsCounts=mwClsCounts)
    return render_to_response("middleware/tomcat_add.html", RequestContext(request, context)) 

def editTomcat(request, uid):
    mwApi = MiddlewareApi()
    mwClsCounts = mwApi.middlewareClsCounts()
    mw = MwTomcat._loadObj(uid)
    context=dict(moUid=uid, mw=mw, mwClsCounts=mwClsCounts)
    return render_to_response("middleware/tomcat_conf.html", RequestContext(request, context)) 

def viewTomcat(request, uid):
    mw = MwTomcat._loadObj(uid)
    context=dict(moUid=uid, mw=mw)
    return render_to_response("middleware/tomcat_detail.html", RequestContext(request, context)) 

def delTomcat(request, uid):
    MiddlewareApi().removeTomcat(uid)
    return HttpResponseRedirect("/middleware/tomcat_list/")

#---------------------------------------------------------------------------------------------------

urlpatterns = patterns('',
    (r"^nginx_list/$", listNginx),
    (r"^nginx_add/$", addNginx),
    (r"^nginx_edit/(?P<uid>\w+)/$", editNginx),
    (r"^nginx_view/(?P<uid>\w+)/$", viewNginx),
    (r"^nginx_del/(?P<uid>\w+)/$", delNginx),
    
    (r"^apache_list/$", listApache),
    (r"^apache_add/$", addApache),
    (r"^apache_edit/(?P<uid>\w+)/$", editApache),
    (r"^apache_view/(?P<uid>\w+)/$", viewApache),
    (r"^apache_del/(?P<uid>\w+)/$", delApache),
    
    (r"^tomcat_list/$", listTomcat),
    (r"^tomcat_add/$", addTomcat),
    (r"^tomcat_edit/(?P<uid>\w+)/$", editTomcat),
    (r"^tomcat_view/(?P<uid>\w+)/$", viewTomcat),  
    (r"^tomcat_del/(?P<uid>\w+)/$", delTomcat),
    
)
