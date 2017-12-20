#coding=utf-8

from django.contrib import auth
from django.utils.functional import SimpleLazyObject
from django.http import HttpResponseRedirect
from threading import local
from products.netAdminWeb.userLocal import UserLocal
from products.netPublicModel.userControl import UserControl
import re

_admin_user_local = local()

def get_user(request):
    if not hasattr(request, '_cached_user'):
        request._cached_user = auth.get_user(request)
    return request._cached_user



class AuthenticationMiddleware(object):

    def _anonymousUserAllowPath(self, path):
        "匿名用户可否进入某路径"
        allowPathList = [r"^/favicon\.ico$", r"^/index/$",r"/account/.+$",
                     r"/engineer/$", r"/engineer/index/$", r"/engineer/login/$", 
                     r"/sale/",r"/sale/index/$", r"/sale/login/$", 
                     r"/admin/$",r"/admin/index/$", r"/admin/login/$", 
                     
                     r"/operation/$",r"/operation/login/$", 
                     
                     r"^/media/.+",r"^/help/.+", r"^/remote/ServiceNoteApi/addAttachment"]
        for allowPath in allowPathList:
            if re.search(allowPath, path): return True
        
        return False

    
    def process_request(self, request):
        assert hasattr(request, 'session'), "The Django authentication middleware requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."

        u = request.user = SimpleLazyObject(lambda: get_user(request))
        #userType = UserLocal.getUserType()
        userType = request.session.get('userType', None)
        UserLocal.setUserType(userType)
        if str(u) == "AnonymousUser" and not self._anonymousUserAllowPath(request.path):
            print "AnonymousUser can't enter path: %s" %request.path
            return HttpResponseRedirect("/index/")
            
        if u and str(u) != "AnonymousUser":
            UserControl.setUser(u)
            
            
            