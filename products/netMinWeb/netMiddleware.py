#coding=utf-8

from django.contrib import auth
from django.utils.functional import SimpleLazyObject
from django.http import HttpResponseRedirect
from threading import local
from products.netAdminWeb.userLocal import UserLocal
from products.netPublicModel.userControl import UserControl
from products.netModel.operation.operationer import Operationer
from products.netModel.user.user import User
from products.netModel.baseModel import RefDocObject
from products.netModel.device import Device
from products.netModel.website import Website
from products.netModel.network import Network
from products.netBilling.levelPolicy import LevelPolicy
from products.netModel.operation.deviceDtail import DeviceDtail

_admin_user_local = local()

def get_user(request):
    if not hasattr(request, '_cached_user'):
        request._cached_user = auth.get_user(request)
    return request._cached_user



class AuthenticationMiddleware(object):
    
    def _anonymousUserAllowPath(self, path):
        "匿名用户可否进入某路径"
        allowPathList = ["/remote/UserApi/checkEmail/", "/favicon.ico", "/index","/accounts/", "/outsite/",
                         "/admin/index/", "/media/","/help/", "/feedback/","/getVerifyCode/", "/getPhoneVerifyCode/",
                         "/login.html",
                         "/remote/ServiceNoteApi/addAttachment","/ucenter/searchShares/",
                         "/ucenter/communityAnonymous/","/ucenter/viewQuestion/","/ucenter/viewShare/",
                         "/remote/TopicApi/getNewMessageNum/","/ucenter/searchQuestions/","/reportOpinion/"]

        if  path == "/": return True
        for allowPath in allowPathList:
            if path.find(allowPath) == 0: return True
        
        return False
    
    
        
    def _FS_UserAllowPath(self, path):
        "免费版标准版用户可否进入某路径"
        notAllowPathList = []
        #notAllowPathList = ["/location/", "/network/","/remote/NetworkApi/","/remote/LocationApi/"]
        for notAllowPath in notAllowPathList:
            if path.find(notAllowPath) == 0: return False
        
        return True
    
    def _EC_UserAllowPath(self, path):
        "企业版自定版用户可否进入某路径"
        notAllowPathList = []
        for notAllowPath in notAllowPathList:
            if path.find(notAllowPath) == 0: return False
        return True      
    
    def _allowEnterAdvPath(self, u, path):
        if u.levelPolicy.getUid() in  ["free", "standard"]: return False
        allowList = ["/location", "/network"]
        for urlPre in allowList:
            if path.find(urlPre) == 0: return True
        
        return False
    
    def process_request(self, request):
        assert hasattr(request, 'session'), "The Django authentication middleware requires session middleware to \
        be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."

        u = request.user = SimpleLazyObject(lambda: get_user(request))
        #userType = UserLocal.getUserType()
        userType = request.session.get('userType', None)
        UserLocal.setUserType(userType)
        #print "url:%s" %request.path
        if str(u) == "AnonymousUser":
            if not self._anonymousUserAllowPath(request.path):
                print "匿名用户不能进入路径: %s" %request.path
                return HttpResponseRedirect("/index/")
#        else:
#            if u.levelPolicy.getUid() in  ["free", "standard"] and  not self._FS_UserAllowPath(request.path):
#                print "免费版\标准版用户不能进入路径: %s" %request.path
#                return HttpResponseRedirect("/index/")
#            
#            elif u.levelPolicy.getUid() in  ["enterprise", "customization"] and  not self._EC_UserAllowPath(request.path):
#                print "企业版\自定版用户不能进入路径: %s" %request.path
#                return HttpResponseRedirect("/index/")
                
                
            
                
        if u and str(u) != "AnonymousUser":
            UserControl.setUser(u)
            
        
            
            
            
            