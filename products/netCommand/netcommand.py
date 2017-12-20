#coding=utf-8
###########################################################################
#       
#
#此软件版权为深圳商之杰科技有限公司所有,更多信息请访问www.netbase.asia
#
#
###########################################################################
__doc__ = """命令行守护进程"""

import time
from sets import Set
from twisted.internet import reactor,defer
from twisted.python import failure

from products.netCommand.commandParser import ParsedResults
from products.netCommand.sshRunner import SshRunner,SshPool
from products.netCommand.telnetRunner import TelnetRunner
from products.netCommand.cmdRunner import CmdRunner
from products.dataCollector.redisManager import RedisManager
from products.netUtils.driver import drive,driveLater
from products.netUtils.Utils import TimeoutError
from products.netUtils.xutils import importClass
from products.netUtils.deamonBase import DeamonBase
import logging
log = logging.getLogger("netcommand")

USESSH = "ssh"
USETEL = "telnet"
USECMD = "script"
class Cmd():
    """
    功能:构建一个命令类,其中包含设备配置
    作者:wl
    时间:2013-1-7
    """
    componentId = None
    componentType = None
    title=None
    templateId = None
    command = None
    connectMode = USECMD
    dsname = None
    cycleTime = None
    severity = 0
    lastStart = 0
    lastStop = 0
    result = None

    def __init__(self):
        self.points = []

    def running(self):
        """
        功能:判断命令是否还在运行
        返回:是否运行
        作者:wl
        时间:2013-1-7
        """
        return self.lastStop < self.lastStart

    def name(self):
        """
        功能:构造命令名称
        返回:名称
        作者:wl
        时间:2013-1-7
        """
        cmd,args = (self.command + ' ').split(' ',1)
        cmd = cmd.split('/')[-1]
        return '%s %s' % (cmd,args)

    def nextRun(self):
        """
        功能:计算命令的下一次运行时间
        返回:时间
        作者:wl
        时间:2013-1-7
        """
        if self.running():
            return self.lastStart + self.cycleTime
        return self.lastStop + self.cycleTime

    def start(self,pool):
        """
        功能:开始执行一个命令
        返回:deffered对象
        作者:wl
        时间:2013-1-7
        """
        if self.connectMode == USESSH:
            pr = SshRunner(pool)
        elif self.connectMode == USETEL:
            pr = TelnetRunner()
        else:
            pr = CmdRunner()
        d = pr.start(self)
        self.lastStart = time.time()
        d.addBoth(self.processEnded)
        return d

    def processEnded(self,pr):
        """
        功能:停止运行
        作者:wl
        时间:2013-1-7
        """
        self.result = pr
        self.lastStop = time.time()

        #检查循环停止的条件
        if self.lastStop < self.lastStart:
            self.lastStop = self.lastStart
        if not isinstance(pr,failure.Failure):
            return self
        return pr

    def updateConfig(self,cfg,manageObjConfig):
        """
        功能:更新命令的配置
        返回:时间
        作者:wl
        时间:2013-1-7
        """
        self.manageObjConfig = manageObjConfig
        self.connectMode = cfg.connectMode
        self.cycleTime = max(cfg.cycleTime,1)
        self.command = str(cfg.command)
        self.points = cfg.points
        return self

class ConfigurationProcessor(object):
    """
    功能:配置处理类,用于更新配置命令
    作者:wl
    时间:2013-1-7
    """

    def __init__(self,config,scheduledCmds):
        self._config = config
        self._scheduledCmds = scheduledCmds
        self._objId = config.objId
        self._suppressed = [] # log warning and send event once per device
        self._summary = 'netCommandUsername 未设置'

    def _warnUsernameNotSet(self,command):
        """
        功能:没有设置用户名警告
        参数:执行的命令
        作者:wl
        时间:2013-1-7
        """
        if self._objId not in self._suppressed:
            log.warning(self._summary + ' for %s' % self._objId)
        msg = 'username not configured for %s. skipping %s.'
        log.info(msg % (self._objId,command))

    def updateCommands(self):
        """
        功能:更新配置的命令
        作者:wl
        时间:2013-1-7
        """
        for cmd in self._config.commands:
            key = (self._objId,cmd.command)
            if cmd.connectMode in [USESSH,USETEL]:
                if self._config.username:
                    pass
                else:
                    self._warnUsernameNotSet(cmd.command)
                    if self._objId not in self._suppressed:
                        self._suppressed.append(self._objId)
                    if key in self._scheduledCmds:
                        del self._scheduledCmds[key]
                    continue
            if key in self._scheduledCmds:
                newCmd = self._scheduledCmds.pop(key)
            else:
                newCmd = cmd
            yield newCmd.updateConfig(cmd,self._config)
        self._suppressed = []

class ManageObjConfig():
    """
    功能:构建一个设备配置类
    作者:wl
    时间:2013-1-7
    """
    cuid=''
    objId = ''
    manageId = ''

class DataPointConfig():
    """
    功能:数据点配置类
    作者:wl
    时间:2013-1-7
    """
    dpname = ''
    dataType = None

    def __init__(self):
        self.data = {}

class netcommand(RedisManager,DeamonBase):
    """
    功能:命令行守护进程
    作者:wl
    时间:2013-1-7
    """
    configCycleInterval =300
    parallel = 100

    def __init__(self):
        DeamonBase.__init__(self)
        self.schedule = []
        self.cmdConfigs=[]
        self.timeout = None
        self.pool = SshPool()
        self.executed = 0
        self.stopped = False

    def updateConfig(self,configs,expected):
        """
        功能:更新设备命令配置,将其加入到任务调度中去
        参数:configs,新加的设备配置,expected,原有的设备
        作者:wl
        时间:2013-1-7
        """
        expected = Set(expected)
        #已有的设备
        current = {}
        for c in self.schedule:
            if c.manageObjConfig.objId in expected:
                current[c.manageObjConfig.objId,c.command] = c
        #一般为空
        update = [c for c in self.schedule if c.manageObjConfig.objId not in expected]
        #更新设备配置
        for cfg in configs:
            processor = ConfigurationProcessor(cfg,current)
            update.extend(processor.updateCommands())
        self.schedule = update
        self.processSchedule()

    def processSchedule(self,*unused):
        """
        功能:任务调度处理
        作者:wl
        时间:2013-1-7
        """
        try:
            #按下一次的开始运行时间从小到大进行排序,确定执行的先后
            def compare(x,y):
                return cmp(x.nextRun(),y.nextRun())
            self.schedule.sort(compare)
            #准备设备的连接
            self.pool.trimConnections(self.schedule)
            earliest = None
            running = 0
            now = time.time()
            for c in self.schedule:
                if c.running():
                    running += 1

            for c in self.schedule:
                #self.parallel:最大的并行运行个数,默认值可设置为10
                #如果大于最大的并行运行次数,则不再重新开始新,直到一部分结束后再开始运行其他
                if running >= self.parallel:
                    break
                if c.nextRun() <= now:
                    c.start(self.pool).addBoth(self.finished)
                    running += 1
                else:
                    earliest = c.nextRun() - now
                    break
            #在一个运行周期内,没有达到开始运行时间的则一秒钟查看一次
            if earliest is not None:
                self.timeout = reactor.callLater(max(1,earliest),
                                                 self.processSchedule)
        except Exception,ex:
            log.error("processSchedule :%s" % ex)

    def finished(self,cmdOrErr):
        """
        功能:命令行完成
        参数:cmd实例或者twisted错误对象
        作者:wl
        时间:2013-1-7
        """
        self.executed += 1
        if isinstance(cmdOrErr,failure.Failure):
            self.error(cmdOrErr)
        else:
            cmd = cmdOrErr
            self.handleExitCode(cmd)
            self.parseResults(cmd)
        self.processSchedule()

    def handleExitCode(self,cmd):
        """
        发送正常的clear事件
        """
        exitCode = cmd.result.exitCode
        msg = '命令: %s - 编号: %s ' % (cmd.command,exitCode)
        if exitCode == 0:
            component=cmd.componentId
            if component:moUid=cmd.componentId
            else:moUid=cmd.manageObjConfig.objId
            data = {"moUid":moUid,
                          "title":cmd.title,
                          "componentType":cmd.componentType,
                          "message":"%s" % msg,
                          "severity":0,
                          "collector":cmd.manageObjConfig.cuid,
                          "agent":"netcommand"
            }
            if cmd.componentType=="Website":
                data.update({"eventClass":"/status"})
            self.saveEvent(data)

    def error(self,err):
        """
        功能:运行命令错误
        参数:异常对象
        作者:wl
        时间:2013-1-6
        """
        if isinstance(err.value,TimeoutError):
            cmd, = err.value.args
            msg = "在设备%s上执行命令超时: %r" % (
                    cmd.manageObjConfig.manageId,cmd.command)
            log.error(msg)
        else:
            log.error(err.value)

    def parseResults(self,cmd):
        """
        功能:解析命令行结果
        参数:命令行对象
        作者:wl
        时间:2013-1-7
        """
        parser = importClass("products.netCommand.parser.%s"%cmd.parser,cmd.parser)
        results = ParsedResults()
        component=cmd.componentId
        if component:moUid=cmd.componentId
        else:moUid=cmd.manageObjConfig.objId
        try:
            parserResults = parser().processResults(cmd,results)
            for ev in results.events:
                ev["collector"]=cmd.manageObjConfig.cuid
                self.saveEvent(ev)
            for rel in  parserResults.values:
                log.info("parseResults: %s" % str(rel))
                dp,value = rel
                if dp.dataType=="DERIVE" and (not dp.dpname.find("nection")>=0):
                    value=round(float(value)/300.0,3)
                data = {"moUid":moUid,
                            "title":cmd.title,
                             "componentType":cmd.componentType,
                             "templateUid":cmd.templateId,
                             "dataSource":cmd.dsname,
                             "dataPoint":dp.dpname,
                             "agent":"netcommand",
                             "value":value
                             }
                self.saveResult(data)
        except Exception,ex:
            log.error("解析命令行结果出错,%s" % ex.message)
            import traceback
            data = {"moUid":moUid,
                         "title":cmd.title,
                         "componentType":cmd.componentType,
                         "message":"解析命令行结果出错,%s" % traceback.format_exc(),
                         "severity":3,
                         "collector":cmd.manageObjConfig.cuid,
                         "agent":"netcommand"
                    }
            self.saveEvent(data)

    def getManageObjConfig(self):
        """
        功能:得到所有的设备配置
        返回:所有设备的配置列表
        作者:wl
        时间:2013-1-6
        """
        log.info("before getconfig")
        configResults = self.getManageObjConifgs()
        if configResults[0]:
            self.cmdConfigs=configResults[1]
            log.info("共计获取%d个设备的配置" % len(self.cmdConfigs))
        else:
            log.error(configResults[1])
        return self.cmdConfigs

    def fetchConfig(self):
        """
        功能:获取配置
        返回:deffered对象
        作者:wl
        时间:2013-1-6
        """
        def doFetchConfig(driver):
            try:
                yield defer.execute(self.getManageObjConfig)
                objIds= list(Set([c.manageObjConfig.objId
                                        for c in self.schedule]))
                self.updateConfig(driver.next(),objIds)
            except Exception,ex:
                raise
        return drive(doFetchConfig)

    def errorStop(self,why):
        """
        功能:出现错误,停止守护进程
        参数:错误信息
        作者:wl
        时间:2013-1-6
        """
        log.error(why)
        def stopNow():
            if reactor.running:reactor.stop()
        if reactor.running and not self.stopped:
            self.stopped = True
        reactor.callLater(1,stopNow)

    def start(self,driver):
        """
        功能:开始获取数据,循环调用
        参数:driver实例
        作者:wl
        时间:2013-1-6
        """
        ex = None
        try:
            yield self.fetchConfig()
        except Exception,ex:
            pass
        driveLater(self.configCycleInterval * 60,self.start)
        if ex:
            raise ex

    def run(self):
        """
        功能:启动reactor
        作者:wl
        时间:2013-1-6
        """
        log.info('启动命令行守护进程!')
        d = drive(self.start).addCallbacks(self.processSchedule,self.errorStop)
        reactor.run()
        
    def buildOptions(self):
        DeamonBase.buildOptions(self)
        self.parser.add_option('--csmconfig',dest='csmconfig',
                               default='CommandConfig',
                               help='命令行守护进程配置类,默认为CommandConfig')

if __name__ == '__main__':
    from products.netCommand.netcommand import netcommand
    z = netcommand()
    z.run()
