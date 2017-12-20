#coding=utf-8
###########################################################################
#
#
#此软件版权为深圳商之杰科技有限公司所有,更多信息请访问www.netbase.asia
#
#
###########################################################################

import re
import time
import commands
from products.netCollectPoint.task.BaseTask import BaseTask
NagParser = re.compile(r"""([^ =']+|'(.*)'+)=([-0-9.eE]+)([^;]*;?){0,5}""")
CacParser = re.compile(r"""([^ :']+|'(.*)'+):([-0-9.]+)""")
class CachedResult(object):
    def __init__(self,rsValue):
        self.timeStamp=time.time()
        self.rsValue=rsValue

class HttpTask(BaseTask):
    """
        功能:Http命令行输出结果的解析器
        作者:wl
        时间:2013-1-7
    """
    cachedTime=300
    def executeCommand(self,cmd):
        """
                执行命令
        """
        time.sleep(0.1)#防止对命令的过于频繁执行出错
        self.command = 'exec %s' % cmd
        rs=commands.getoutput(self.command)
        return rs
    
    def executeTask(self,resultCached):
        """
                执行任务(在300秒之内执行过的命令暂不执行)
        """
        self._command = self._taskConfig.get("command")
        if resultCached.has_key(self._command):
            cacRs=resultCached[self._command]
            if time.time()-cacRs.timeStamp<=self.cachedTime:
                return cacRs.rsValue
        rs=self.executeCommand(self._command)
        if not rs.find("HTTP OK"):rs=self.executeCommand(self._command)
        resultCached[self._command]=CachedResult(rs)
        return rs
        
    def processResults(self,rs):
        """
                功能:处理Http的输出结果
                参数:结果对象
                作者:wl
                时间:2013-12-3
        """
        output = rs.split('\n')[0].strip()
        moUid=self._taskConfig.get("objId")
        title=self._taskConfig.get("title")
        cptUid=self._taskConfig.get("cptUid")
        cptTitle=self._taskConfig.get("cptTitle")
        collector=self._taskConfig.get("cuid")
        manageId=self._taskConfig.get("manageId")
        dataSource=self._taskConfig.get("dsname")
        templateId=self._taskConfig.get("templateId")
        severity=self._taskConfig.get("severity")
        componentType=self._taskConfig.get("componentType")
        if output.find('|') >= 0:
            msg, values = output.split('|', 1)
        else:
            msg, values = output, ''
        if msg.find("HTTP OK")>=0:
            severity=0
            msg=u"站点%s连接成功!"%manageId
        else:
            severity=5
            msg=u"站点%s连接失败!"%manageId
        self._taskResult[self._addressIp][moUid]=[]
        self._taskResult[self._addressIp][moUid].append({"moUid":moUid,
                                                "title":title,
                                                "componentType":componentType,
                                                "message":"%s" % msg,
                                                "severity":severity,
                                                "eventClass":"/status",
                                                "collector":collector,
                                                "agent":"netcollect",
                                                "collectPointTitle":cptTitle,
                                                "collectPointUid":cptUid,
                                                "insertType":"event"})
        for value in values.split(' '):
            if value.find('=') > 0:
                parts = NagParser.match(value)
            else:
                parts = CacParser.match(value)
            if not parts: continue
            label = parts.group(1).replace("''", "'")
            try:
                value = float(parts.group(3))
            except:
                value = 'U'
            
            for dpname in self._taskConfig.get("points"):
                if dpname == label:
                    data = {"moUid":moUid,
                            "title":title,
                            "componentType":componentType,
                            "templateUid":templateId,
                            "dataSource":dataSource,
                            "dataPoint":dpname,
                            "agent":"netcollect",
                            "collectPointTitle":cptTitle,
                            "collectPointUid":cptUid,
                            "value":value,
                            "insertType":"value"}
                    self._taskResult[self._addressIp][moUid].append(data)
                    break

