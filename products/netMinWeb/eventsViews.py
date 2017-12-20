#coding=utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
import json
from products.netPublicModel.userControl import UserControl



def _loadParams(request, pname):
    q = request.REQUEST.get(pname, "{}")
    q = json.loads(q)
    return q


#-------------------------------------------------------------------------------------------    
def index(request):
    user=UserControl.getUser()
    return render_to_response("event/events_index.html",RequestContext(request, {"user":user})) 

def eventHistoryList(request):
    return render_to_response("event/events_history_index.html",RequestContext(request, {})) 


def config(request):
        return render_to_response("event/config.html", RequestContext(request, { })) 
    
