#coding=utf-8

from django.conf.urls.defaults import patterns
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from products.netModel.org.location import Location




def  locIndex(request, orgUid=None):
    if not orgUid:
        loc = Location.getDefault()
        orgUid = loc.getUid()

    return render_to_response( "location/cls_index.html", RequestContext(request, {"orgUid":orgUid}))


def  location_index(request):
    
    locDefault = Location.getDefault()
    orgUid = locDefault.getUid()
    return HttpResponseRedirect( "/location/loc/%s" %orgUid)
        


urlpatterns = patterns('',
    (r'^$',location_index),
    (r'^index/$',location_index),
    (r'^loc/(?P<orgUid>\w+)/$', locIndex),

)
