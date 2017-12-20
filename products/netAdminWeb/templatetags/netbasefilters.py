#coding=utf-8
from django import template
import time
register = template.Library()

@register.filter
def getSureLength(target,length):
    return target[0:length]

@register.filter(name='cut')
def cut(value, arg):
    return value.replace(arg, '')

@register.filter
def lower(value):
    return value.lower()


@register.filter
def firstPath(value):
    maps = {"EngineerUser":"engineer", "SaleUser":"sale", "AdminUser":"admin","Operationer":"operation"}
    return maps.get(value, "")

@register.filter
def userType(value):
    request = value
    ut = request.REQUEST.get("userType","")
    if  not ut:
        ut = request.session.get("userType","")
    return ut
    
@register.filter
def formatTime(t):
    if not t: return ""
    strT = time.strftime("%Y-%m-%d %H:%M", time.localtime(t))
    return strT

@register.filter
def formatShortTime(t):
    if not t: return ""
    strT = time.strftime("%Y-%m-%d", time.localtime(t))
    return strT    


@register.filter
def  defaultIcon(icon):
    if not icon:
        return  '/media/user_icons/37ce1031959a0755f194b4c1938387d1.jpg'
    return icon 

@register.filter
def  getName(username):
    name=username.split("@")
    return name[0]

@register.filter
def  getLevelValue(level):
    level="%s" % level
    if level=="5" or level=="4":return "好"
    if level=="3":return "一般"
    if level=="2" or level=="1":return "差"   
    
@register.filter
def  cutAttachName(filename):
    fl=filename.split("_")
    return fl[len(fl)-1]

@register.filter
def  getGoodRate(goodRate):
    fr=float(goodRate)*100
    return "%.2f%% " % fr

@register.filter
def  userType2(u):
    userType = u.__class__.__name__
    if userType == "Operationer":
        return "运营商"
    elif userType == "User":
        return "普通用户"
    else:
        return userType

@register.filter
def getTime(stime):
    if "T" not in stime :return stime
    if "." not in stime:return stime 
    strTimes=stime.split("T")
    hours=strTimes[1].split(".")
    year=strTimes[0]
    hour=hours[0]
    rs=year+" "+hour
    return    rs

