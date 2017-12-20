#coding=utf-8
import pickle,os
from products.netUtils.xutils import importClass
from products.dataCollector.snmpClient import SnmpClient
from products.dataCollector.portscanClient import PortscanClient
from products.dataCollector.sshClient import SshClient
from products.dataCollector.pythonClient import PythonClient
from products.dataCollector.discDevice import DiscDevice
import logging
log = logging.getLogger("netTcpServer")
class CollectModel(object):
    """
    用于管理端交互执行管理端发送的命令或者程序
    """
    def __init__(self,transport,factory):
        """
        初始化函数
        """
        self.transport=transport
        self.factory=factory

    def getObjConfig(self,uid,componentType):
        """
            得到对象配置
        """ 
        def afun(serviceObj=None):
            csm = serviceObj.getCSM("ModelConfig")
            return csm.remoteGetObjConfigByUid(uid,componentType)
        configResults = self.factory.rpyc.access(afun)
        if configResults is None:return []
        return pickle.loads(configResults)
    
    def getClassCollectorPlugins(self,clsName):
        """
        获取对象的收集器插件
        """
        modelPath = " products.dataCollector.plugins"
        try:
            cls = importClass("%s.%s"%(modelPath.strip(),clsName),clsName)()
            return cls
        except Exception,e:
            self.transportWrite({"message":"不支持该类型的数据获取,请连接管理人员!","data":[]})
    
    def transportWrite(self,rs):
        """
        写入
        """
        self.transport.write(pickle.dumps(rs))
        
    def isCollector(self):
        """
        是收集器
        """
        log.info("in func isCollector")
        self.transportWrite(True)
        self.transport.loseConnection()
        
    def checkPingAndSnmpStatus(self,data):
        manageIp = data.get("manageIp","")
        snmpCommunity = data.get("snmpCommunity","public")
        #pingRes = os.system("ping %s -c 1" %manageIp)
        #if pingRes != 0:
        #    self.transportWrite(1)
        #    self.transport.loseConnection()
        #    return
        snmpRes = os.system("snmpwalk -v 2c -c %s %s sysname" %(snmpCommunity,manageIp))
        if snmpRes != 0:
            self.transportWrite(2)
            self.transport.loseConnection()
            return
        self.transportWrite(0)
        self.transport.loseConnection()
        
    def collectDevice(self,data):
        """
        设备配置数据采集
        """
        uid=data.get("uid")
        clsName=data.get("clsName")
        componentType=data.get("componentType")
        obj=self.getObjConfig(uid, componentType)
        cls=self.getClassCollectorPlugins(clsName)
        if cls is  None or obj is None:return
        client=getattr(self,"%sCollect"%cls.transport)(obj,cls,10)
        if client:
            client.start()
        else:
            self.transportWrite({"message":"在设备%s无法获取%s的数据"%(uid,clsName),"data":[]})
            log.warn('在设备%s无法获取%s的数据',uid,clsName)
    
    def executeSshCmd(self,data):
        """
                执行SSH命令
        """
        uid=data.get("uid")
        cmd=data.get("cmd").encode("utf-8")
        componentType=data.get("componentType")
        obj=self.getObjConfig(uid, componentType)
        cls=self.getClassCollectorPlugins("SshCmdMap")
        if cls is  None or obj is None:return
        client=self.sshCollect(obj,cls,cmd)
        if client:
            client.run()
        else:
            self.transportWrite({"message":"在设备%s无法执行%s命令!"%(uid,cmd),"data":[]})
            
    def discoverDevice(self,data):
        """
                设备自动发现
        """
        ips=data.get("batchIps")
        communities=data.get("communities")
        dde=DiscDevice(self,ips,communities)
        dde.startDiscover()
            
    def portscanCollect(self,obj,cls,timeout):
        """
                扫描收集数据
        """
        client = None
        try:
            client = PortscanClient(obj.manageIp,obj.manageIp,self.options,obj, self,[cls])
            if not client:
                log.warn("Portscan客户端创建失败")
                return
        except (SystemExit, KeyboardInterrupt): raise
        except:
            log.exception("portscan获取数据失败")
        return client
        
    def snmpCollect(self,obj,cls,timeout):
        """
        SNMP收集数据
        """
        from products.netPublicModel.config.snmpConnInfo import SnmpConnInfo
        client = None
        try:
            #hostname = obj.manageIp
            #if getattr( obj, "netSnmpMonitorIgnore", False ):
                #log.info("主机%s上禁用SNMP" % hostname)
                #return
            snmpConninfo = SnmpConnInfo(obj.manageIp,obj.snmpConfig)
            client = SnmpClient(obj.manageIp,obj.manageIp,device=obj,connInfo = snmpConninfo,datacollector=self,plugins = [cls])
            if not client:
                log.warn("SNMP客户端创建失败")
                return
        except (SystemExit, KeyboardInterrupt): raise
        except:
            log.exception("SNMP获取数据失败")
        return client
    
    def getSshOptions(self,obj):
        """
                获取设备SSH参数
        """
        from products.netRRD.option import Options
        if obj.getComponentType()=="Device":
            commConfig=obj.commConfig
            username=commConfig.get("netCommandUsername").encode("utf-8")
            password=commConfig.get("netCommandPassword").encode("utf-8")
            loginTimeout=commConfig.get("netCommandLoginTimeout")
            commandTimeout=commConfig.get("netCommandCommandTimeout")
            keyPath=commConfig.get("netKeyPath").encode("utf-8")
            concurrentSessions=commConfig.get("netSshConcurrentSessions")
            option=Options(username,password,loginTimeout,commandTimeout,keyPath,concurrentSessions)
            return option
        else:
            self.transportWrite({"message":"warn:命令无法执行!","data":[]})
        

    def sshCollect(self,obj,cls,cmd):
        """
        ssh命令数据获取
        """
        client = None
        try:
            hostname = obj.manageIp
            options=self.getSshOptions(obj)
            commandPort = obj.commConfig.get('netCommandPort',22)
            cls.command=cmd
            if options:
                client = SshClient(hostname,hostname, commandPort,
                                   options=options,
                                   plugins=[cls], device=obj,
                                   datacollector=self, isLoseConnection=True)
                log.info('在设备%s上使用SSH方式执行命令'% hostname)
            else:
                return
            if not client:
                log.warn("命令行客户端创建失败")
        except (SystemExit, KeyboardInterrupt): raise
        except:
            self.transportWrite({"message":"warn:命令获取数据失败!","data":[]})
        return client
    

    def pythonCollect(self,obj,cls,timeout):
        """
        python数据收集
        """
        client = None
        try:
            client = PythonClient(obj,self,[cls])
            if not client:
                log.warn("Python客户端创建失败")
                return
        except (SystemExit, KeyboardInterrupt): raise
        except:
            log.exception("Python脚本获取数据失败")
        return client
    
    def ipmiCollect(self,obj,cls,timeout):
        """
                开机执行
        """
        message,datamaps = cls.process(obj,log)
        self.transportWrite({"message":message,"data":datamaps})
        self.transport.loseConnection()
    
    def clientFinished(self,sc):
        """
                收集完成
        """
        for plugin,results in sc.getResults():
                if plugin is None: continue
                if not results:
                    self.transportWrite({"message":"未返回任何结果!","data":[]})
                    log.warn("插件%s未返回任何结果.",plugin.name())
                    continue
                try:
                    results = plugin.preprocess(results,log)
                    if results:
                        message,datamaps = plugin.process(sc.device,results,log)
                        self.transportWrite({"message":message,"data":datamaps})
                except (SystemExit,KeyboardInterrupt),ex:
                    self.transportWrite({"message":"warn:获取数据出错!","data":[]})
                    continue
        else:
            self.transport.loseConnection()
            
