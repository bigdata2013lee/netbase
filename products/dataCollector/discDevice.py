#coding=utf-8
from pynetsnmp.twistedsnmp import AgentProxy
from twisted.internet import reactor
from twisted.internet.defer import Deferred
from products.netUtils.driver import drive
from products.netUtils.netJobs import NetJobs
from twisted.python.failure import Failure
from twisted.internet.defer import succeed
from products.netPing.AsyncPing import Ping
class SnmpConfig(object):
    succeeded = None
    def __init__(self,ip,community):
        """
                初始化方法
        """
        self.ip=ip
        self.community=community
        
    def getAgentProxy(self):
        """
                得到SNMP代码
        """
        return AgentProxy(
            ip=self.ip,
            port=161,
            timeout=3,
            tries=2,
            snmpVersion="v2c",
            community=self.community)

    def snmpGet(self,oid="1.3.6.1.2.1.1.5.0"):
        """
        SNMP获取值
        """
        self.proxy = self.getAgentProxy()
        self.proxy.open()
        d=self.proxy.get([oid])
        return d.addBoth(self.snmpResults)

    def snmpResults(self, result):
        """
        SNMP结果
        """
        self.proxy.close()
        if isinstance(result, dict) and bool(result):
            self.succeeded = True
        else:
            self.succeeded = False
        return self
        
class SnmpAgentDiscoverer(object):
    """
    SNMP代理自动发现
    """
    __snmpResult ={}
    def findBestConfig(self, configs):
        self._d = Deferred()
        self._pending =[]
        for c in configs:
            self._pending.append(c.ip)
            ds=c.snmpGet()
            ds.addBoth(self._handleResult)
        return self._d
    
    def _handleResult(self,result):
        """
                处理结果
        """
        ip=result.ip
        self.__snmpResult=(ip,False)
        self._pending.remove(ip)
        if not self._d.called:
            if result.succeeded:
                self.__snmpResult=(ip,True)
                self._d.callback(self.__snmpResult)
            elif len(self._pending)==0:
                self._d.callback(self.__snmpResult)

class PingConfig(object):
    def __init__(self,deviceIp):
        """
                初始化Ping配置对象
        """
        self.deviceIp=deviceIp
        self.deviceId=deviceIp
        self.hcType="ping"
        self.devicePort = 22
        self.title = deviceIp
        self.cuid="localhost"
        self.componentType="Device"

class DiscDevice(object):
    """
        自动发现设备
    """
    maxLoadCount=50
    def __init__(self,dataCollector,ips,communities):
        """
                初始化方法
        """
        self.ips=ips
        print ips,communities
        self.ping=Ping()
        self.communities=communities
        self.dataCollector=dataCollector
    
    def startDiscover(self):
        """
                开始自动发现
        """
        d = drive(self.discoverDevice)
        d.addBoth(self.processResults)
    
    def discoverDevice(self,driver):
        """
                自动发现设备
        """
        yield self.discoverIps()
        ips = driver.next()
        yield self.discoverSnmpInfo(ips)
        driver.next()

    def discoverIps(self):
        """
                自动发现IP(通过网段)
        """
        def inner(driver):
            yield NetJobs(self.maxLoadCount,
                        self.ping.ping,
                        self.getConfigIps()).start()
            results = driver.next()
            goodips = [v.ipaddr for v in results if not isinstance(v, Failure)]
            yield succeed(goodips)
            driver.next()
        d = drive(inner)
        return d
    
    def getConfigIps(self):
        """
                得到配置IP
        """
        return [PingConfig(ip) for ip in self.ips]
        
    def discoverSnmpInfo(self,ips):
        """
                自动发现SNMP信息
        """
        return NetJobs(self.maxLoadCount,
                          self.testSnmp,
                          ips).start()
    
    def testSnmp(self,ip):
        """
                测试SNMP状态
        """
        sad=SnmpAgentDiscoverer()
        def inner(driver):
            configs = []
            for community in self.communities:
                configs.append(SnmpConfig(ip,community))
            yield sad.findBestConfig(configs)
            driver.next()
        return drive(inner)
    
    def processResults(self,results):
        """
                处理结果
        """
        self.dataCollector.transportWrite({"message":"自动发现%s个IP"%len(results),"data":dict(results)})
        self.dataCollector.transport.loseConnection()

if __name__=="__main__":
    dle=DiscDevice("192.168.2.0/24",["public"])
    dle.startDiscover()
    reactor.run()
        