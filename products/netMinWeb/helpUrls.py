#coding=utf-8

from django.conf.urls.defaults import patterns
from django.shortcuts import render_to_response
from django.template import RequestContext

def helpHtml(request, html):
    return render_to_response( "help/%s.html" %html, RequestContext(request, {"pageName":html}))

urlpatterns = patterns('',
    (r'^(?P<html>\w+)\.html$',helpHtml),
)
