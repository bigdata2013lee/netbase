#coding=utf-8
##########################################################################
#
#
#此软件版权为深圳商之杰科技有限公司所有,更多信息请访问www.netbase.asia
#
#
#
###########################################################################

__doc__= """
配置获取和更新进程
"""
import time
import types
import DateTime
from random import randint
import os
import pysamba.twisted.reactor
from twisted.internet import reactor,defer
from twisted.internet.defer import succeed
from twisted.python.failure import Failure
from products.rpcService.client import Client
from products.dataCollector.redisManager import RedisManager
from products.netRRD.wmiClient import WMIClient
from products.netUtils.driver import drive, driveLater,Driver
from products.dataCollector.pythonClient   import PythonClient
from products.dataCollector.sshClient  import SshClient
from products.dataCollector.telnetClient  import TelnetClient
from products.dataCollector.snmpClient  import SnmpClient
from products.dataCollector.portscanClient import PortscanClient                   
from products.netUtils.logger import Logging
from products.netUtils import xutils
from products.netUtils.deamonBase import DeamonBase
log = Logging.getLogger("NetModel")

defaultPortScanTimeout = 5
defaultParallel = 100
defaultProtocol = "ssh"
defaultPort = 22

class NetModel(RedisManager,DeamonBase):
    """
    构建配置模型的守护进程类
    """

    name = 'NetModel'
    generateEvents = True
    configCycleInterval = 360
    classCollectorPluginList = []
    classCollectorPlugins = ()

    def __init__(self, single=False ):
        """
        初始化
        @param single: 是否收集单一的设备
        @type single: 布尔类型
        """
        DeamonBase.__init__(self,"netmodel.xml")
        self.start = None
        self.single = single
        if self.options.device:
            self.single = True
        self.modelerCycleInterval = self.options.cycletime
        self.collage = float( self.options.collage ) / 1440.0
        self.rpyc = Client(hostName="192.168.1.89")
        self.clients = []
        self.finished = []
        self.devicegen = None
        
        self.started = False
        self.stopped =False
        self.startDelay = 0
        if self.options.daemon:
            if self.options.now:
                log.debug("以守护进程运行,立即开始.")
            else:
                self.startDelay = randint(10, 60) * 1
                log.info("以守护进程运行, 等待%s后开始" %
                              self.startDelay)
        else:
            log.debug("在前台运行, 立即开始.")

    def reportError(self, error):
        """
        错误报告
        @param error: 错误信息
        """
        log.error("发生错误: %s", error)

    def connected(self):
        """
        连接
        """
        d = defer.maybeDeferred(self.getClassCollectorPlugins)
        d.addCallback(self.startCycle)
        d.addErrback(self.reportError)

    def startCycle(self,ignored=None):
        """
        开始循环检测
        """
        ARBITRARY_BEAT = 30
        reactor.callLater(ARBITRARY_BEAT, self.startCycle)
        if not self.started:
            self.started = True
            reactor.callLater(self.startDelay, self.main)

    def getClassCollectorPlugins(self):
        """
        获取设备的收集器插件
        """
        modelPath = " products.dataCollector.plugins"
        clsDict = {}
        for filename in os.listdir("plugins"):
            if filename.endswith("Map.py") or filename.endswith("Map.pyc"):
                clsName = filename.split(".")[0]
                if clsName not in clsDict.keys():
                    lis = modelPath.split(".")
                    lis.append(clsName)
                    clsModelPath = ".".join(lis)
                    try:
                        cls = xutils.importClass(clsModelPath.strip(),clsName)
                    except :
                        log.error("搜集器插件%s实例化失败"%clsName)
                        continue
                    clsDict[clsName] = cls()
        self.classCollectorPluginList =  clsDict.values()
        return self.classCollectorPluginList

    def selectPlugins(self, device, transport):
        """
        构建收集器列表
        """
        plugins = []
        valid_loaders = []
        for plugin in self.classCollectorPluginList:
            try:
                if plugin.transport == transport:
                    log.debug( "已加载插件 %s" % plugin.name() )
                    plugins.append( plugin )
                    valid_loaders.append( plugin )
            except (SystemExit, KeyboardInterrupt), ex:
                log.info( "被外部信号(%s)中断" % str(ex) )
                raise
            except :
                info= "加载插件出现问题,插件: %s"%plugin.name()
                log.info( info ) 

        if len( self.classCollectorPluginList ) != len( valid_loaders ):
            device.plugins= valid_loaders

        collectTest = lambda x: False
        ignoreTest = lambda x: False
#        if self.options.collectPlugins:
#            collectTest = re.compile(self.options.collectPlugins).search
#        elif self.options.ignorePlugins:
#            ignoreTest = re.compile(self.options.ignorePlugins).search

        result = []
        for plugin in plugins:
            if plugin.transport != transport:
                continue
            result.append(plugin)
        return result

    def collectDevice(self, device):
        """
        收集设备的数据
        """
        clientTimeout = getattr(device, 'netCollectorClientTimeout', 180)
        ip = device.manageIp
        timeout = clientTimeout + time.time()
        self.wmiCollect(device, ip, timeout)
        self.pythonCollect(device, ip, timeout)
        self.cmdCollect(device, ip, timeout) 
        self.snmpCollect(device, ip, timeout)
        self.portscanCollect(device, ip, timeout)
        
    def wmiCollect(self, device, ip, timeout):
        """
        wmi数据收集
        """
        client = None
        try:
            plugins = self.selectPlugins(device, 'wmi')
            if not plugins:
                log.info("在设备%s上没有发现WMI插件" % ip)
                return
            if self.checkCollection(device):
                log.info('在设备%s使用WMI收集方式' % ip)
                log.info("插件: %s",
                        ", ".join(map(lambda p: p.name(), plugins)))
                client = WMIClient(device, self, plugins)
            if not client or not plugins:
                log.warn("WMI收集器创建失败")
                return
        except (SystemExit, KeyboardInterrupt):
            raise
        except Exception:
            log.exception("打开WMI收集器失败")
        self.addClient(client, timeout, 'WMI', device.id)

    def pythonCollect(self, device, ip, timeout):
        """
        python数据收集
        """
        client = None
        try:
            plugins = self.selectPlugins(device, "python")
            if not plugins:
                log.info(" 在设备%s上没有发现python收集器插件" % ip)
                return
            if self.checkCollection(device):
                log.info('Python收集器device %s' % ip)
                log.info("插件: %s",
                        ", ".join(map(lambda p: p.name(), plugins)))
                client = PythonClient(device, self, plugins)
            if not client or not plugins:
                log.warn("Python客户端创建失败")
                return
        except (SystemExit, KeyboardInterrupt): raise
        except:
            log.exception("打开Python客户端时出错")
        self.addClient(client, timeout, 'python', ip)

    def cmdCollect(self, device, ip, timeout):
        """
        命令行数据收集
        """
        client = None
        clientType = 'snmp'

        hostname = ip
        try:
            plugins = self.selectPlugins(device,"command")
            if not plugins:
                log.info("在设备%s上未找到command收集器插件" % hostname)
                return

            protocol = getattr(device, 'netCommandProtocol', defaultProtocol)
            commandPort = getattr(device, 'netCommandPort', defaultPort)

            if protocol == "ssh":
                client = SshClient(hostname, ip, commandPort,
                                   options=self.options,
                                   plugins=plugins, device=device,
                                   datacollector=self, isLoseConnection=True)
                clientType = 'ssh'
                log.info('在设备%s上使用SSH收集方式'
                              % hostname)

            elif protocol == 'telnet':
                if commandPort == 22: commandPort = 23 #set default telnet
                client = TelnetClient(hostname, ip, commandPort,
                                      options=self.options,
                                      plugins=plugins, device=device,
                                      datacollector=self)
                clientType = 'telnet'
                log.info('在设备%s上使用Telnet收集方式'
                              % hostname)

            else:
                info = "未知协议 %s 设备:%s -- 默认 %s 为收集方法" %(protocol, hostname, clientType)
                log.warn( info )
                #dictMap={'critical':5, 'error':4, 'warning':3, 'info':2, 'debug':1, 'clear':0}
                evt= { "deviceUid":device.getUid(),
                            "component":None,
                            "message":info,
                            "eventKey":"model",
                            "severity":3,
                            "collector":"main",
                            "agent":self.name
                            }
                self.saveEvent( evt )
                return

            if not client:
                log.warn("Shell命令收集器创建失败")
            else:
                log.info("插件: %s",
                    ", ".join(map(lambda p: p.name(), plugins)))
        except (SystemExit, KeyboardInterrupt): raise
        except:
            log.exception("打开命令收集器失败")
        self.addClient(client, timeout, clientType, ip)

    def snmpCollect(self, device, ip, timeout):
        """
        snmp数据收集
        """
        client = None
        try:
            hostname = device.manageIp
#            if getattr( device, "netSnmpMonitorIgnore", True ):
#                log.info("主机%s上SNMP监控失效" % hostname)
#                return

            if not ip:
                log.info("主机%s上没有设置管理IP" % hostname)
                return

            plugins = []
            plugins = self.selectPlugins(device,"snmp")
            if not plugins:
                log.info("主机%s上么有发现SNMP插件" % hostname)
                return

            if self.checkCollection(device):
                log.info('SNMP收集器设备%s' % hostname)
                log.info("插件: %s",
                              ", ".join(map(lambda p: p.name(), plugins)))
                from products.netPublicModel.config.snmpConnInfo import SnmpConnInfo
                snmpConninfo = SnmpConnInfo(device.manageIp,device.snmpConfig)
                client = SnmpClient(device.manageIp,device.manageIp,device=device,connInfo = snmpConninfo,datacollector=self,plugins = plugins)
            if not client or not plugins:
                log.warn("SNMP收集器创建失败")
                return
        except (SystemExit, KeyboardInterrupt): raise
        except:
            log.exception("打开SNMP收集器失败")
        self.addClient(client, timeout, 'SNMP', ip)

    def addClient(self, device, timeout, clientType, name):
        """
        添加设备的客户端
        """
        if device:
            device.timeout = timeout
            device.timedOut = False
            self.clients.append(device)
            device.start()
        else:
            log.warn('在设备%s无法创建收集器%s',
                           name,clientType)

    def portscanCollect(self, device, ip, timeout):
        """
        扫描收集数据
        """
        client = None
        try:
            hostname = ip
            plugins = self.selectPlugins(device, "portscan")
            if not plugins:
                log.info("在主机%s上未找到portscan插件" % hostname)
                return
            if self.checkCollection(device):
                log.info('在设备%s上设置portscan收集方式'
                              % hostname)
                log.info("插件: %s",
                    ", ".join(map(lambda p: p.name(), plugins)))
                client = PortscanClient(ip, ip, self.options,
                                        device, self, plugins)
            if not client or not plugins:
                log.warn("Portscan收集器创建失败")
                return
        except (SystemExit, KeyboardInterrupt): raise
        except:
            log.exception("打开portscan收集器失败")
        self.addClient(client, timeout, 'portscan', ip)

    def checkCollection(self, device):
        """
        检查数据收集的新旧
        """
#        age = device.getSnmpLastCollection() + self.collage
#        if device.getSnmpStatusNumber() > 0 and age >= DateTime.DateTime():
#            log.info("跳过设备%s上的收集器插件" % device.manageIp)
#            return False
        return True

    def clientFinished(self, collectorClient):
        """
        对收集的返回值进行处理
        """
        device = collectorClient.device
        log.debug("完成设备%s上的收集工作", device.manageIp)
        def processClient(driver):
            try:
                pluginStats = {}
                log.debug("收集设备%s的数据", device.manageIp)
                devchanged = False
                maps = []
                for plugin, results in collectorClient.getResults():
                    if plugin is None: continue
                    log.debug("%s启动设备%s上的收集器插件 ...",
                                   plugin.name(), device.manageIp)
                    if not results:
                        log.warn("插件%s未返回任何结果.",
                                      plugin.name())
                        continue

                    datamaps = []
                    try:
                        results = plugin.preprocess(results, log)
                        if results:
                            status,datamaps = plugin.process(device, results, log)
                        if status:
                            yield defer.execute(updateConfig,device,datamaps,plugin)
                            pluginStats.setdefault(plugin.name(), plugin.weight)

                    except (SystemExit, KeyboardInterrupt), ex:
                        log.info( "插件%s由于外部信号(%s)终止运行" % (plugin.name(), str(ex))                                      )
                        continue

                    except Exception, ex:
                        info= "执行收集器插件出现问题 %s" %plugin.name()
                        log.warn( info )
                        #dictMap={'critical':5, 'error':4, 'warning':3, 'info':2, 'debug':1, 'clear':0}
                        evt= { "deviceUid":device.getUid(),
                                    "component":None,
                                    "message":info,
                                    "eventKey":"model",
                                    "severity":3,
                                    "collector":"main",
                                    "agent":self.name
                        }
                        self.saveEvent( evt )
                        continue

                    if type(datamaps) not in (types.ListType, types.TupleType):
                        datamaps = [datamaps,]
                    if datamaps:
                        maps += [m for m in datamaps if m]
                if devchanged:
                    log.info("配置应用变化")
                else:
                    log.info("未检测到配置应用变化")
            except Exception, ex:
                log.exception(ex)
                raise
 
        def updateConfig(device,tmpObjList,plugin):
            "更新设备的接口\文件\进程等信息"
            realConfigList = plugin.getDataList(device)
            realNameList = []
            realDict = {}
            for realEle in realConfigList:
                realNameList.append(realEle.name)
                realDict[realEle.name] = realEle
    
            #没有发现接口\文件\进程等
            if not tmpObjList:
                for realConfig in realConfigList:
                    realConfig.remove()
                return
    
            for tmpObj in tmpObjList:
                #是否为已有的接口\文件\进程等，如果存在需要更新，没有就创建
                if tmpObj.name in realNameList:
                    #接口\文件\进程等是否被锁定
                    realObj = realDict[tmpObj.name]
                    realNameList.remove(tmpObj.name)
                    if realObj.locked:
                        continue
                    else:
                        #更新接口\文件\进程等
                        plugin.updateConfig(realObj,tmpObj)
                else:
                    #新发现的接口\文件\进程等需要创建
                    tmpObj._saveObj()
    
            #不存在的接口\文件\进程等需要删除
            if realNameList:
                for rname in realNameList:
                    realDict[rname].remove() 
        
        def processClientFinished(result):
            """
            处理收集完成的客户端
            """
            if not result:
                log.debug("设备%s完成数据收集" % device.manageIp)
            else:
                log.error("设备%s完成时携带信息: %s" %
                               (device.manageIp, result))
            try:
                self.clients.remove(collectorClient)
                self.finished.append(collectorClient)
            except ValueError:
                log.debug("设备%s在活跃设备列表中未找到",device.manageIp)
            d = drive(self.fillCollectionSlots)
            d.addErrback(self.fillError)

        d = drive(processClient)
        d.addBoth(processClientFinished)



    def fillError(self, reason):
        """
        出错函数
        """
        if type(reason.value) == StopIteration:
            pass
        else:
            log.error("无法填补收集插槽: %s" % reason)


    def cycleTime(self):
        """
        循环时间
        """
        return self.modelerCycleInterval * 60

    def checkStop(self, unused = None):
        """
        检查是否停止
        """
        if self.clients: return
        if self.devicegen: return

        if self.start:
            runTime = time.time() - self.start
            self.start = None
            log.info("扫描时间: %0.2f seconds", runTime)
            devices = len(self.finished)
            timedOut = len([c for c in self.finished if c.timedOut])
            summary='周期循环时间: %s,扫描时间: %s devices %s 超时时间: %s'%(self.cycleTime(),runTime,devices,timedOut)
            #dictMap={'critical':5, 'error':4, 'warning':3, 'info':2, 'debug':1, 'clear':0}
            data = { "deviceUid":None,
                            "component":None,
                            "message":summary,
                            "eventKey":"model",
                            "severity":2,
                            "collector":"main",
                            "agent":self.name
            }
            self.saveEvent(data)
            if not self.options.cycle:
                self.stop()
            self.finished = []
            
    def stop(self, ignored=''):
        """
        停止
        """
        def stopNow(ignored):
            if reactor.running:
                reactor.stop()
        if reactor.running and not self.stopped:
            self.stopped = True
            reactor.callLater(1, stopNow, True)
        
    def remoteGetDeviceConfig(self):
        """
        功能:获取设备配置信息
        返回:所有设备配置信息
        作者:wl
        时间:2013-1-16
        """
        deviceConfigs=[]
        import pickle
        try:
            serObj = self.rpyc.getServiceObj()
            csm = serObj.getCSM(self.options.csmconfig)
            if self.options.device:
                log.info("收集设备%s信息", self.options.device)
                deviceConfigs = pickle.loads(csm.remoteGetDeviceConfigByUidList([self.options.device]))
            else:
                deviceConfigs = pickle.loads(csm.remoteGetDeviceConfig(self.options.collector))
        except Exception,ex:
            summary="远程获取设备配置出错,%s"%(ex)
            log.error(summary)

        log.info("共计获取%d个设备的配置" % len(deviceConfigs))
        if not deviceConfigs:
            log.info("获取设备数据为空.")
            return defer.fail("获取设备数据为空.")
        self.devicegen = iter(deviceConfigs)

    def fillCollectionSlots(self, driver):
        """
        设备数据调用收集
        """
        count = len(self.clients)
        if count < self.options.parallel:
            try:
                yield defer.maybeDeferred(self.devicegen.next)
                device = driver.next()
                self.collectDevice(device)
            except (StopIteration,AttributeError),ex:
                self.devicegen = None
            
        update = len(self.clients)
        if not update:pass
        elif update != count and update != 1:
            log.info('运行%d个客户端', update)
        else:
            log.debug('运行%d个客户端', update)
        self.checkStop()

    def _timeoutClients(self):
        """
        超时检查
        """
        active = []
        for client in self.clients:
            if client.timeout < time.time():
                log.warn("设备%s连接超时", client.hostname)
                self.finished.append(client)
                client.timedOut = True
                client.stop()
            else:
                active.append(client)
        self.clients = active

    def timeoutClients(self, unused=None):
        """
        客户端超时检查并停止超时的客户端
        """
        reactor.callLater(1, self.timeoutClients)
        self._timeoutClients()
        d = drive(self.fillCollectionSlots)
        d.addCallback(self.checkStop)
        d.addErrback(self.fillError)

    def reactorLoop(self):
        """
        Twisted主循环
        """
        reactor.startRunning()
        while reactor.running:
            try:
                while reactor.running:
                    reactor.runUntilCurrent()
                    timeout = reactor.timeout()
                    reactor.doIteration(timeout)
            except:
                if reactor.running:
                    log.exception("主方法中发生错误.")

    def mainLoop(self):
        """
        主收集循环,python迭代
        """
        if self.options.cycle:
            driveLater(self.cycleTime(), self.mainLoop)

        if self.clients:
            log.error("模型化花了太长时间了,客户端超时返回")
            return
        
        self.start = time.time()
        log.debug("启动收集器...")
        d = defer.maybeDeferred(self.remoteGetDeviceConfig)
        d.addCallback(self.fillCollectionSlots)
        d.addErrback(self.fillError)
        log.debug("收集器插槽已填满")

    def main(self, unused=None):
        """
        主函数
        """
        self.finished = []
        d = defer.maybeDeferred(self.mainLoop)
        d.addCallback(self.timeoutClients)
        return d

    def run(self):
        """
        启动
        """
        self.connected()
        reactor.run()
        
    def buildOptions(self):
        """
        构建命令行选项
        """
        DeamonBase.buildOptions(self)
        self.parser.add_option('--debug',
                dest='debug', action="store_true", default=False,
                help="打印日志级别")
        self.parser.add_option('-D', '--daemon', default=False,
                dest='daemon',action="store_true",
                help="启动后台运行模式")
        self.parser.add_option('--parallel', dest='parallel',
                type='int', default=defaultParallel,
                help="收集设备的最大并发数")
        self.parser.add_option('-c', '--cycle',dest='cycle',
                action="store_true", default=False,
                help="循环执行守护进程")
        self.parser.add_option('--cycletime',
                dest='cycletime',default=720,type='int',
                help="循环时间")
        self.parser.add_option('-p', '--path', dest='path',
                help="开始收集的设备类路径")
        self.parser.add_option('-a', '--collage',
                dest='collage', default=0, type='float',
                help="多少时间之内不收集数据")
        self.parser.add_option('-d', '--device', dest='device', default="51e74f549c59154c5fffc88c",
                help="符合要求的设备ID")
        self.parser.add_option('--now',
                dest='now', action="store_true", default=False,
                help="立刻运行守护进程")
        self.parser.add_option('--csmconfig',dest='csmconfig',default='ModelConfig',
                help='netmodel守护进程配置类,默认为ModelConfig')
        
if __name__ == '__main__':
        nm = NetModel()
        reactor.run = nm.reactorLoop
        nm.run()

        
        
