#coding=utf-8
import json
import time
from products.netPublicModel import telVerfyCode
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.translation import check_for_language
from django.conf.urls.defaults import patterns, include, url
from django.http import HttpResponseRedirect, HttpResponse
from products.netWebAPI.userApi import UserApi
from products.netModel.user.user import User
from products.netPublicModel.emailTemplates import user_pwd_mail_html
from products.netUtils import xutils
import logging
log = logging.getLogger('django.request')


def view_loginout(request):
    logout(request)
    return HttpResponseRedirect("/index")

def view_loginout2(request):
    logout(request)
    return HttpResponse(json.dumps("ok"))

def view_register(request):

    userInfo = request.REQUEST.get("userInfo")
    if not userInfo: userInfo = None
    userInfo = json.loads(userInfo)
    #print "userInfo:", userInfo
    verifyCode = userInfo.get("phoneVerify","")
    #print "phoneVerifyCode:", request.session.get("phoneVerifyCode",{}).get("code")
    if not telVerfyCode.checkPhoneVerifyCode(request.session, verifyCode):
        return HttpResponse("warn:验证码错误")
    
    if not userInfo.get('password', ''):
        return HttpResponse("warn:请输入密码")
    
    if not userInfo.get('phoneNum', ''):
        return HttpResponse("warn:请输入手机号码")
      
    if request.session.get("phoneVerifyCode_phone","") != userInfo.get('phoneNum', ''):
        return HttpResponse("warn:请输入您刚才收到验证码的手机号")
    
    if not User.isVaildUserName(userInfo.get('email', '')):
        return HttpResponse("warn:你的用户名"+userInfo.get('email', '')+"，已经申请过帐号")
    
    if not User.isVaildPhone(userInfo.get('phoneNum', '')):
        return HttpResponse("warn:你的手机号"+userInfo.get('phoneNum', '')+"，已经申请过帐号")
    
    userApi = UserApi()
    userApi.request = request
    msg = userApi.registerUser(userInfo)
    return HttpResponse(msg)
    
def view_login(request):
    "系统用户登入"
    message = {}
    request.csrf_processing_done = True
    userInfo = request.REQUEST.get("userInfo")
    if not userInfo: userInfo = None
    userInfo = json.loads(userInfo)
    verifyCode = userInfo.get("verifyCode","")
    from DjangoVerifyCode import Code
    code = Code(request)
    if not code.check(verifyCode):
        return HttpResponse("验证码错误")
    user = authenticate(username=userInfo.get("username"), password=userInfo.get("password"))
    if user is not None:
        if not user.is_active:
            message["message_info"] = "您的账户未激活！"
            return HttpResponse("您的账户未激活!")
        user.id = user.getUid()
        ret = login(request, user)
        #使用默认安装时选择的语言
        lang_code = settings.LANGUAGE_CODE
        if lang_code and check_for_language(lang_code):
            if hasattr(request, 'session'):
                request.session['django_language'] = lang_code
            else:
                ret.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
        return HttpResponse("0")
    return  HttpResponse("用户名或密码错误!")

def view_login2(request):
    "系统用户登陆 from app"
    request.csrf_processing_done = True
    user = authenticate(username=request.REQUEST.get("username"), password=request.REQUEST.get("password"))
    if user is not None:
        if not user.is_active:
            return HttpResponse(json.dumps({"status":"fail","msg":"您的账户未激活！"}))           
        user.id = user.getUid()
        ret = login(request, user)
        #使用默认安装时选择的语言
        lang_code = settings.LANGUAGE_CODE
        if lang_code and check_for_language(lang_code):
            if hasattr(request, 'session'):
                    request.session['django_language'] = lang_code
            else:
                    ret.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
        return HttpResponse(json.dumps({"status":"ok","msg":"登陆成功"}))
    return HttpResponse(json.dumps({"status":"fail","msg":"用户名或密码错误，原因可能是:忘记密码!"}))

def view_active(request, hash_username):
    userApi = UserApi()
    request.csrf_processing_done = True
    ret = userApi.activeUser(hash_username)

    if ret == 'ok':
        return HttpResponseRedirect("/accounts/activeSuccess/")   
    
    return HttpResponseRedirect("/accounts/activeFail/")   

def forgetPwd(request):
    "进入忘记密码页面，如果输入了用户名，则验证并发送邮件"
    
    context = {"stime":time.time(), "error_message":"", "rs":""}
    username=request.REQUEST.get("username")
    from DjangoVerifyCode import Code
    if username:
        code = Code(request)
        verifyCode = request.REQUEST.get("verifyCode")
        if not code.check(verifyCode):
            context["error_message"] = "验证码错误，请重新输入！"
            return render_to_response( "forgetPwd.html", RequestContext(request, context))
        
        u = User._loadByUserName(username)
        if not u:
            context["error_message"] = "帐号不存在，请重新输入你注册使用的帐号"
            return render_to_response( "forgetPwd.html", RequestContext(request, context))
        
        if not u.is_active:
            context["error_message"] = "未激活的帐号，无法取回密码"
            return render_to_response( "forgetPwd.html", RequestContext(request, context))
        
        try:
            _sendPwdMail(u)
        except Exception ,e:
            log.warn("邮件发送失败")
            log.exception(e)
            context["error_message"] = "邮件发送失败，可能无法联系到你的邮箱"
            
            return render_to_response( "forgetPwd.html", RequestContext(request, context))
        
        context["rs"] = "success"
        
    return render_to_response( "forgetPwd.html", RequestContext(request, context))

def _sendPwdMail(user):
    subject = "网脊运维通系统邮件--找回密码"
    import hashlib
    rPwd =  xutils.getRandomStr(6)
    user.password=hashlib.md5(rPwd).hexdigest()
    message = user_pwd_mail_html % {
         "user":user.username, "pwd":rPwd
    }
    xutils.sendMail(subject=subject, message=message, recipient_list=[user.email])
    
def registerHtml(request):
    return render_to_response( "loginAndRegister/Registration_Next.html", RequestContext(request, {}))
   
def registerSuccess(request):
    return render_to_response( "loginAndRegister/registerSuccess.html", RequestContext(request, {}) )

def activeSuccess(request):
    return render_to_response( "loginAndRegister/activeSuccess.html", RequestContext(request, {}) )

def activeFail(request):
    return render_to_response( "loginAndRegister/activeFail.html", RequestContext(request, {}) )
  

urlpatterns = patterns('',                    
    (r'^login/$', view_login),
    (r'^loginFromApp/$', view_login2),
    (r'^logout/$', view_loginout),
    (r'^logoutFromApp/$', view_loginout2),
    (r'^register/$', view_register),
    (r'^active/(?P<hash_username>\w+)/', view_active),
    (r'^forgetPwd/$', forgetPwd),
    (r'^register.html/$', registerHtml),
    (r'^registerSuccess/$', registerSuccess),
    (r'^activeSuccess/$', activeSuccess),
    (r'^activeFail/$', activeFail),
    url(r'^forgetPwd/', include('netMinWeb.forgetUrls')),
)
