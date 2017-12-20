#-*- coding:utf-8 -*-
'''
Created on 2013-3-26

@author: Administrator
'''
import win32serviceutil
import win32service
import win32event
import threading
from singelton import ConfigObject
from PluginJob import PluginJob

class win32test(win32serviceutil.ServiceFramework):    
    _svc_name_ = "PythonWin32Service"     
    _svc_display_name_ = "PythonWin32Service"     
    _svc_description_ = "PythonWin32Service." 

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)         
        self.conf = ConfigObject()
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
    
    def SvcDoRun(self):
        self.task = threading.Thread(target=PluginJob().doTask)
        self.task.start()
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

    def SvcStop(self):
        self.conf.running = False
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)         
        win32event.SetEvent(self.hWaitStop)

if __name__=='__main__':
    win32serviceutil.HandleCommandLine(win32test)