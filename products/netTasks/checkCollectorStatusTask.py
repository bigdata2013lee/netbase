#coding=utf-8
import time
import socket
from products.netModel.collector import Collector
from products.netTasks import NetbaseSysTask

def _sysAutoCheck():
    collectors = Collector._findObjects()
    tryTimes =2
    timeout = 5
    
    for coll in collectors:
        for port in [coll.tcpServerPort, coll.bootpoPort]:
            for i in xrange(tryTimes):
                try:
                    s=socket.socket()
                    s.settimeout(timeout)
                    status = s.connect_ex((coll.host,port))
                    if status == 0:
                        coll.status = True
                        break
                    else:
                        coll.status = False
                finally:
                    s.close()
            if coll.status:break
        coll._saveObj()

class Task(NetbaseSysTask):      
    def __runService__(self):
        while True:
            _sysAutoCheck()
            time.sleep(60*10) #休眠10分钟
    
    

    
