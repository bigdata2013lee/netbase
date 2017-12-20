#coding=utf-8

import time
import random

from django.conf.urls.defaults import patterns
from django.shortcuts import render_to_response
from django.template import RequestContext
from products.netModel.userForgetRecTable import UserLookForPwdRec
from products.netUtils.settings import ManagerSettings
from products.netUtils import xutils
from products.netModel.user.user import User
from products.netPublicModel.emailTemplates import user_pwd_mail_html

import logging
log = logging.getLogger('django.request')


confSettings = ManagerSettings.getSettings()
_Letters=['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']


def  _insertLookForPwdRec(userId, code):
        ufts = UserLookForPwdRec._findObjects({"userId": userId})
        for  rec in ufts: rec.remove()
        
        rec = UserLookForPwdRec()
        rec.userId = userId
        rec.code = code
        rec.stamp = time.time()
        rec.status =False
        rec._saveObj()
        
    
def _sendPwdMail(user, code):
    
    subject = "Netbase系统邮件--找回密码"
    active_url = confSettings.get("mainServer", "hostUrl") #服务器端的主路径url
    message = user_pwd_mail_html % {
         "user":user.username, 
         "url":"%s/accounts/forgetPwd/lookfor/%s/%s" % (active_url,user.getUid(), code)
    }
    
    xutils.sendMail(subject=subject, message=message, recipient_list=[user.email])


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
        
        
        code = "".join([random.choice(_Letters) for x in xrange(8)])
        
        try:
            _sendPwdMail(u, code)
        except Exception ,e:
            log.warn("邮件发送失败")
            log.exception(e)
            context["error_message"] = "邮件发送失败，可能无法联系到你的邮箱"
            
            return render_to_response( "forgetPwd.html", RequestContext(request, context))
        
        
        _insertLookForPwdRec(u.getUid(), code)
        
        context["rs"] = "toEmailFindPwd"
        context["email"] = u.email
        
    return render_to_response( "forgetPwd.html", RequestContext(request, context))
    
    
def  lookfor(request, userId, code):
    context = {}
    context["rs"] = "fromEmailPage"
    context["infos"] =  dict(userId=userId, code=code)
    
    ufts = UserLookForPwdRec._findObjects({"userId": userId, "code": code})
    user = User._loadObj(userId)
    
    if not ufts or  ufts[0].status or  int(time.time() - ufts[0].stamp) > 86400 or  not user:
        context["rs"] = "expireTime"
    
    return render_to_response( "forgetPwd.html", RequestContext(request, context))

def resetPwd(request):
    context = {}
    
    userId = request.REQUEST.get("userId")
    code = request.REQUEST.get("code")
    password = request.REQUEST.get("password")
    
    ufts = UserLookForPwdRec._findObjects({"userId": userId, "code": code})
    
    
    user = User._loadObj(userId)
    
    if not ufts or  ufts[0].status or  int(time.time() - ufts[0].stamp) > 86400 or  not user:
        context["rs"] = "expireTime"
        return render_to_response( "forgetPwd.html", RequestContext(request, context))
    
    

    context["rs"] = "success"
    
    user.password = password
    ufts[0].status = True
    return render_to_response( "forgetPwd.html", RequestContext(request, context))



urlpatterns = patterns('',
    (r'^$',forgetPwd),
    (r'^lookfor/(?P<userId>\w+)/(?P<code>\w+)/$',lookfor),
    (r'^resetPwd/$',resetPwd),
)
