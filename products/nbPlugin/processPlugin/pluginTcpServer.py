#coding=utf-8
import pickle
from twisted.internet import protocol
from twisted.internet.protocol import Factory
from processOperation import ProcessOperation
class PluginProtocol(protocol.Protocol):
    """
        插件协议类
    """
    def connectionMade(self):
        if self.factory.numConnections>=self.factory.maxConnections:
            self.connectionLost("连接数过大,请稍后连接!")
        self.factory.numConnections += 1
         
    def dataReceived(self,data):
        """
                接收数据
        """
        data=pickle.loads(data)
        processName=data.get("proName")
        proType=data.get("proType")
        hostName=data.get("hostName")
        userName=data.get("userName")
        password=data.get("password")
        po=ProcessOperation(hostName,userName,password)
        if proType=="up":
            rs=po.createProcess(processName)
        else:
            rs=po.shutdownProcess(processName)
        self.transport.write(rs)

    def connectionLost(self, reason):
        self.factory.numConnections -= 1

class PluginFactory(Factory):
    """
        插件工厂
    """
    maxConnections = 100
    protocol = PluginProtocol
    def __init__(self):
        self.numConnections = 0
