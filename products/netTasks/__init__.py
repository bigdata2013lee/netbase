#coding=utf-8
from threading import Thread

class NetbaseSysTask(object):
    
    def execTask(self):
        th = Thread(target=self.__runService__)
        th.setDaemon(True)
        th.start()
        
