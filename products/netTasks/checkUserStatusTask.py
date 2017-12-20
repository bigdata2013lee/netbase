#coding=utf-8
import time
from products.netTasks import NetbaseSysTask



def _sysAutoCheck():
    pass

class Task(NetbaseSysTask):
    def __runService__(self):
        while True:
            hour = time.localtime().tm_hour
            if hour == 6:
                _sysAutoCheck()
            time.sleep(60*60) #休眠
    
