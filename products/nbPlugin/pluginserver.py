#coding=utf-8
import ssl
import time
import pickle
import os, socket
from twisted.internet import reactor,protocol,defer
from products.nbPlugin.taskmanage import TaskManage
from products.rpcService.client import Client
from products.netUtils.logger import Logging
from products.netUtils.xutils import nbPath as _p
log=Logging.getLogger("pluginsnmpserver")

class SnmpTcpProtocol(protocol.Protocol):
    """
    snmpTcp协议
    """
    bufferData=""
    ipAddress=""
    connInterval = 10
    timeout = connInterval*2
    cfgInterval=0

    def __init__(self):
        """
        初始化
        """
        self.timeout_deferred=None
        self.started = False
        self.taskList=[]

    def connectionLost(self, reason):
        """
        失去连接,客户端没断开一个链接，总连接数-1
        """
        protocol.Protocol.connectionLost(self, reason)
        self.factory.number_of_connections -= 1
        
    def connectionMade(self):
        """
        连接模式,如果服务器连接数超过最大连接数，拒绝新链接建立
        """
        #获取客户端的IP和端口
        #openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout cert.pem
        self.ipAddress,port=self.transport.client
        self.transport = ssl.wrap_socket(self.transport, 
                                                               keyfile="/root/key.pem", 
                                                               certfile="/root/cert.pem", 
                                                               server_side=True,
                                                               ssl_version=ssl.PROTOCOL_SSLv23)
        #验证设备
        devexist=self.connVerification()
        if not devexist:
            self.transport.loseConnection()
            return
        #检查最大连接数
        if self.factory.number_of_connections >= self.factory.max_connections:
            self.transport.write('Too many connections, try again later')
            self.transport.loseConnection()
            return
        
        #开始连通性检测
        self.start()
        self.factory.number_of_connections += 1
        self.timeout_deferred = reactor.callLater(self.timeout, self.loseConnection)

    def dataReceived(self,data):
        """
        接收数据,如果收到的是'start'命令,开始获取配置,否则解析获取的OID数据并放入redis中
        """
        data = data.strip()
        #测试连接是否成功
        if data.startswith("<<success>>"):
            self.connectSucceed()
        #发送的配置类型
        elif data.find("<<pluginconfig")>=0:
            self.started=True
            self.taskList=eval(data.split(":")[1][:-2])
        else:
            self.bufferData+=data
            if self.bufferData.endswith(">>"):
                self.processData()
                self.bufferData=""
        #每次执行完客户端请求后重置timeout，重新开始计算无操作时间.
        if self.timeout_deferred:
            self.timeout_deferred.cancel()
            self.timeout_deferred = reactor.callLater(self.timeout, self.loseConnection)
            
    def modelDevice(self):
        """
        读文件,判断是否需要模型化设备
        """
        f=open(_p("/model.txt"),"r")
        rs=f.read()
        f.close()
        if rs.strip()==self.ipAddress:
            return True
        return False
        
    def processData(self):
        """
        处理数据格式
        """
        self.bufferData=self.bufferData[2:-2]
        dataList=self.bufferData.split(">><<")
        for datars in dataList:
            if not hasattr(self,"tm"):self.start()
            try:
                datars=eval(datars)
                tasktype=datars.get("pcollector","")
                taskrs=datars.get("pvalue",{})
                self.tm.getTaskObj(tasktype).processResult(self.ipAddress,taskrs)
            except Exception,ex:
                self.processError(taskrs)
    
    def processError(self,taskrs):
        """
        处理失败
        """
        log.error("设备%s上数据%s转换失败,请联系管理员解决!"%(self.ipAddress,taskrs))
    
    def loseConnection(self):
        """
        twisted框架,连接断开后处理函数
        """
        self.bufferData = ""
        self.connectFail()
        if hasattr(self,"send_defered"):
            if self.send_defered:self.send_defered.cancel()
        self.transport.loseConnection()
    
    def start(self):
        """
        客户端开始连接服务器
        """
        self.sendTime()
        
    def connVerification(self):
        """
        连接验证,验证该客户端设备是否为监控设备
        """
        self.tm=TaskManage(self.factory.rpyc)
        self.tm.startRegist()
        devexist=self.tm.getTaskObj("status").getDeviceConfig(self.ipAddress)
        return devexist
        
    def sendTime(self):
        """
        发送当前时间,检测连通性
        """
        self.transport.write("<<[%s]>>"%time.time())
        if self.modelDevice():
            interface=self.tm.getTaskObj("interface")
            filesystem=self.tm.getTaskObj("filesystem")
            self.transport.write("<<%s>>"%interface.getDeviceConfig())
            self.transport.write("<<%s>>"%filesystem.getDeviceConfig())
        self.send_defered=reactor.callLater(self.connInterval, self.sendTime)
        
    def connectFail(self):
        """
        连接失败
        """
        self.started=False
        msg="连接设备%s失败"%(self.ipAddress)
        self.tm.getTaskObj("status").processEvents(5,msg)
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        
    def connectSucceed(self):
        """
        连接成功,开始发送配置
        """
        if self.started:
            self.sendConfig()
        msg="连接设备%s成功"%(self.ipAddress)
        self.tm.getTaskObj("status").processEvents(0,msg)
        log.info("设备%s连接正常"%self.ipAddress)

    def sendConfig(self):
        """
        发送设备配置信息
        """
        self.cfgInterval+=self.connInterval
        if not self.ipAddress:return
        for tasktype in self.taskList:
            deviceConfig=self.tm.getTaskObj(tasktype).getDeviceConfig(self.ipAddress)
            if not deviceConfig:continue            
            deviceConfig.update({"ptype":tasktype})
            self.transport.write("<<%s>>"%(deviceConfig))
        log.info("开始发送设备%s配置信息"%self.ipAddress)

class SnmpTcpFactory(protocol.Factory):
    """
    SnmpTcp工厂
    """
    protocol = SnmpTcpProtocol
    #最大链接数
    max_connections = 1000
    def __init__(self):
        self.number_of_connections = 0
        self.rpyc = Client()

class PluginSnmpServer():
    """
    snmp数据接收程序
    """
    port=8000

    def __init__(self):
        """
        功能:初始化snmp收集器插件守护进程
        """
        pass
        
    def  doListen(self):
        """
        开始监听
        """
        factory=SnmpTcpFactory()
        reactor.listenTCP(self.port, factory)
        
    def run(self):
        """
        功能:启动
        """
        self.doListen()
        reactor.run()

if __name__=="__main__":
    pss=PluginSnmpServer()
    pss.run()
