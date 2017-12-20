#coding=utf-8
import sys
from products.netModel.user.user import User
from products.netModel.user.saleUser import SaleUser
from products.netModel.user.engineerUser import EngineerUser
from products.netModel.collector import Collector
import re
from random import randint
from products.netModel.user.idcUser import IdcUser
from products.netUtils.settings import ManagerSettings
settings = ManagerSettings.getSettings()

def activeUser():
    username =raw_input("请输入用户名 :")
    user = User._loadByUserName(username)
    if not user:
        print ">>对不起，操作失败，你指定的用户名不存在."
        return xcontinue()
    else:
        user._medata["is_active"] = True
        user._saveObj()
        print ">>成功激活用户"
        return xcontinue()
    
def addMoney():
    from products.rpcService.client import Client
    rpycHost = settings.get('rpycConnection', 'rpcHost')
    rpycPort = settings.getAsInt('rpycConnection', 'rpcPort')
    if rpycHost == "0.0.0.0":
        rpycHost = '127.0.0.1'
    
    rpcServiceClient = Client(rpycHost, rpycPort) #rpyc客户端
    dr = rpcServiceClient.getServiceObj().getDataRoot()
    username =raw_input("请输入用户名 :")
    user = User._loadByUserName(username)
    if not user:
        print ">>对不起，操作失败，你指定的客户名不存在."
        return xcontinue()
    money =raw_input("输入充值金额 :")
    uid = user.getUid()
    if not dr.addUserMoney(uid, money):
        print ">>对不起，充值失败"
        return xcontinue()
    else:
        print ">>充值成功"
        return xcontinue()
    
def setSaleUserForUser():
    username =raw_input("请输入用户名 :")
    user = User._loadByUserName(username)
    if not user:
        print ">>对不起，操作失败，你指定的客户名不存在."
        return xcontinue()
        
    uid =raw_input("输入销售帐号 :")
    su = SaleUser._loadObj(uid)
    if not su:
        print ">>对不起，操作失败，你指定的销售名不存在."
        return xcontinue()
        
    user.saleUser = su
    print ">>成功分配了销售经理"
    return xcontinue()


def setIdcUserForUser():
    uid =raw_input("输入客户帐号 :")
    u = User._loadObj(uid)
    if not u:
        print ">>对不起，操作失败，你指定的客户名不存在."
        return xcontinue()
        
    uid =raw_input("输入IDC帐号 :")
    su = IdcUser._loadObj(uid)
    if not su:
        print ">>对不起，操作失败，你指定的IDC不存在."
        return xcontinue()
        
    u.idcUser = su
    print ">>成功分配了IDC"
    return xcontinue()    

def setEnginnerSkills():
    uid =raw_input("输入工程师帐号:")
    eng = EngineerUser._loadObj(uid)
    
    if not eng:
        print ">>对不起，操作失败，你指定的工程师不存在."
        return xcontinue()
    
    skills=[]
    skill = answerVal("linux", y="linux")
    if skill: skills.append(skill)
    
    skill = answerVal("windows", y="windows")
    if skill: skills.append(skill)
    
    
    eng.skills = skills
    
    print ">>成功设置工程师技能:%s" %skills
    return xcontinue()
    
    
    
def editCollector():
    uid =raw_input("输入收集器UID:")
    coll = Collector._loadObj(uid)
    exp = r"^\s*(?:(?:[1-9]?[0-9]|1[0-9]{2}|2(?:[0-4][0-9]|5[0-5]))\.){3}(?:[1-9]?[0-9]|1[0-9]{2}|2(?:[0-4][0-9]|5[0-5]))\s*$"
    if not coll:
        print ">>对不起，操作失败，你指定的Collector不存在."
        return xcontinue()
    
    title =raw_input("设置别名:")
    if title: coll.title = title
    
    host =raw_input("设置ip:")
    host = host.strip()
    if not re.match(exp, host):
        print ">>对不起，设置ip操作失败，ip地址不正确."
        return xcontinue()
    
    if Collector._loadByHost(host):
        print ">>对不起，设置ip操作失败，ip地址已经存在."
        return xcontinue()
    
    
    coll.host = host
    print ">>修改完毕."
    return xcontinue()
    
def createCollector():
    
    def getCollUid():
        index = randint(10, 10000)
        uid = "Collector_%s" %index
        if not Collector._loadObj(uid): return uid
        return getCollUid()
    
    exp = r"^\s*(?:(?:[1-9]?[0-9]|1[0-9]{2}|2(?:[0-4][0-9]|5[0-5]))\.){3}(?:[1-9]?[0-9]|1[0-9]{2}|2(?:[0-4][0-9]|5[0-5]))\s*$"
    
    coll = Collector()
    title =raw_input("设置别名:")
    if title: coll.title = title
    
    host =raw_input("设置ip:")
    host = host.strip()
    if not re.match(exp, host):
        print ">>对不起，操作失败，ip地址不正确."
        return xcontinue()
    
    if Collector._loadByHost(host):
        print ">>对不起，操作失败，ip地址已经存在."
        return xcontinue()
    
    coll.host = host
    
    uid = getCollUid()
    coll._medata["_id"] = uid
    coll._saveObj()
    print ">>收集器UID:%s     修改完毕." %(uid)
    return xcontinue()    
    
def delCollector():
    print "!!! 如果你将要删除的收集器，已经挂载了监控对象，请慎重使用此功能 !!!!"
    
    val = answerVal("继续??")
    if not val: return True
    uid =raw_input("输入收集器UID:")
    coll = Collector._loadObj(uid)
    if not coll:
        print ">>对不起，操作失败，你指定的Collector不存在."
        return xcontinue()
    
    coll.remove()
    print ">>已经成功删除收集器."
    return xcontinue()
    
#------------------------------------------------------------------------------------#
def xquit():
    print ">>已退出程序"
    sys.exit()

def answerVal(question, y=True, n=False):
    answer = raw_input(question + " ? (yes|no):")
    if answer == "yes" or answer == "y": return y
    return n

    
    
def selectMenu():
    print menus
    menu = raw_input("请选择执行的操作:")
    if menu not in functions: return selectMenu()
    return menu

def xcontinue():
    return answerVal("返回")
    
    
#------------------------------------------------------------------------------------#
    
functions={
    "a":activeUser, "q":xquit, "s":setSaleUserForUser, "i":setIdcUserForUser, 'am': addMoney,
    "es":setEnginnerSkills, "ce":editCollector, "cc":createCollector, "cd":delCollector,
}
menus="""
    a) 激活用户
    s) 为用户分配销售经理
    i) 为用户分配IDC
   am) 用户充值 
   es) 设置工程师技术技能
   ----------------------------------------
   ce) Edit Collector
   cc) Create New Collector
   cd) Del Collector
   ----------------------------------------
    q) 退出
"""



if __name__ == "__main__":
    while True:
        menu = selectMenu()
        ctu = functions[menu]()
        if not ctu: xquit()
    
    
    
    
    