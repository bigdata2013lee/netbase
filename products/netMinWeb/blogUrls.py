#coding=utf-8

from django.conf.urls.defaults import patterns
from django.shortcuts import render_to_response
from django.template import RequestContext


def index(request):
    return render_to_response( "outsite/blog/list.html", RequestContext(request, {}))

def blogHtml(request, html):
    return render_to_response( "outsite/blog/%s.html" %html, RequestContext(request, {"pageName":html}))

urlpatterns = patterns('',
    (r'^(?P<html>\w+)\.html$',blogHtml),
)
