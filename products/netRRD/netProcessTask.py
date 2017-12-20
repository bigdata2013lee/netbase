#! /usr/bin/env python
#coding=utf-8
###########################################################################
#
#
#此软件版权为深圳商之杰科技有限公司所有,更多信息请访问www.netbase.asia
#
#
###########################################################################

__doc__ = '''
通过SNMP获取设备进程数据
'''
from twisted.internet import defer,error
from twisted.python.failure import Failure
from products.netUtils.chain import Chain
from products.dataCollector.redisManager import RedisManager
import logging
log = logging.getLogger("netprocess")
WRAP = 100.0
# 使用HOST-RESOURCES-MIB中的OIDs
HOSTROOT = '.1.3.6.1.2.1.25'
RUNROOT = HOSTROOT + '.4'
NAMETABLE = RUNROOT + '.2.1.2'
PATHTABLE = RUNROOT + '.2.1.4'
ARGSTABLE = RUNROOT + '.2.1.5'
PERFROOT = HOSTROOT + '.5'
CPU = PERFROOT + '.1.1.1.'
MEM = PERFROOT + '.1.1.2.'


class NetProcessTask(RedisManager):

    def __init__(self,snmpConfig,schedule):
        """
        功能:进程任务初始化
        参数:SNMP配置,定制任务对象
        作者:wl
        时间:2013-1-17
        """
        self.schedule = schedule
        self.snmpConfig = snmpConfig
        self.snmpProxy = None
        self.snmpConnInfo = snmpConfig.snmpConninfo
        self.device = snmpConfig.manageIp
        self.deviceStats = DeviceStatus(snmpConfig)

    def connect(self):
        """
        功能:获取连接
        返回:返回SNMP连接代理
        作者:wl
        时间:2013-1-17
        """
        if (self.snmpProxy is None or
            self.snmpProxy.snmpConnInfo != self.snmpConnInfo):
            self.snmpProxy = self.schedule.getSnmpProxy(self.snmpConfig)

    def connectCallback(self,result):
        """
        功能:流程控制函数
        参数:SNMP连接代理
        作者:wl
        时间:2013-1-17
        """
        log.debug("连接到%s",self.device)
        return result

    def handleProcess(self):
        """
        功能:任务执行函数,连接一台设备,返回一个deffered
        作者:wl
        时间:2013-1-14
        """
        #log.info("handleProcess coming in...")
        d = defer.maybeDeferred(self.connect)
        d.addCallbacks(self.connectCallback,self.failure)
        d.addCallback(self.collectCallback)
        d.addBoth(self.finished)
        return d

    def failure(self,reason):
        """
        功能:失败处理
        作者:wl
        时间:2013-1-17
        """
        msg = '无法读取设备%s 上的进程' % self.device
        if isinstance(reason.value,error.TimeoutError):
            log.debug('Timeout on device %s' % self.device)
            msg = '%s; 连接设备超时' % msg
        else:
            msg = '%s; 错误: %s' % (msg,reason.getErrorMessage())
            log.error('Error on device %s; %s' % (self.device,
                      reason.getErrorMessage()))
        return reason

    def collectCallback(self,result):
        """
        功能:数据收集处理
        参数:SNMP配置,定制任务对象
        作者:wl
        时间:2013-1-17
        """
        #log.info("collectCallback coming in ...")
        tables = [NAMETABLE,PATHTABLE,ARGSTABLE]
        d = self.getTable(tables)
        if d:
            d.addCallbacks(self.storeProcessNames,self.failure)
            d.addCallback(self.fetchPrefer)
            return d
        return None

    def getTable(self,tables):
        """
        功能:通过SNMP代理远程获取进程列表
        参数:SNMP配置,定制任务对象
        作者:wl
        时间:2013-1-17
        """
        import sys
        repetitions = 40 / len(tables)
        result = self.snmpProxy.getTable(tables,
                                timeout =10,
                                retryCount = 2,
                                maxRepetitions =repetitions,
                                limit = sys.maxint)
        return result

    def storeProcessNames(self,results):
        """
        功能:缓存进程列表
        参数:SNMP配置,定制任务对象
        作者:wl
        时间:2013-1-17
        """
        log.info("storeProcessNames coming in ...")
        if not results or not results[NAMETABLE]:
            summary = '设备%s未配置MIB库HOST-RESOURCES-MIB' % self.snmpConfig.manageIp
            log.info(summary)
            return defer.fail(summary)
        summary="设备%s进程列表已开启"%(self.snmpConfig.manageIp)
        log.info(summary)
        args,procs = self.mapResultsToDicts(results)
        #log.info("storeProcessNames procs:%s" % procs)
        #self.showProcessList(procs)

        # 查找进程中的差异
        beforePids = set(self.deviceStats.pidToProcess.keys())
        afterPidToProcessStats = {}
        for pStats in self.deviceStats.processStats:
            for pid,(name,args) in procs:
                if pStats.match(name,args):
                    log.info("Found process %d on %s" % (pid,pStats.config.name))
                    afterPidToProcessStats[pid] = pStats
        afterPids = set(afterPidToProcessStats.keys())
        afterByConfig = self.reverseDict(afterPidToProcessStats)
        newPids = afterPids - beforePids
        deadPids = beforePids - afterPids

        # 死掉的进程重启
        restarted = {}
        for pid in deadPids:
            procStats = self.deviceStats.pidToProcess[pid]
            procStats.discardPid(pid)
            if procStats in afterByConfig:
                pConfig = procStats.config
                if pConfig.restart:
                    restarted[procStats] = True
                    summary = '重启进程: %s' % pConfig.originalName
                    data = {"moUid":pConfig.psid,
                             "title":pConfig.name,
                             "componentType":pConfig.componentType,
                             "message":summary,
                             "severity":pConfig.severity,
                             "eventClass":"/status",
                             "collector":pConfig.cuid,
                             "agent":"netprocess"
                }
                    self.saveEvent(data)
                    log.info(summary)

        # 当前运行进程
        for processStat in afterByConfig.keys():
            if processStat in restarted: continue
            summary = "已启动进程: %s" % processStat.config.originalName
            data = {"moUid":processStat.config.psid,
                            "title":processStat.config.name,
                             "componentType":processStat.config.componentType,
                             "message":summary,
                             "severity":0,
                             "eventClass":"/status",
                             "collector":processStat.config.cuid,
                             "agent":"netprocess"
                }
            self.saveEvent(data)
            log.debug(summary)

        # 新起动进程
        for pid in newPids:
            log.debug("Found new %s pid %d on %s" % (
                afterPidToProcessStats[pid].config.originalName,pid,
                self.snmpConfig.manageIp))
        self.deviceStats.pidToProcess = afterPidToProcessStats

        # 无法运行的进程
        for procStat in self.deviceStats.processStats:
            if procStat not in afterByConfig:
                procConfig = procStat.config
                summary = '进程已停止: %s' % procConfig.originalName
                data = {"moUid":procConfig.psid,
                            "title":procConfig.name,
                             "componentType":procConfig.componentType,
                             "message":summary,
                             "severity":procConfig.severity,
                             "eventClass":"/status",
                             "collector":procConfig.cuid,
                             "agent":"netprocess"
                }
                self.saveEvent(data)
                log.warning(summary)

        # 存储设备的每个进程状态
        pidCounts = {}
        for procStat in self.deviceStats.pidToProcess.values():
            pidCounts[procStat] = pidCounts.get(procStat,0) + 1
        for procName,count  in pidCounts.items():
            data =  {'moUid': procName.config.psid,
                          "title":procName.config.name,
                          'componentType':procName.config.componentType,
                           'templateUid':'OSProcess',
                          'dataSource':"ps",
                          'dataPoint':"count",
                          'value': count,
                          "agent":"netprocess"
            }
            self.saveResult(data)
        return results

    def mapResultsToDicts(self,results):
        """
        功能:SNMP数据解析格式化为DICT类型
        参数:SNMP配置,定制任务对象
        作者:wl
        时间:2013-1-17
        """
        def extract(dictionary,oid,value):
            """
            功能:SNMP数据解析格式化为DICT类型
            参数:SNMP配置,定制任务对象
            作者:wl
            时间:2013-1-17
            """
            pid = int(oid.split('.')[-1])
            dictionary[pid] = value

        names,paths,args = {},{},{}
        log.debug("NAMETABLE = %r",results[NAMETABLE])
        for row in results[NAMETABLE].items():
            extract(names,*row)
        log.debug("PATHTABLE = %r",results[PATHTABLE])
        for row in results[PATHTABLE].items():
            extract(paths,*row)
        log.debug("ARGSTABLE = %r",results[ARGSTABLE])
        for row in results[ARGSTABLE].items():
            extract(args,*row)

        procs = []
        for pid,name in names.items():
            path = paths.get(pid,'')
            if path and path.find('\\') == -1:
                name = path
            arg = args.get(pid,'')
            procs.append((pid,(name,arg)))
        return args,procs

    def showProcessList(self,procs):
        """
        功能:显示进程信息列表
        参数:SNMP配置,定制任务对象
        作者:wl
        时间:2013-1-17
        """
        device_name = self.snmpConfig.manageIp
        proc_list = [ '%s %s %s' % (pid,name,args) for pid,(name,args) \
                         in sorted(procs)]
        proc_list.append('')
        log.info("#===== Processes on %s:\n%s",device_name,'\n'.join(proc_list))

    def getPids(self,procs):
        """
        功能:获取PID列表
        参数:SNMP配置,定制任务对象
        作者:wl
        时间:2013-1-17
        """
        pid_list = []
        for pid,(name,args) in sorted(procs):
            pid_list.append(pid)
        return pid_list

    def reverseDict(self,afterPids):
        """
        功能:反转
        参数:SNMP配置,定制任务对象
        作者:wl
        时间:2013-1-17
        """
        result = {}
        for a,v in afterPids.items():
            result.setdefault(v,[]).append(a)
        return result

    def fetchPrefer(self,result):
        """
        功能:获取进程性能指标
        参数:SNMP配置,定制任务对象
        作者:wl
        时间:2013-1-17
        """
        oids = []
        for pid in self.deviceStats.pids:
            oids.extend([CPU + str(pid),MEM + str(pid)])
        if not oids:
            return defer.succeed(([]))

        def get(oids):
            """
            功能:得到OID的值
            参数:SNMP配置,定制任务对象
            作者:wl
            时间:2013-1-17
            """
            return self.snmpProxy.get(oids,20,2)

        d = Chain(get,iter(self.chunk(oids,40))).run()
        d.addCallbacks(self.storePerfStats,self.failure)
        return d

    def storePerfStats(self,results):
        """
        功能:缓存性能状态指标
        参数:SNMP配置,定制任务对象
        作者:wl
        时间:2013-1-17
        """
        for success,result in results:
            if  not success:
                return result
        parts = {}
        for success,values in results:
            if success:
                parts.update(values)
        results = parts
        byConf = self.reverseDict(self.deviceStats.pidToProcess)
        for procStat,pids in byConf.items():
            if len(pids) != 1:
                log.info("There are %d pids by the name %s",
                         len(pids),procStat.config.name)
            for pid in pids:
                cpu = results.get(CPU + str(pid),None)
                mem = results.get(MEM + str(pid),None)
                procStat.updateCpu(pid,cpu)
                procStat.updateMemory(pid,mem)
            data =  {'moUid': procStat.config.psid,
                          "title":procStat.config.name,
                          'componentType':procStat.config.componentType,
                           'templateUid':'OSProcess',
                          'dataSource':"ps",
                          'dataPoint':"cpu",
                          'value': procStat.cpu,
                          "agent":"netprocess"
            }
            self.saveResult(data)
            data['dataPoint'] = 'mem'
            data['value'] = procStat.getMemory() * 1024
            self.saveResult(data)
        return results

    def chunk(self,lst,n):
        """
        功能:按n将列表分成子列表
        参数:SNMP配置,定制任务对象
        作者:wl
        时间:2013-1-17
        """
        return [lst[i:i + n] for i in xrange(0,len(lst),n)]

    def close(self):
        """
        功能:关闭
        参数:SNMP配置,定制任务对象
        作者:wl
        时间:2013-1-17
        """
        if self.snmpProxy:
            self.snmpProxy.close()
        self.snmpProxy = None

    def finished(self,result):
        '''
        功能:结束工作,关闭连接
        参数:SNMP配置,定制任务对象
        作者:wl
        时间:2013-1-17
        '''
        if not isinstance(result,Failure):
            log.debug("Device %s  scanned successfully",
                     self.device)
        else:
            if isinstance(result.value,error.TimeoutError):
                log.error( "连接设备%s超时" % (self.device))
            else:
                log.debug("Device %s  scanned failed, %s",
                          self.device,result.getErrorMessage())
        try:
            self.schedule.close(self.snmpConfig)
        except Exception,e:
            log.warn("Failed to close device %s: error %s" %
                     (self.device,str(e)))

class DeviceStatus(object):
    '''
    设备状态类
    '''
    def __init__(self,deviceConfig):
        self.config = deviceConfig
        #PID与进程状态类的映射关系
        self.pidToProcess = {}
        #进程ID与进程状态类的映射关系
        self.processes = {}
        for psid,process in deviceConfig.processes.items():
            self.processes[process.psid] = ProcessStats(process)

    def update(self,device):
        '''
        更新进程状态
        '''
        for process in device.processes:
            if self.processes.get(id):
                self.processes[id].update(process)
            else:
                self.processes[id] = ProcessStats(process)

    @property
    def processStats(self):
        """
        进程ProcessStats
        """
        return self.processes.values()

    @property
    def pids(self):
        """
        PID
        """
        return self.pidToProcess.keys()


class ProcessStats:
    '''
    进程状态类
    '''
    def __init__(self,process):
        self.pids = {}
        self.config = process
        self.cpu = 0

    def update(self,process):
        self.config = process

    def match(self,name,args):
        """
        匹配进程名称
        """
        if self.config.name is None:
            return False
        if not args:return self.config.originalName == name
        nargs='%s%s'% (name,args)
        return self.config.originalName.replace(" ", "") == nargs.replace(" ", "")

    def updateCpu(self,pid,value):
        """
        更新CPU
        """
        pid = self.pids.setdefault(pid,Pid())
        cpu = pid.updateCpu(value)
        if cpu is not None:
            self.cpu += cpu/WRAP

    def updateMemory(self,pid,value):
        """
        更新内存
        """
        self.pids.setdefault(pid,Pid()).memory = value

    def getMemory(self):
        """
        得到内存
        """
        return sum([x.memory for x in self.pids.values()
                    if x.memory is not None])

    def discardPid(self,pid):
        """
        删除
        """
        if pid in self.pids:
            del self.pids[pid]

class Pid:
    """
    Pid类
    """
    cpu = None
    memory = None

    def updateCpu(self,n):
        """
        更新CPU
        """
        if n is not None:
            try:
                n = int(n)
            except ValueError:
                log.warning("Bad value for CPU: '%s'",n)
        self.cpu = n
        return self.cpu

    def updateMemory(self,n):
        """
        更新内存
        """
        self.memory = n
