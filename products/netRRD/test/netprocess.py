#! /usr/bin/env python
#coding=utf-8
###########################################################################
#
#
#此软件版权为深圳商之杰科技有限公司所有,更多信息请访问www.netbase.asia
#
#
###########################################################################


__doc__ = """
通过SNMP获取设备进程数据
"""

import logging
import sys
import re
from md5 import md5
from pprint import pformat
import os.path


from products.netUtils.Utils import unused
from products.netPublicModel.config.snmpConnInfo import SnmpConnInfo
from twisted.internet import defer,error

# 使用HOST-RESOURCES-MIB中的OIDs
HOSTROOT = '.1.3.6.1.2.1.25'
RUNROOT = HOSTROOT + '.4'
NAMETABLE = RUNROOT + '.2.1.2'
PATHTABLE = RUNROOT + '.2.1.4'
ARGSTABLE = RUNROOT + '.2.1.5'
PERFROOT = HOSTROOT + '.5'
CPU = PERFROOT + '.1.1.1.'
MEM = PERFROOT + '.1.1.2.'

#最大CPU数
WRAP = 0xffffffffL

#判断字符窜是否是16进制数字
IS_MD5 = re.compile('^[a-f0-9]{32}$')

class nenProcess(object):
    """
    进程的守护进程,用于判断进程的状态变化和进程的CPU,内存变化情况
    """

    DEVICE_STATS = {}

    #counter to keep track of total restarted and missing processes
    RESTARTED = 0
    MISSING = 0

    STATE_CONNECTING = 'CONNECTING'
    STATE_SCANNING_PROCS = 'SCANNING_PROCESSES'
    STATE_FETCH_PERF = 'FETCH_PERF_DATA'
    STATE_STORE_PERF = 'STORE_PERF_DATA'

    def __init__(self,
                 deviceId,
                 taskName,
                 scheduleIntervalSeconds,
                 taskConfig):

        #needed for interface
        self.name = taskName
        self.configId = deviceId
        self.interval = scheduleIntervalSeconds

        #the task config corresponds to a DeviceProxy
        self._device = taskConfig
        self._devId = self._device.name
        self._manageIp = self._device.manageIp
        self._maxOidsPerRequest = self._device.zMaxOIDPerRequest
        self.snmpProxy = None
        self.snmpConnInfo = self._device.snmpConnInfo


    def _failure(self,reason):
        """
        失败时抛出异常
        """
        return reason


    def _connectCallback(self,result):
        """
        远程设备成功连接时回调
        """
        return result

    def _collectCallback(self,result):
        """
        回调
        """
        self.state = ZenProcessTask.STATE_SCANNING_PROCS
        tables = [NAMETABLE,PATHTABLE,ARGSTABLE]
        d = self._getTables(tables)
        d.addCallbacks(self._storeProcessNames,self._failure)
        d.addCallback(self._fetchPerf)
        return d

    def _finished(self,result):
        """
        任务结束
        """
        try:
            self._close()
        except Exception,e:
            pass
        return result

    def cleanup(self):
        return self._close()

    def doTask(self):
        """
        任务执行函数,连接一台设备,返回一个deffered
        作者:wl
        时间:2013-1-14
        """
        d = defer.maybeDeferred(self.getConnect)
        d.addCallbacks(self._connectCallback,self._failure)
        d.addCallback(self._collectCallback)
        d.addBoth(self._finished)
        return d

    def _storeProcessNames(self,results):
        """
        Parse the process tables and reconstruct the list of processes
        that are on the device.

        @parameter results: results of SNMP table gets
        @type results: dictionary of dictionaries
        @parameter device: proxy connection object
        @type device: Device object
        """

        showrawtables = self._preferences.options.showrawtables
        args,procs = mapResultsToDicts(showrawtables,results)
        if self._preferences.options.showprocs:
            self._showProcessList(procs)

        # look for changes in processes
        beforePids = set(self._deviceStats.pids)
        afterPidToProcessStats = {}
        for pStats in self._deviceStats.processStats:
            for pid,(name,args) in procs:
                if pStats.match(name,args):
                    pass
                    afterPidToProcessStats[pid] = pStats
        afterPids = set(afterPidToProcessStats.keys())
        afterByConfig = reverseDict(afterPidToProcessStats)
        newPids = afterPids - beforePids
        deadPids = beforePids - afterPids

        # report pid restarts
        restarted = {}
        for pid in deadPids:
            procStats = self._deviceStats._pidToProcess[pid]
            procStats.discardPid(pid)
            if procStats in afterByConfig:
                ZenProcessTask.RESTARTED += 1
                pConfig = procStats._config
                if pConfig.restart:
                    restarted[procStats] = True

                    summary = '重启进程: %s' % pConfig.originalName

                    self._eventService.sendEvent(self.statusEvent,
                                                 device = self._devId,
                                                 summary = summary,
                                                 component = pConfig.originalName,
                                                 severity = pConfig.severity)

        # report alive processes
        for processStat in afterByConfig.keys():
            if processStat in restarted: continue
            summary = "已启动进程: %s" % processStat._config.originalName

        self._deviceStats._pidToProcess = afterPidToProcessStats

        # Look for missing processes
        for procStat in self._deviceStats.processStats:
            if procStat not in afterByConfig:
                procConfig = procStat._config
                ZenProcessTask.MISSING += 1
                summary = '进程已停止: %s' % procConfig.originalName

        # Store per-device, per-process statistics
        pidCounts = dict([(p,0) for p in self._deviceStats.processStats])
        for procStat in self._deviceStats.monitoredProcs:
            pidCounts[procStat] += 1
        for procName,count in pidCounts.items():
            self._save(procName,'count_count',count,'GAUGE')
        return results

    def _fetchPerf(self,results):
        """
        得到性能数据
        """
        self.state = ZenProcessTask.STATE_FETCH_PERF

        oids = []
        for pid in self._deviceStats.pids:
            oids.extend([CPU + str(pid),MEM + str(pid)])
        if not oids:
            return defer.succeed(([]))
        d = Chain(self._get,iter(chunk(oids,self._maxOidsPerRequest))).run()
        d.addCallback(self._storePerfStats)
        d.addErrback(self._failure)
        return d

    def _storePerfStats(self,results):
        """
        保存性能数据
        """
        self.state = ZenProcessTask.STATE_STORE_PERF
        for success,result in results:
            if  not success:
                #return the failure
                return result
        parts = {}
        for success,values in results:
            if success:
                parts.update(values)
        results = parts
        byConf = reverseDict(self._deviceStats._pidToProcess)
        for procStat,pids in byConf.items():
            procName = procStat._config.name
            for pid in pids:
                cpu = results.get(CPU + str(pid),None)
                mem = results.get(MEM + str(pid),None)
                procStat.updateCpu(pid,cpu)
                procStat.updateMemory(pid,mem)
            self._save(procName,'cpu_cpu',procStat.getCpu(),
                      'DERIVE',min = 0)
            self._save(procName,'mem_mem',
                      procStat.getMemory() * 1024,'GAUGE')
        return results

    def _getTables(self,oids):
        """
        获取进程snmp表数据
        """
        repetitions = self._maxOidsPerRequest / len(oids)
        t = self.snmpProxy.getTable(oids,
                                timeout = self.snmpConnInfo.zSnmpTimeout,
                                retryCount = self.snmpConnInfo.zSnmpTries,
                                maxRepetitions = repetitions,
                                limit = sys.maxint)
        return t

    def _get(self,oids):
        """
        Perform SNMP get for specified OIDs

        @parameter oids: OIDs to gather
        @type oids: list of strings
        @return: Twisted deferred
        @rtype: Twisted deferred
        """
        return self.snmpProxy.get(oids,
                              self.snmpConnInfo.zSnmpTimeout,
                              self.snmpConnInfo.zSnmpTries)

    def getConnect(self):
        """
        得到一个snmp代理的连接,如果没有就创建
        作者:wl
        时间:2013-1-7
        """
        self.snmpProxy = self.snmpConnInfo.createSession()
        self.snmpProxy.open()

    def _close(self):
        """
        关闭远端设备的连接
        """
        if self.snmpProxy:
            self.snmpProxy.close()
        self.snmpProxy = None


    def _showProcessList(self,procs):
        """
        Display the processes in a sane manner.

        @parameter procs: list of (pid, (name, args))
        @type procs: list of tuples
        """
        device_name = self._devId
        proc_list = [ '%s %s %s' % (pid,name,args) for pid,(name,args) \
                         in sorted(procs)]
        proc_list.append('')


def mapResultsToDicts(showrawtables,results):
    """
    Parse the process tables and reconstruct the list of processes
    that are on the device.
    """
    def extract(dictionary,oid,value):
        """
        解析SNMP数据
        """
        pid = int(oid.split('.')[-1])
        dictionary[pid] = value

    names,paths,args = {},{},{}
    for row in results[NAMETABLE].items():
        extract(names,*row)

    for row in results[PATHTABLE].items():
        extract(paths,*row)

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

def reverseDict(d):
    """
    
    """
    result = {}
    for a,v in d.items():
        result.setdefault(v,[]).append(a)
    return result

def chunk(lst,n):
    """
    n个一组进行分割
    """
    return [lst[i:i + n] for i in xrange(0,len(lst),n)]
if __name__ == '__main__':
    pass
