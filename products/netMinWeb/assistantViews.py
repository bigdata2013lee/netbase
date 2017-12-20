#coding=utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from products.netModel.collector import Collector



#-------------------------------------------------------------------------------------------    
def index(request):
    colls = Collector._findObjects()
    return render_to_response("assistant/bootpo_index.html", RequestContext(request, {"collectors": colls}))
        


    
def shortcutCmdIndex(request):
    return render_to_response("assistant/shortcutCmd_index.html", RequestContext(request, {}))