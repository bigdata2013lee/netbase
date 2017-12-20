#coding=utf-8
import sys
import pickle
import re
import socket
from twisted.internet.protocol import Protocol
from twisted.internet import reactor, protocol
from twisted.internet.protocol import ReconnectingClientFactory

class CmdObj(object):
    
    def __init__(self, cId, cmdName, vars):
        self.cId = cId
        self.cmdName = cmdName
        self.vars = vars
        
class cmdRs():
    def __init__(self, cId, rs):
        self.cId = cId
        self.rs = rs
        
class ClientProtocol(Protocol):
    
    def connectionLost(self, reason):
        print "connection is lost! %s" %reason
        
        #ReconnectingClientFactory.clientConnectionLost(self, connector, unused_reason)  
        
    
    def connectionMade(self):
        print "start connection the server!"
        self.factory.look(self.transport)
    
    
    def dataReceived(self, data):
        cmdObj = pickle.loads(data)
        if not cmdObj: print "服务器已没有属于你的命令!"
        else:
            print "从服务器获取命令：%s" %str(cmdObj)
            cmdRs = self.factory.serClient.execCMD(cmdObj)
            self.factory.serClient.returnCMDResult(cmdRs)
        
        
class ClientFactory(ReconnectingClientFactory):
    
    protocol = ClientProtocol

    def __init__(self, collId):
        self.collId = collId
        self.maxDelay = 30
        
    def clientConnectionLost(self, connector, unused_reason):
        print "连接服务器丢失，原因是：%s 尝试再去连接！" %str(unused_reason)
        ReconnectingClientFactory.clientConnectionLost(self, connector, unused_reason)
    
    def clientConnectionFailed(self, connector, reason):
        print "..........%s" %self.initialDelay
        print "连接服务器失败，原因是：%s 尝试再去连接！"  %str(reason)
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
        
    def look(self, transport):
        transport.write(pickle.dumps(self.collId))
        reactor.callLater(2, self.look, transport)
    

    

class NetConfigServerClient(object):
    
    def __init__(self, collId, host="192.168.2.104",portA=13520, portB=13521):
        self.collId = collId
        self.host = host
        self.portA = portA
        self.portB = portB
        self.factory = None
    
    
    def _getSocket(self):
        TCPClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TCPClient.settimeout(30)
        TCPClient.connect((self.host, self.portB))
        return TCPClient
    
    def execCMD(self, cmdObj):
        rs = cmdRs(cmdObj.cId, exceMyCmd(cmdObj))
        return rs
    
    
    def returnCMDResult(self, rs):
        _rs = pickle.dumps(rs)
        sc = self._getSocket()
        sc.send(_rs)
        sc.close()
    
    
    def connNCS(self, timeout=30):
        self.factory = ClientFactory(self.collId)
        self.factory.serClient = self
        reactor.connectTCP(self.host, self.portA, self.factory,  timeout=timeout)
        reactor.run()
    



def exceMyCmd(cmdObj):
    return "%s = %s" %(cmdObj.cmdName, sum(cmdObj.vars))  

if __name__ == "__main__":
    NetConfigServerClient("coll001").connNCS()
    