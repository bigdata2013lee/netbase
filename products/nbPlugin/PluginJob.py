#-*- coding:utf-8 -*-
'''
Created on 2013-3-27

@author: Administrator
'''
import os,sys
import time
import socket,ssl
from singelton import ConfigObject
from products.netUtils.xutils import nbPath as _p

class PluginJob(object):
    def loadConfig(self):
        self.task = None                 #数据搜集任务对象
        self.serverIp = "192.168.11.22"  #搜集器server IP
        self.serverPort = 8000           #搜集器server port
        self.cycleTime = 2               #定时取数据周期,建议取值为0-9 minute
        self.cycleTimeFlag = -1
        self.heartbeatCycle = 30         #心跳周期
        self.timeOut = 90                #心跳超时时间 
        self.timeOutTime = 0             #心跳超时次数
        self.lastUpdateTime = 0          #最近一次心跳时间
        self.sock = None                 #连接
        self.timeDelta = 0               #搜集器server与插件的时间差值
        self.pluginList = []
        self.conf = ConfigObject()
        self.getplugins()
    def getplugins(self):
        unloadstartflag = "W"
        if sys.platform == "win32":
            path = os.getcwd()+"\plugins"
            sys.path.append(path.replace("\\","\\"))
            unloadstartflag = "L"
        else:
            path = _p("/products/nbPlugin/plugins")
            sys.path.append(path)
        clsDict = {}
        for filename in os.listdir(path):
#        for filename in os.listdir("plugins"):
            if filename.startswith(unloadstartflag):
                continue
            if filename.endswith("_PLUGIN.py") or filename.endswith("_PLUGIN.pyc"):
                clsName = filename.split(".")[0].strip()
                if clsName not in clsDict.keys():
                    try:
                        __import__(clsName, globals(), locals(), clsName)
                        mod = sys.modules[clsName]
                        cls = getattr(mod, clsName)
                    except Exception,e:
                        continue
                    clsDict[clsName] = cls()
        self.pluginList = clsDict.values()
    def doTask(self):
        self.loadConfig()
        while self.conf.running:
            tmin = time.localtime()[4]
            if tmin%self.cycleTime == 0 and tmin != self.cycleTimeFlag and len(self.pluginList) > 0 :
                self.cycleTimeFlag = tmin
                self.doCycleJob()
            
            if self.sock is None:
                try:
                    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                    self.sock = ssl.wrap_socket(s,
                                                                   ca_certs="/root/cert.pem",
                                                                   cert_reqs=ssl.CERT_REQUIRED)
                    self.sock.connect((self.serverIp,self.serverPort))
                    self.pluginRegister()
                except Exception,e:
                    self.done()
                    time.sleep(5)
                    continue
            try:
                valueStr = self.sock.recv(1024)
                if valueStr is None or len(valueStr) == 0:
                    self.doTimeOutCheck()
                    time.sleep(10)
                    continue
                
                [self.handleMsg(msg.strip()) for msg in valueStr[2:-2].split(">><<")] 
            except Exception ,e:
                self.done()
                continue   
    
    def handleMsg(self,valueStr):
        if valueStr is None:
            return
        if valueStr.startswith("["):
            self.heartBeat(valueStr[1:-1])
        else:
            self.getValue(valueStr)
    
    def heartBeat(self,value):
        self.timeDelta = float(value) - time.time()
        self.lastUpdateTime = time.time()
        self.timeOutTime = 0
        try:
            self.sock.send("<<success>>")
        except Exception,e:
            self.done()

    def doTimeOutCheck(self):
        if time.time() - self.lastUpdateTime > self.heartbeatCycle:
            self.timeOutTime += 1
            if self.timeOutTime > 2:
                self.done()
    
    def done(self):
        if self.sock:
            self.sock.close()
            self.sock = None
    
    def pluginRegister(self):
        pgNames = []
        for plugin in self.pluginList:
            try:
                msg = plugin.getStartFlag().strip()
            except Exception,e:
                continue
            pgNames.append(msg)
            self.conf.pluginDict[msg] = plugin
            self.conf.configDict[msg] = {}
        if pgNames:
            self.sock.send("<<pluginconfig:"+str(pgNames)+">>")
    
    def getValue(self,valueStr):
        #"ptype":"SNMP","pcollector":"model","psave":True,"pvalue":None
        valueDict = eval(valueStr)
        if type(valueDict) != type({}):
            return
        
        pluginName = valueDict.get("ptype",None)
        pcollector = valueDict.get("pcollector",None)
        psave = valueDict.get("psave",True)
        pconf = valueDict.get("pvalue",[])
        if not pconf:
            return
        if self.conf.configDict.has_key(pluginName):
            result = {}
            try:
                #缓存配置信息
                if psave:
                    self.conf.configDict[pluginName] = {pcollector:pconf}
                plugin = self.conf.pluginDict.get(pluginName)
                result = plugin.getValues(pconf)
            except Exception,e:pass
            if result:
                self.handleOidValues(self.buildResultStr(pluginName, pcollector, psave, result))
                plugin.clear()
    
    def buildResultStr(self,ptype,pcollector,psave,pvalue):
        pvalueDict = {}
        resultDict = {}
        pvalueDict[time.time()+self.timeDelta] = pvalue
        resultDict["ptype"] = ptype
        resultDict["pcollector"] = pcollector
        resultDict["psave"] = psave
        resultDict["pvalue"] = pvalueDict
        return "<<"+str(resultDict).strip()+">>"
    
    def handleOidValues(self,valueStr):
        try:
            self.sock.sendall(valueStr.strip())
        except Exception,e:
            self.done()

    def doCycleJob(self):
        pvList = [(k,self.conf.pluginDict.get(k),v) for k,v in self.conf.configDict.iteritems() if v]
        for item in pvList:
            pluginName,plugin,configDict = item
            for pcollector,pconf in configDict.iteritems():
                result = plugin.getValues(pconf)
                if not result:
                    continue
                resultStr = self.buildResultStr(pluginName, pcollector, True, result)
                plugin.clear()
                clen = len(plugin.cacheMessage)
                if self.sock is None:
                    plugin.cacheMessage.append(resultStr)
                    if clen > plugin.MAX_CACHE_SIZE:
                        plugin.cacheMessage = plugin.cacheMessage[clen-plugin.MAX_CACHE_SIZE:]
                else:
                    try:
                        self.handleOidValues(resultStr)
                        if clen > 0:
                            [self.handleOidValues(cacheResult) for cacheResult in plugin.cacheMessage]
                            plugin.cacheMessage = []
                    except Exception,e:
                        self.done()