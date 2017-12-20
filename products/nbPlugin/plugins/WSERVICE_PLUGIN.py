#-*- coding:utf-8 -*-
'''
Created on 2013-3-27

@author: Administrator
'''
import os
from COLLECTBASE import COLLECTBASE

class WSERVICE_PLUGIN(COLLECTBASE):
    
    def getStartFlag(self):
        return "service"
    
    def getValues(self, configsList):
        [self.getValue(port) for port in configsList]
        return self.valueDict

    def getValue(self, conf):
        if str(conf).isdigit():
            try:
                re = os.system("netstat -ano |findstr :%d >nbtmp.txt"%conf)
            except Exception,e:pass
            if re == 0:
                lines = [line.strip() for line in open('nbtmp.txt','r').readlines()]
                pidList = [line.split(" ")[-1] for line in lines]
                os.system("sc queryex >nbtmp.txt")
                sevStr = open('nbtmp.txt','r').read().strip()
                pidStr = ",".join([sev.split("\n")[9] for sev in sevStr.split("SERVICE_NAME:") if sev])
                def getStatus(pid):
                    if pidStr.find(pid) > 0:
                        self.valueDict[conf] = True
                    else:
                        self.valueDict[conf] = False
                [getStatus(pid) for pid in pidList]
            else:
                self.valueDict[conf] = False