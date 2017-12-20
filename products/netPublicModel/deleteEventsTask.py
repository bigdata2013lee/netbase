#coding=utf-8
import time
from threading import Thread
from products.netEvent.event import Event
from products.netModel.user.user import User
from products.netUtils.settings import ManagerSettings

settings = ManagerSettings.getSettings()

def _sysAutoDeleteEvents():
    users = User._findObjects()
    for user in users:
        limit = int(settings.get("eventsLimit",user.status))
        company = user.ownCompany
        if company:companyUid = company.getUid()
        conditions = {"companyUid":companyUid}
        events = Event._findObjects(conditions=conditions,skip=limit)
        for event in events:
                event.remove()
                
                
def runService():
    
    def target():
        while True:
            hour = time.localtime().tm_hour
            if hour == 2:
                _sysAutoDeleteEvents()
            time.sleep(60*60) #休眠
    
    th = Thread(target=target)        
    th.setDaemon(True)
    th.start()

if __name__=="__main__":

    _sysAutoDeleteEvents()