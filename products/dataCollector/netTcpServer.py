#coding=utf-8
import sys
import pickle
from twisted.internet import reactor,protocol,ssl
from twisted.internet.protocol import Protocol
from products.netUtils.deamonBase import DeamonBase
from products.netUtils.settings import CollectorSettings
from products.dataCollector.collectModel import CollectModel
import logging
from products.netUtils.xutils import nbPath as _p
log = logging.getLogger("netTcpServer")

class NetTcpProtocol(Protocol):
    """
    TCP协议
    """
    def connectionLost(self, reason):
        """
                失去连接,客户端没断开一个链接，总连接数-1
        """
        protocol.Protocol.connectionLost(self, reason)
        self.factory.num_connection -= 1

    def connectionMade(self):
        """
        连接模式,如果服务器连接数超过最大连接数，拒绝新链接建立
        """
        #检查最大连接数
        if self.factory.num_connection >= self.factory.max_connections:
            self.transport.write(pickle.dumps({"message":"当前连接数比较多,请稍后连接!","data":[]}))
            self.transport.loseConnection()
            return
        #开始连通性检测
        self.factory.num_connection += 1
        
    def dataReceived(self,data):
        """
                接收数据
        @data:字典格式数据
        """
        data=pickle.loads(data)
        log.info("%s" %data.get("clsName",''))
        if data.get("clsName","") == "CollVerify":
            CollectModel(self.transport,self.factory).isCollector()
        elif data.get("clsName","") == "PingSnmp":
            CollectModel(self.transport,self.factory).checkPingAndSnmpStatus(data)
        elif data.get("clsName","") == "SaveCollUid":
            CollectModel(self.transport,self.factory).saveCollectorUid(data)
        elif data.get("clsName","")=="ShortcutCmd":
            CollectModel(self.transport,self.factory).executeSshCmd(data)
        elif data.get("clsName","")=="discoverDevice":
            CollectModel(self.transport,self.factory).discoverDevice(data)
        else:
            CollectModel(self.transport,self.factory).collectDevice(data)

        
class NetTcpFactory(protocol.Factory):
    """
    Tcp协议工厂
    """
    protocol = NetTcpProtocol
    #最大链接数
    max_connections = 100
    def __init__(self,rpyc):
        self.num_connection = 0
        self.rpyc=rpyc

class NetTcpServer(DeamonBase):
    """
    TCP服务器
    """
    
    def __init__(self):
        """
        初始化函数
        """
        DeamonBase.__init__(self)
        self.port=CollectorSettings.getSettings().getAsInt("tcpServer", "tcpPort")

    def  doListen(self):
        """
        开始监听
        """
        sslContext=ssl.DefaultOpenSSLContextFactory(
                                    _p("/bin/privkey.pem"),
                                    _p("/bin/cacert.pem"))
        factory=NetTcpFactory(self.rpyc)
        log.info("开始监听%s端口!"%self.port)
        reactor.listenSSL(self.port,factory,contextFactory=sslContext)
        
    def run(self):
        """
                功能:启动
        """
        self.doListen()
        log.info("启动获取配置守护进程!")
        reactor.run()

if __name__ == '__main__':
    nts=NetTcpServer()
    nts.run()
