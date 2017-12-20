#coding=utf-8
from django.conf.urls.defaults import patterns
from django.http import HttpResponse


def downloadLicenseKey(request, collUid):
    response = HttpResponse(mimetype='application')  
    response['Content-Disposition'] = 'attachment; filename=.license.dat'
    from products.netWebAPI.userApi import UserApi
    sn = UserApi().getCollectorSn(collUid)
    response.write(sn)
    return response
    
urlpatterns = patterns('',
    (r'^downloadLicenseKey/(?P<collUid>\w+)$', downloadLicenseKey),
    
)
