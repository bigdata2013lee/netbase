#coding=utf-8

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf.urls.defaults import patterns
import logging
from products.netWebAPI.communityApi.topicApi import TopicApi
from products.netCommunity.question import Question
from products.netUtils import xutils
from products.netCommunity.share import Share
from products.netWebAPI.eventApi import EventApi
from products.netPublicModel.userControl import UserControl
from products.netWebAPI.admin.operationApi import OperationApi
from products.netModel.operation.operationer import Operationer
from products.netModel.user.engineerUser import EngineerUser
from products.netModel.user.user import User
from django.http import HttpResponse
log = logging.getLogger('django.request')

def index(request):
    publisher=UserControl.getUser()
    topicApi=TopicApi()
    qList=topicApi.listQuestions()
    sList=topicApi.listShares()
        
    context=dict(qList=qList,sList=sList,publisher=publisher, pageName="myDynamic")
    return render_to_response("ucenter/myDynamic.html", RequestContext(request, context))

def aboutme(request):
    topicApi=TopicApi()
    newCommentQList=topicApi.getNewMessageQuestionList()
    newCommentSList=topicApi.getNewMessageShareList()
    qList=[]
    sList=[]
    aboutme="aboutme"
    if newCommentQList or newCommentSList:
        qList=newCommentQList
        sList=newCommentSList
    context=dict(qList=qList,sList=sList,aboutme=aboutme, pageName="aboutMe")
    return render_to_response("ucenter/myDynamic.html", RequestContext(request, context))

def deviceDynamic(request):
    eventApi=EventApi()
    publisher=UserControl.getUser()
    pageData={"limit":200,"skip":0,"sort":{"endTime":-1}}
    conditions={"severity":{"$gte":3}}
    ret=eventApi.searchEvents(pageData, conditions)
    context=dict(ret=ret,publisher=publisher, pageName="deviceDynamic")
    return render_to_response("ucenter/deviceDynamic.html", RequestContext(request, context))

def community(request):
    context=dict(pageName="community")
    return render_to_response("ucenter/community.html", RequestContext(request, context))

def communityAnonymous(request):
    return render_to_response("ucenter/communityAnonymous.html", RequestContext(request, {}))

def viewQuestion(request, questionId):
    topic=Question._loadObj(questionId)
    visiter=request.user
    
    if str(visiter)=="AnonymousUser": 
        visiter="None"
    else:
        visiter="Have"
    sortFiled = request.REQUEST.get("sort", "ctime")
    if  sortFiled not in ["approveNum","ctime"]: sortFiled = "approveNum"
    sortInfo={sortFiled:-1}
    pn = request.REQUEST.get("pageNum", 1)
    pn = int(pn)
    ps = 10
    ptotal=topic.replyNum
    commentList=topic.getComments(sortInfo=sortInfo, skip=(pn-1)*ps,  limit=ps)
    topicApi=TopicApi()
    topicApi.readMessage(topic)
    accetpComment=topicApi.getAcceptComment(topic, commentList)
    
    pageInfos = xutils.page(pn, ptotal, ps=ps)
    context=dict(commentList=commentList,topic=topic, accetpComment=accetpComment,
                 pageInfos=pageInfos,visiter=visiter,topicType="Question", pageName="community")
    if visiter=="Have":
        return render_to_response("ucenter/viewTopic.html", RequestContext(request, context))
    else:
        return render_to_response("ucenter/viewTopicAnonymous.html", RequestContext(request, context))

def viewShare(request, shareId):
    visiter=request.user
    if str(visiter)=="AnonymousUser": 
        visiter="None"
    else:
        visiter="Have"    
    topic=Share._loadObj(shareId)
    sortFiled = request.REQUEST.get("sort", "ctime")
    if  sortFiled not in ["approveNum","ctime"]: sortFiled = "approveNum"
    sortInfo={sortFiled:-1}
    pn = request.REQUEST.get("pageNum", 1)
    pn = int(pn)
    ps = 10
    ptotal=topic.replyNum
    commentList=topic.getComments(sortInfo=sortInfo, skip=(pn-1)*ps,  limit=ps)
    topicApi=TopicApi()
    topicApi.readMessage(topic)
        
    pageInfos = xutils.page(pn, ptotal, ps=ps)
    context=dict(commentList=commentList,topic=topic, pageInfos=pageInfos,visiter=visiter,topicType="Share", pageName="community")
    if visiter=="Have":
        return render_to_response("ucenter/viewTopic.html", RequestContext(request, context))
    else:
        return render_to_response("ucenter/viewTopicAnonymous.html", RequestContext(request, context))

def searchQuestions(request):
    topicApi=TopicApi()
    
    pn = request.REQUEST.get("pageNum", 1)
    pn = int(pn)
    ps = 10
    
    
    keywords = request.REQUEST.get("keywords")
    d0 = request.REQUEST.get("d0")
    d1 = request.REQUEST.get("d1")
    fields = request.REQUEST.get("fields","")
    fields = fields.strip()
    _fields=[]
    if(fields):_fields=fields.split(",")
    
    
    searchResult = topicApi.searchQuestions(text=keywords, area={"d0":d0,"d1":d1},
                                            fields=_fields,sortInfo=None,skip=(pn-1)*ps ,limit=ps)
    pageInfos = xutils.page(pn, searchResult.get("total",0), ps=ps)

    context=dict(searchResult=searchResult, pageInfos=pageInfos, topicType="Question")
    return render_to_response("ucenter/search_results.html", RequestContext(request, context))
         
         
def searchShares(request):
    topicApi=TopicApi()
    
    pn = request.REQUEST.get("pageNum", 1)
    pn = int(pn)
    ps = 20
    
    
    keywords = request.REQUEST.get("keywords")
    d0 = request.REQUEST.get("d0")
    d1 = request.REQUEST.get("d1")
    fields = request.REQUEST.get("fields","")
    fields = fields.strip()
    _fields=[]
    if(fields):_fields=fields.split(",")
    
    
    searchResult = topicApi.searchShares(text=keywords, area={"d0":d0,"d1":d1},
                                            fields=_fields,sortInfo=None,skip=(pn-1)*ps ,limit=ps)
    pageInfos = xutils.page(pn, searchResult.get("total",0), ps=ps)

    context=dict(searchResult=searchResult, pageInfos=pageInfos,topicType="Share")
    return render_to_response("ucenter/search_results.html", RequestContext(request, context))
                              
def  listTopicAboutFiled(request):
    topicApi=TopicApi()
    pn = request.REQUEST.get("pageNum", 1)
    pn = int(pn)
    ps = 20
    filed = request.REQUEST.get("filed","")
    topicType = request.REQUEST.get("topicType","Question")
    topicTypes = ["Question","Share"]
    if topicType not in topicTypes: topicType = "Question"
    
    _fields=[]
    if filed:_fields.append(filed)
    
    searchResult = []
    if topicType=="Question":
        searchResult = topicApi.searchQuestions(text="", area={},fields=_fields,sortInfo=None,skip=(pn-1)*ps ,limit=ps)
    if topicType=="Share":
        searchResult = topicApi.searchShares(text="", area={},fields=_fields,sortInfo=None,skip=(pn-1)*ps ,limit=ps)
        
    pageInfos = xutils.page(pn, searchResult.get("total",0), ps=ps)

    context=dict(searchResult=searchResult, pageInfos=pageInfos, topicType=topicType)
    return render_to_response("ucenter/abouteFiled.html", RequestContext(request, context))
    
def operationerList(request):
    api = OperationApi() 
    pn = request.REQUEST.get("pageNum",1);
    pn = int(pn)
    ps = 20
    
    technologyFileds = request.REQUEST.get("technologyFileds","");
    technologyFileds = technologyFileds.split(",")
    technologyFileds = filter(lambda filed: filed, technologyFileds)
    searchResult = api.searchOperationers(technologyFileds=technologyFileds, skip=(pn-1)*ps, limit=ps)
    pageInfos = xutils.page(pn, searchResult.get("total",0), ps=ps)
    context = dict(searchResult=searchResult, pageInfos=pageInfos, pageName="operationerList")
    return render_to_response("ucenter/operationerList.html", RequestContext(request, context)) 
    
def viewOperationer(request, operationerId):
    operationer = Operationer._loadObj(operationerId)
    context = dict(operationer=operationer, pageName="operationerList")
    return render_to_response("ucenter/viewOperationer.html", RequestContext(request, context)) 


def showUser(request,userId, userType):
    
    xuser=None
    if userType=="User":
        xuser = User._loadObj(userId)
    
    if userType=="Operationer":
        xuser = Operationer._loadObj(userId)
        
    if userType=="Enginner":
        xuser = EngineerUser._loadObj(userId)
    
    
    context = dict(xuser=xuser, userType=userType)
    return render_to_response("ucenter/showUser.html", RequestContext(request, context)) 

def checkVerifyCode(request):
    from DjangoVerifyCode import Code
    code = Code(request)
    if not code.check(request.REQUEST.get("verifyCode","")):
        return HttpResponse("验证码错误")
    return  HttpResponse("0")  
                    
urlpatterns = patterns('',                    
    (r'^index/$', index),
    (r'^aboutme/$', aboutme),
    (r'^searchQuestions/$', searchQuestions),
    (r'^searchShares/$', searchShares),
    (r'^deviceDynamic/$', deviceDynamic),
    (r'^community/$', community),
    (r'^checkVerifyCode/$', checkVerifyCode),
    (r'^abouteFiled/$', listTopicAboutFiled),
    (r'^communityAnonymous/$', communityAnonymous),
    (r'^viewQuestion/(?P<questionId>\w+)/$', viewQuestion),    
    (r'^viewShare/(?P<shareId>\w+)/$', viewShare),
    (r'^operationerList/$', operationerList),
    (r'^viewOperationer/(?P<operationerId>\w+)/$', viewOperationer),
    (r'^showUser/(?P<userId>\w+)/(?P<userType>\w+)/$', showUser),        
)