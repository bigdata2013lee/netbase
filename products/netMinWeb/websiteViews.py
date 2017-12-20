#coding=utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
import json
from products.netModel.org.webSiteClass import WebSiteClass
from products.netWebAPI.websiteApi import WebsiteApi
from products.netModel.website import Website
from products.netModel.baseModel import RefDocObject
from products.netPublicModel.userControl import UserControl



def _loadParams(request, pname):
    q = request.REQUEST.get(pname, "{}")
    q = json.loads(q)
    return q


#-------------------------------------------------------------------------------------------    
def index(request):
    api = WebsiteApi()
    websites = api.listWebsites()
    user=UserControl.getUser()
    ownCompany=user.ownCompany
    conditions={"ownCompany":RefDocObject.getRefInfo(ownCompany)}
    usedNum = Website._countObjects(conditions)
    count=user.levelPolicy.websiteCount
    availableNum=count - usedNum
    numDic={"usedNum":usedNum,"count":count,"availableNum":availableNum}
    context=dict(pageName="website_list", websites=websites,numDic=numDic)
    return render_to_response("website/website_list.html", RequestContext(request, context)) 

def website_add(request):
    context=dict(pageName="website_add")
    return render_to_response("website/website_add.html", RequestContext(request, context)) 

def website_conf(request, websiteUid):
    ws = Website._loadObj(websiteUid)
    context=dict(pageName="website_conf", ws=ws)
    return render_to_response("website/website_conf.html", RequestContext(request, context)) 
    
def website_detail(request, websiteUid):
    api = WebsiteApi()
    ws = Website._loadObj(websiteUid)
    cptsInfos = api.listCptsInfos(websiteUid)
    
    context=dict(pageName="website_detail", ws=ws, cptsInfos=cptsInfos)
    return render_to_response("website/website_detail.html", RequestContext(request, context)) 

def websiteClsIndex(request, orgUid):
    return render_to_response("website/websiteCls_index.html", RequestContext(request, {"orgUid":orgUid})) 
    
def config(request):
    return render_to_response("website/config.html", RequestContext(request, {})) 


    
