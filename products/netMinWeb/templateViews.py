#coding=utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
import json
from products.netWebAPI.thresholdApi import ThresholdApi
from copy import deepcopy


thresholdTypeNames = {
"MinThreshold":"最小阀值",
"MaxThreshold":"最大阀值",
"RangeThreshold":"范围阀值",
"StatusThreshold":"状态小阀值",
"KeyThreshold":"关键字阀值"
}

def thresholdList(request, uid, cType):
    context = {}
    thresholdTypeNames["thresholdTypeNames"] = thresholdTypeNames
    thsApi = ThresholdApi()
    thsApi.request = request
    thresholds = thsApi.getMoThresholds(uid, cType)
    rs = []
    thresholds = deepcopy(thresholds)
    for key, val in thresholds.items():
        val["key"] = key
        rs.append(val)
        
    context["thresholds"] = rs
    return render_to_response("threshold/thresholdList.html", RequestContext(request, context)) 


    

