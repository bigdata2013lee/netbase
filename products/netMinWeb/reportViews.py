#coding=utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext


#-------------------------------------------------------------------------------------------    
def index(request):
    return render_to_response("report/report_default.html", RequestContext(request, { })) 
    
def reportIndex(request, moUid):
    return render_to_response("report/report_index.html", RequestContext(request, {"moUid":moUid}))

def addreport(request):
        return render_to_response("report/report_add.html", RequestContext(request, { })) 
