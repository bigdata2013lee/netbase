#coding=utf-8
from settings import MEDIA_ROOT
from django.conf.urls.defaults import patterns, include, url
from django.http import HttpResponseRedirect
from products.netWebAPI.adminApiView import remoteView 
import os

def default_site_page(request):
    defaultBasePath = "/engineer/"
    basePath = request.COOKIES.get("remenber_login_path",defaultBasePath)
    return HttpResponseRedirect(basePath)

    
def index(request):
    return default_site_page(request)


urlpatterns = patterns('',
    (r'^remote/(?P<apiClsName>\w*)/(?P<methodName>[a-zA-Z]+\w*)/', remoteView),
    (r'media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
    (r'downloads/(?P<path>.*)$', 'django.views.static.serve', {'document_root': "%s/nbfiles/upload/" %os.environ["NBHOME"]}),
    url(r'^engineer/', include('netAdminWeb.engineerUrls')),
    url(r'^operation/', include('netAdminWeb.operationerUrls')),
    url(r'^sale/', include('netAdminWeb.saleUrls')),
    url(r'^admin/', include('netAdminWeb.adminUserUrls')),
    (r'^index/', index),
    (r'^$', default_site_page),
)
