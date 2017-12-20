#coding=utf-8
import sys
import pickle
import re
from twisted.internet.protocol import Protocol
from twisted.internet import reactor, protocol


class CmdObj(object):
    
    def __init__(self, cId, cmdName, vars):
        self.cId = cId
        self.cmdName = cmdName
        self.vars = vars
        
class cmdRs():
    def __init__(self, cId, rs):
        self.cId = cId
        self.rs = rs
#----------------------------------------------------------#        
class ProtocolA(Protocol):

    def connectionLost(self, reason):
        pass
    
    def connectionMade(self):
        pass
       
    
    def dataReceived(self,data):
        collId = pickle.loads(data)
        cmdObj = self.factory.server.getCmd(collId)
        if not cmdObj: 
            print "没有你的命令！" 
            return
        print "cmdObj.cId:%s" %cmdObj.cId
        self.factory.server.sendCmd(self.transport,cmdObj)
        
class ProtocolB(Protocol):

    def connectionLost(self, reason):
        pass
    
    def connectionMade(self):
        pass
       
    
    def dataReceived(self,data):
        cmdRs = pickle.loads(data)
        self.factory.server.saveResult(cmdRs)
    
class ProtocolC(Protocol):

    def connectionLost(self, reason):
        print  "ProtocolC connectionLost"
    
    def connectionMade(self):
        print  "ProtocolC connectionMade"
       
    
    def dataReceived(self,data):
        cmdObj = pickle.loads(data)
        self.factory.server.addCmd(cmdObj)
        self.transport.loseConnection()
        print "finished!C"
#----------------------------------------------------------#
class FactoryA(protocol.Factory):
    
    protocol = ProtocolA  
    

class FactoryB(protocol.Factory):
    
    protocol = ProtocolB 
    
    
class FactoryC(protocol.Factory):
    
    protocol = ProtocolC     
    
    
        
        
        

class NetbaseConfigServer(object):
    
    def __init__(self, host="0.0.0.0", portA=13520, portB=13521, portC=13522):
        self.host = host
        self.portA = portA
        self.portB = portB
        self.portC = portC
        self.cmdDict = {"coll001:001": CmdObj("coll001:001", "sum", [1,2,3]), 
                        "coll001:002": CmdObj("coll001:002", "sum", [1,2,3,4])}
    
    def addCmd(self, cmdObj):
        self.cmdDict[cmdObj.cId]  = cmdObj
        
    
    def getCmd(self, collId):
        
        for key in self.cmdDict.keys():
            if key.find("%s:" %collId) == 0:
                cmdObj = self.cmdDict[key]
                del self.cmdDict[key]
                return cmdObj
            
        return None
    
    def sendCmd(self, transport, cmdObj):
        data = None
        try:
            data = pickle.dumps(cmdObj)
        except:
            print " pickle error "
            
        if data:
            transport.write(data)
                
    
    def saveResult(self, cmdRs):
        print cmdRs.rs
    
    def doListenTcp(self):
        fa = FactoryA()
        fb = FactoryB()
        fc = FactoryC()
        
        fa.server = self
        fb.server = self
        fc.server = self
        
        ca = reactor.listenTCP(self.portA, fa)
        cb = reactor.listenTCP(self.portB, fb)
        cc = reactor.listenTCP(self.portC, fc)
        
        print 'Serving NetbaseConfigServer start on %s.' % (ca.getHost())
        print 'Serving NetbaseConfigServer start on %s.' % (cb.getHost())
        print 'Serving NetbaseConfigServer start on %s.' % (cc.getHost())
        
        
    def run(self):
        self.doListenTcp()
        reactor.run()
        

if __name__ == "__main__":
    
    NetbaseConfigServer().run()