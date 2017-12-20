#coding=utf-8
import time
from products.netModel.user.user import User
from products.netModel.org.webSiteClass import WebSiteClass
from products.netTasks import NetbaseSysTask

def _sysAutoClear():
    """
        系统清除用户
        没有激活且没有添加监控对象的用户的24小时清除
    """
    nowTime = time.time()
    expireTime = nowTime - 3600*24 #过期时间24小时前
    conditions = {"is_active":False, "createTime":{"$lte": expireTime}}
    users = User._findObjects(conditions=conditions)
    
    for u in users:
        c = u.ownCompany
        l=u.last_login #如果为0或者为空表示其没有登录过
        if c and not l: 
            wscs = c._getRefMeObjects("ownCompany", WebSiteClass)
            for wsc in wscs: wsc.remove()
            c.remove()

        u.remove()

class Task(NetbaseSysTask):        
    def __runService__(self):
        while True:
            _sysAutoClear()
            time.sleep(60*10) #休眠10分钟
    
    
