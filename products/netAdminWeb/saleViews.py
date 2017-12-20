#coding=utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext

def loginPage(request):
    return render_to_response('login.html', RequestContext(request, {"userType": "SaleUser"}))

def customers(request):
    return render_to_response("sale/customers.html", RequestContext(request, {})) 

def saleOp(request):
    return render_to_response("sale/saleOp.html", RequestContext(request, {}))
            
def rechargeRecord(request):
    return render_to_response("sale/rechargeRecord.html", RequestContext(request, {}))
