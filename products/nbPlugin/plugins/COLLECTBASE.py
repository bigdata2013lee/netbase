#-*- coding:utf-8 -*-
'''
Created on 2013-3-26

@author: Administrator
'''
class COLLECTBASE(object):
    valueDict = {}
    cacheMessage = []
    MAX_CACHE_SIZE = 60
    
    def getStartFlag(self):
        "plugin start falag"
        return None
    
    def getValues(self,configsList):
        "parse string to config"
        return self.valueDict
    
    def getValue(self,conf):
        "get single config value to valueDict"
    
    def clear(self):
        self.valueDict.clear()