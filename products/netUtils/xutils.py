
#coding=utf-8
'''
Created on 2012-12-8

@author: Administrator
'''
import re
import sys
import types
import md5
import os
import time



severitys = {'critical':5, 'error':4, 'warning':3, 'info':2, 'debug':1, 'clear':0}
eventStates = {'unacknowledge':0, 'acknowledge':1, 'suppress':2} #未确认0，确认1,  禁止2


def fixObjectId(oid):
    """
    如果oid是满足ObjectId格式， 则返回ObjectId对象
    否则返回原始值
    """
    from bson.objectid import ObjectId
    if not oid: raise Exception("empty or None value can not fix to objectId.")
    if oid and type(oid) in types.StringTypes and len(oid) != 24: return oid
    if ObjectId.is_valid(str(oid)): return ObjectId(str(oid))
    return oid

def fixPerfDbName(uid, componentType):
    """
    生成性能数据库的名称
    @param uid: <string>监控对象UID
    @param componentType: <string>监控对象类名
    """
    _index = 0
    if not uid:
        raise Exception("uid param error.")
    
    if not componentType:
        raise Exception("componentType param error.")

    _index = int(uid, 16)%10
    return "%s-%s" %(componentType, _index)
        
def importClass(modulePath, classname=""):
    """
    Import a class from the module given.

    @param modulePath: path to module in sys.modules
    @type modulePath: string
    @param classname: name of a class
    @type classname: string
    @return: the class in the module
    @rtype: class
    """
    try:
        if not classname: 
            classname = modulePath.split(".")[-1]
            modulePath = ".".join(modulePath.split(".")[0:-1])
        try:
            __import__(modulePath, globals(), locals(), classname)
            mod = sys.modules[modulePath]
        except (ValueError, ImportError, KeyError), ex:
            raise ex

        return getattr(mod, classname)
    except AttributeError:
        raise ImportError("Failed while importing class %s from module %s" % (classname, modulePath))
    
    
def getEventManager():
    from products.netPublicModel.modelManager import ModelManager
    return  ModelManager.getMod('eventManager')

def getDataRoot():
    from products.netPublicModel.modelManager import ModelManager
    return  ModelManager.getMod('dataRoot')


def nbPath(subPath=""):
    home = os.environ["NBHOME"]
    return home + subPath
    
def sendMail(subject, message, recipient_list, attachments=[]):
    """
    发送邮件
    @param subject: <string>邮件主题
    @param message: <string>邮件内容
    @param recipient_list: 收集人列表
    @param attachments: 附件文件路径列表
    
    @note: 关于邮件服务器的配置，及登陆用户名、密码在配置文件中获取
    """
    from products.netUtils import xemail
    from products.netUtils.settings import ManagerSettings
    settings = ManagerSettings.getSettings()
    server={}
    server["name"] = settings.get("mailServer", "sername")
    server["port"] = settings.getAsInt("mailServer", "port")
    server["user"] = settings.get("sendUser", "username")
    server["passwd"] = settings.get("sendUser", "password")

    xemail.send_mail(server, server["user"], recipient_list, subject, message, files=attachments)
    

def isValidIp(ip):
    if re.match(r"^\s*\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s*$", ip): return True
    return False
    
def isValidMac(mac):
    if re.match(r"^\s*([0-9a-fA-F]{2,2}[:|-]){5,5}[0-9a-fA-F]{2,2}\s*$", mac): return True
    return False

def isValidEmail(email):
    if re.match(r"^[0-9a-zA-Z_\.#]+@(([0-9a-zA-Z]+)[.])+[a-z]{2,4}$", email): return True
    return False

def isValidPhone(phone):
    if re.match(r"^\d{11}$", phone): return True
    return False
    
def isOnlyContainNum(num):
    num = "%s" %num
    if re.match(r"^[0-9]+$",num):return True
    return False

def parseInt(val, default=0):
    try:
        return int(val)
    except:
        return default
         
def ellipsisText(text, length=26, position="center"):
    """
    省略文本
    @param length: 最大长度
    @position: 位置 center | right  
    """
    if not text: return text
    text = unicode(text)
    if len(text) <= length: return text
    if position == "right": return text[:length] + "..." 
    
    if position != "right":
        lenL = length / 2
        lenR = length - lenL
        return "%s...%s" %(text[:lenL], text[-lenR:])
    
    return text

def mkMd5(xstr):
    return md5.new(xstr).hexdigest()


def getIpmiDefaultConfig():
    ipmiConfig=dict(
            netIpmiUserName="root",
            netIpmiIp="",
            netIpmiPassword="netbase"
    )
    return ipmiConfig

def  formartTime(ts,fm="%Y-%m-%d"):
    if not ts: return ""
    lt = time.localtime(ts)
    return time.strftime(fm, lt)

def getDeviceSnmpAndCommDefaultConfig():
    
    config = dict(
                snmpConfig=dict( 
                        netMaxOIDPerRequest=40,
                        netSnmpMonitorIgnore=False,
                        netSnmpAuthPassword=None, 
                        netSnmpAuthType=None,
                        netSnmpCommunity='public', 
                        netSnmpPort=161,
                        netSnmpPrivPassword=None,
                        netSnmpPrivType=None,
                        netSnmpSecurityName=None,
                        netSnmpTimeout=3,
                        netSnmpTries=2, 
                        netSnmpVer='v2c'
                ),                                

                commConfig=dict(
                        netCommandPort="",
                        netCommandUsername="",
                        netCommandPassword="",
                        netCommandLoginTimeout=10,
                        netCommandCommandTimeout=30, 
                        netKeyPath="~/.ssh/id_dsa",
                        netSshConcurrentSessions=10,
                        hcPorts="80",
                        hcType="ping" #ping|port
                ),
                wmiConfig=dict(
                        netWmiProxy="",
                        netWinUser="administrator",
                        netWinPassword="netbase"
                )
                
        )

    return config


def byte2readable(val, bps=True):
    """
    字节数据转为可读文本
    如 1024 -> 1k
    """
    if val is None: return val
    val = float(val)
    keys = [{"name":"Gbps", "val": 1024*1024*1024},{"name":"Mbps", "val": 1024*1024}, {"name":"Kbps", "val": 1024}, {"name":"bps", "val":1}];
    if not bps:
        keys = [{"name":"G", "val": 1024*1024*1024},{"name":"M", "val": 1024*1024}, {"name":"K", "val": 1024}, {"name":"B", "val":1}];
    
    for item in keys:
        _val = item.get("val")
        if val >= _val: return "%.1f%s" %(float(val)/_val, item.get("name")) 
            
    return "%s" %val

def sec2UseTime(ut):
    "秒转时间"
    if ut is None: return "unknown"
    if ("%s" %ut).strip().isdigit(): ut = int(ut)
    
    if ut < 0: return "unknown"
    elif ut == 0: return "0天0小时0分"
    
    days = ut / 86400
    hour = (ut % 86400) / 3600
    mins = (ut % 3600) / 60
    return "%d天%d小时%d分" % (days,hour,mins)

def  page(pn, total, ps=10):
    """
    分页
    @param pn: 当前页码
    @param total: 总记录数
    @param ps: page size
    """
    xlist = []
    ln = rn = pn
    lx = rx = 0
    totalPage = int(total/ps) + (1 if total%ps else 0)
    xlist.append(pn)
    while True:
        if len(xlist) >= 10:break
        if ln >1:
            ln-=1
            xlist.append(ln)
        else:
            lx = 1
        
        if len(xlist) >= 10:break
        if rn < totalPage:
            rn+=1
            xlist.append(rn)
        else:
            rx=1
            
        if lx + rx == 2:
            break
        
    xlist.sort()
    return {"pn":pn, "plist":xlist}

def getRandomStr(num, onlyNumber=False):
    import random
    chars=['0','1','2','3','4','5','6','7','8','9',
        'a','b','c','d','e','f','g','h','i','j','k','l','m','n',
        'o','p','q','r','s','t','u','v','w','x','y','z']
    if onlyNumber:
        chars=['0','1','2','3','4','5','6','7','8','9']
        
    strRandom =  "".join([random.choice(chars) for x in  range(num)])
    return strRandom

def dealTime(t,sp1,sp2):
    t = "%s" % t
    t=t.split()
    year=t[0].split(sp1)[0]
    month=t[0].split(sp1)[1]
    day=t[0].split(sp1)[2]
    hour=t[1].split(sp2)[0]
    minute=t[1].split(sp2)[1]
    second=t[1].split(sp2)[2]
    t1="%s%s%s%s%s%s"%(year,month,day,hour,minute,second)
    return t1
    
def dealPageNum(pageNum):
    if not isOnlyContainNum(pageNum):pageNum = "1"
    pageNum = int(pageNum)
    if pageNum <=0:pageNum = 1
    return pageNum

def countMoney(count,price,discount):
    return count*price*discount

def setDiscount(count):
    if count <10:return 1.00
    if count < 100:return 0.90
    if count < 500:return 0.80
    else:return 0.50

def isValiedNum(num,allowZero=True):
    num = "%s" %num
    if allowZero:
        if num=="0":return True
    if re.match(r"^0",num):return False
    if re.match(r"^[0-9]+$",num):return True
    return False

def addAttachment(request,sn):
    file_obj = request.FILES.get("Filedata", None)
    if not file_obj: return "success"
    fileDict=["txt","rar","zip","gz","tar","bz","gzip2","ppt","pptx","doc","docx","xlsx","xls", "wps","dps","et",
              "jpg","jpeg","psd","swf","png","raw","bmp","tiff","svg","gif"]
    fileNameSuffix=file_obj.name.split(".")[1].lower()
    if fileNameSuffix not in fileDict:
        return "warn:不允许的文件格式，只允许文本文件，压缩文件，office文件,常用图片文件格式"
    if file_obj.size/(1024*1024)>10:return "warn:附件的大小不能超过5M"
    attachFileName = "%s_%s" %(sn.getUid(), file_obj.name)
    attachFile = open(nbPath(u"/nbfiles/upload/%s" %unicode(attachFileName)), "wb+")
    sn.attachments += [attachFileName]
    data = file_obj.read()
    attachFile.write(data)
    file_obj.close()
    attachFile.close()
    return "success"
    
if __name__  == "__main__":
    
    print byte2readable(1024)
    
    
    
    
    
    
