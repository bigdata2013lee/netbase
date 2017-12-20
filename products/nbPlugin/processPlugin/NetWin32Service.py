#-*- coding:utf-8 -*-
import win32serviceutil
import win32service
import win32event
from twisted.internet import reactor
from pluginTcpServer import PluginFactory

class win32test(win32serviceutil.ServiceFramework):    
    _svc_name_ = "NetWin32Service"     
    _svc_display_name_ = "NetWin32Service"     
    _svc_description_ = "NetWin32Service." 

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
       
    def SvcDoRun(self):
        reactor.listenTCP(12368, PluginFactory())
        reactor.run()
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
       
    def SvcStop(self):
        reactor.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop) 

if __name__=='__main__':
    win32serviceutil.HandleCommandLine(win32test)