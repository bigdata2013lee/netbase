#coding=utf-8
import saleViews
from django.conf.urls.defaults import patterns
from products.netAdminWeb.userLocal import UserLocal
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
_userType="SaleUser"

def view_login(request):
    "系统用户登入"
    userType=_userType
    UserLocal.setUserType(userType)
    
    user = authenticate(username=request.REQUEST.get("username"), password=request.REQUEST.get("password"))
    message = {}
    message["userType"] = userType
    if user is not None:
            if not user.is_active:
                message["message_info"] = "您的账户未激活！"
                return render_to_response( "login.html", RequestContext(request, message)
            )
            user.id = user.getUid()
            ret = login(request, user)
            
            request.session['userType'] = userType
            return HttpResponseRedirect("/sale/customers/")
    if request.method == "POST":
        message["message_info"] = "用户名或密码错误，原因可能是:忘记密码!"
    return render_to_response("login.html",RequestContext(request, message))

def view_loginout(request):
    logout(request)
    return HttpResponseRedirect("/sale/")

urlpatterns = patterns('',
    (r'^customers/$',saleViews.customers),
    (r'^saleOp/$',saleViews.saleOp),
    (r'^rechargeRecord/$',saleViews.rechargeRecord),
    (r'^login/$',view_login),
    (r'^logout/$',view_loginout),
    (r'^index/$',saleViews.loginPage),
    (r'^$',saleViews.loginPage),
)