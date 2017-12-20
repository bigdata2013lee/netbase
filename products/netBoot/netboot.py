#coding=utf-8
import time
import socket
import pickle
import binascii
from twisted.internet import reactor, protocol,ssl
from twisted.internet.protocol import Protocol
from products.dataCollector.redisManager import RedisManager
from products.netUtils.deamonBase import DeamonBase
from products.netUtils.settings import CollectorSettings
from products.netBoot.bootIpmi import BootIpmiTask
import logging
from products.netUtils.xutils import nbPath as _p
log = logging.getLogger("netBoot")
class BootTask(RedisManager):
    """
    netbase开机任务
    """
    def __init__(self,cuid):
        """
        初始化函数
        """
        self.cuid=cuid

    def htonet(self,hexnumber):
        """
        构建包
        """  
        chset = []
        for i in xrange(0, len(hexnumber), 2):
            ch = binascii.unhexlify(hexnumber[i:i+2])
            chset.append(ch)
        return "".join(chset)
        
    def wakeOnLan(self,macaddress):
        """
        唤醒对应的物理地址设备
        ＠macaddress:设备物理地址
        """
        send_data  = self.htonet("FF")*6 + self.htonet(macaddress)*16
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.sendto(send_data, ('255.255.255.255', 7))
        sock.close()
    
    def macFormat(self,macaddress):
        """
        物理地址格式判断
        """
        if len(macaddress)==12:pass
        elif len(macaddress) == 12 + 5:
            sep = macaddress[2]
            macaddress = macaddress.replace(sep,'').strip()
        else:
            return None
        return macaddress
    
    def startBoot(self,uid,title,manageIp,macaddress,componentType,tries=1):
        """
        开始开机
        """
        if macaddress:
            macaddress=self.macFormat(macaddress)
            if macaddress:
                for i in xrange(tries):
                    self.wakeOnLan(macaddress)
                severity=2
                message="%s 设备%s使用开机助手进行开机!"%(time.asctime(),manageIp)
            else:
                severity=3
                message="物理地址格式错误,开机失败!"%(time.asctime(),manageIp)
        else:
            severity=4
            message="物理地址不存在,开机失败!"%(time.asctime(),manageIp)
        data = {
          'moUid':uid,
          'title':title,
          "componentType":componentType,
          "message":message,
          "severity":severity,
          "collector":self.cuid,
          "agent":"netboot"
        }
        self.saveEvent(data)



class BootProtocol(Protocol):
    """
    开机协议
    """
    def connectionMade(self):
        self.transport.client
    
    def connectionLost(self, reason):
        self.transport.client
        
    def dataReceived(self, data):
        data=pickle.loads(data)
        bootType=data.keys()[0]
        objData=data.values()[0]
        uid=objData.get("uid")
        title=objData.get("title")
        cuid=objData.get("collector")
        netIpmiIp=objData.get("netIpmiIp")
        netIpmiUserName=objData.get("netIpmiUserName")
        netIpmiPassword=objData.get("netIpmiPassword")
        componentType=objData.get("componentType")

        ipmit=BootIpmiTask(cuid,uid,netIpmiIp,netIpmiUserName,netIpmiPassword,title,componentType)
        if hasattr(ipmit,bootType):
            rs=getattr(ipmit, bootType)()
            self.transport.write(str(rs))
        self.transport.loseConnection()
                
            
class BootFactory(protocol.Factory):
    """
    Tcp协议工厂
    """
    protocol = BootProtocol

class netboot(DeamonBase):
    """
    自动开机
    """
    def __init__(self):
        """
        初始化函数
        """
        DeamonBase.__init__(self)
        self.port=CollectorSettings.getSettings().getAsInt("remoteBoot", "bootPort")
        
    def run(self):
        """
                调用开机命令
        """
        sslContext=ssl.DefaultOpenSSLContextFactory(_p('/bin/privkey.pem'),_p('/bin/cacert.pem'))
        factory = BootFactory()
        reactor.listenSSL(self.port,factory,contextFactory=sslContext)
        log.info("启动自动开机守护进程!")
        reactor.run()

if __name__ == '__main__':
    nboot=netboot()
    nboot.run()
