#coding=utf-8
import time
from django import template

register = template.Library()


@register.filter(name='cut')
def cut(value, arg):
    return value.replace(arg, '')

@register.filter
def lower(value):
    return value.lower()

@register.filter
def getSureLength(target,length):
    return target[0:length]

@register.filter
def rootFilter(value):
    pathlist = value.split("/")
    if len(pathlist) > 1:
        return pathlist[1]
    return None



@register.filter
def startswith(value, prefix):
    return (value or  "").startswith(prefix)

@register.filter(name='isUserExpired')
def isUserExpired(value):
    return value < time.time()

@register.filter
def isEC_user(u):
    lp = u.levelPolicy
    if lp.getUid() in ["enterprise", "customization"]:
        return True
    return False

@register.filter
def toChina(enStr):
    levelPolicy = {"free": "免费版", "standard": "标准版", "enterprise": "企业版", "customization": "定制版"}
    if enStr not in levelPolicy.keys(): return None
    return levelPolicy[enStr]

@register.filter
def hasExtendTpl(moUid, tplName, moType="Device"):
    from products.netWebAPI.monitorApi import MonitorApi
    api = MonitorApi()
    return api.hasExtendTpl(moUid, tplName, moType)
    
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
def  userType(u):
    return u.__class__.__name__


@register.filter
def  cutAttachName(filename):
    fl=filename.split("_")
    return fl[len(fl)-1]

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

@register.filter
def  getName(username):
    name=username.split("@")
    return name[0]
