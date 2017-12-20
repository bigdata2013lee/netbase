#coding=utf-8
from products.netPublicModel import telVerfyCode
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf.urls.defaults import patterns, include, url
from settings import MEDIA_ROOT
from django.http import HttpResponseRedirect, HttpResponse
from products.netWebAPI.apiView import remoteView 
from products.netUtils.settings import ManagerSettings
from products.netUtils import xutils
import logging
from products.netWebAPI.feedBackInfoApi import FeedBackInfoApi
import os
from products.netModel.user.user import User
from products.netModel.baseModel import RefDocObject
from products.netModel.device import Device
from products.netModel.website import Website
from products.netModel.network import Network
from products.netBilling.levelPolicy import LevelPolicy
from products.netModel import operation
from products.netModel.operation.operationer import Operationer
from products.netModel.operation.deviceDtail import DeviceDtail
log = logging.getLogger('django.request')

confSettings = ManagerSettings.getSettings()



def default_site_page(request):
    context = {}
    return render_to_response(
        'loginAndRegister/login.html',  RequestContext(request, context)
    )


def  outsitePage(request, htmlName):
    return render_to_response('outsite/%s.html' %htmlName)

def index(request):
    return render_to_response('index.html')

def login_html(request):
    return render_to_response('login.html')

def getVerifyCode(request):     
    from DjangoVerifyCode import Code
    CODE_WORLDS = [xutils.getRandomStr(4)]
    
    code =  Code(request)     
    code.worlds = CODE_WORLDS
    code.type = 'world'     
    #code.type = 'number' 
    return code.display()


def feedbacksuccess(request):
    return render_to_response( "feedbacksuccess.html", RequestContext(request,{}))
                               
def feedback(request):
    c={}
    if request.method == "POST":        
        request.csrf_processing_done = True
        feedBackContent = request.REQUEST.get("feedBackContent")
        feedBackUser = request.REQUEST.get("feedBackUser")
        feedBackEmail = request.REQUEST.get("feedBackEmail")
        fapi = FeedBackInfoApi()
        
        if not feedBackContent and not feedBackEmail:
            c["errorMsg"] = "请填写您的宝贵意见"
        
        elif len(feedBackContent) < 6:
            c["errorMsg"] = "请认真填写您的宝贵意见，意见内容不少于6个字."
        
        if not c.get("errorMsg",None):
            msg = fapi.addFeedBackInfo(dict(feedBackContent=feedBackContent, 
                                            feedBackUser=feedBackUser, 
                                            feedBackEmail=feedBackEmail))
            
            c["successMsg"] = msg
            return HttpResponseRedirect("/feedback/success")   

    return render_to_response("feedback.html", RequestContext(request, c))

  

def getPhoneVerifyCode(request, phoneID):

    request.session["phoneVerifyCode_phone"] = phoneID
    if telVerfyCode.checkLastCodeLive(request.session):
        print ">>log:频繁获取验证码"
        return HttpResponse("error")
    
    code = telVerfyCode.createPhoneCode(request.session)
    msg = telVerfyCode.msgTpl_01 %code
    sendStatus = telVerfyCode.sendTelMsg(msg, phoneID)
    
    return HttpResponse(sendStatus)

def reportOpinion(request):
    return render_to_response("reportOpinion.html", RequestContext(request, {}))

urlpatterns = patterns('',                    
    (r'^feedback/$', feedback), 
    (r'^feedback/success$', feedbacksuccess), 
    (r'^getVerifyCode/$', getVerifyCode),
    (r'^getPhoneVerifyCode/(?P<phoneID>\d+)/$', getPhoneVerifyCode),
    url(r'^accounts/', include('netMinWeb.accountsUrls')),
    url(r'^ucenter/', include('netMinWeb.ucenterUrls')),
    url(r'^monitor/', include('netMinWeb.monitorUrls')),
    url(r'^middleware/', include('netMinWeb.middlewareUrls')),
    url(r'^network/', include('netMinWeb.networkUrls')),
    url(r'^website/', include('netMinWeb.websiteUrls')),
    url(r'^events/', include('netMinWeb.eventsUrls')),
    url(r'^assistant/', include('netMinWeb.assistantUrls')),
    url(r'^settings/', include('netMinWeb.settingsUrls')),
    url(r'^report/', include('netMinWeb.reportUrls')),
    url(r'^message/', include('netMinWeb.messageUrls')),
    url(r'^help/', include('netMinWeb.helpUrls')),
    url(r'^blog/', include('netMinWeb.blogUrls')),
    url(r'^location/', include('netMinWeb.locationUrls')),
    url(r'^template/', include('netMinWeb.templateUrls')),
    url(r'^collector/', include('netMinWeb.collectorUrls')),#下载密钥用的
    url(r'^viewer/', include('netMinWeb.viewerUrls')),
    (r'^remote/(?P<apiClsName>\w*)/(?P<methodName>[a-zA-Z]+\w*)/', remoteView),
    (r'media/(?P<path>.+)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
    (r'^(?P<path>favicon\.ico)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT+"/images"}),
    (r'downloads/(?P<path>.+)$', 'django.views.static.serve', {'document_root': "%s/nbfiles/upload/" %os.environ["NBHOME"]}),
    (r'chart_images/(?P<path>.+)$', 'django.views.static.serve', {'document_root': "%s/nbfiles/imgs/"  %os.environ["NBHOME"]}),
    (r'^index/', index),
    (r'^login.html/', login_html),
    (r'^outsite/(?P<htmlName>.+)\.html/$', outsitePage),
    (r'^reportOpinion/', reportOpinion),
    (r'^$', index),
)
