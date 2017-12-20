#coding=utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf.urls.defaults import patterns


def customerMap(request):
    return render_to_response( "customMap/customerMap.html", RequestContext(request, {}))

def editMap(request, mcUid):
    return render_to_response( "customMap/index.html", RequestContext(request, {"mcUid":mcUid}))

def viewMap(request, mcUid):
    return render_to_response( "customMap/view.html", RequestContext(request, {"mcUid":mcUid}))




urlpatterns = patterns('',
    (r'^index/$', customerMap),
    (r'^customerMap/$', customerMap),
    (r'^customerMap/edit/(?P<mcUid>\w+)/$', editMap),
    (r'^customerMap/view/(?P<mcUid>\w+)/$', viewMap),
)
