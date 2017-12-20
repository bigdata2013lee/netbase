#-*- coding:utf-8 -*-
'''
Created on 2013-3-27

@author: root
'''
import os
from COLLECTBASE import COLLECTBASE

class LSERVICE_PLUGIN(COLLECTBASE):
    def getStartFlag(self):
        return "service"
    
    def getValues(self, configsList):
        [self.getValue(port) for port in configsList]
        return self.valueDict
    
    def getValue(self, conf):
        if str(conf).isdigit():
            try:
                re = os.system("netstat -ano |grep ':\*' >nbtmp.txt")
            except Exception,e:pass
            if re == 0:
                lines = open('nbtmp.txt','r').read()
                if lines.find(":%d"%conf) > 0:
                    self.valueDict[conf] = True
                else:
                    self.valueDict[conf] = False
            else:
                self.valueDict[conf] = False
                
