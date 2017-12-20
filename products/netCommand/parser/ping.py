#coding=utf-8
###########################################################################
#
#
#此软件版权为深圳商之杰科技有限公司所有,更多信息请访问www.netbase.asia
#
#
###########################################################################

import re
from products.netUtils.Utils import getExitMessage
from products.netCommand.commandParser import CommandParser

class ping(CommandParser):
    """
    功能:Ping命令行输出结果的解析器
    作者:wl
    时间:2013-1-7
    """
    def processResults(self, cmd, result):
        """
        功能:处理命令行输出的结果
        参数:命令行对象,结果对象
        返回:结果对象
        作者:wl
        时间:2013-1-7
        """
        output = cmd.result.output
        exitCode = cmd.result.exitCode
        severity = cmd.severity
        if exitCode==0:
            valueLine= output.splitlines(False)[-2:]
            pingLR=valueLine[0].split(",")[-3:-1]
            pingReceived,pingLoss=[lr.strip().split()[0].strip("%") for lr in pingLR]
            rrtValueList=valueLine[1].split("=")[1].strip()
            minRtt,avgRtt,maxRtt,mdevRtt=[float(x) for x in rrtValueList .split()[0].split("/")]
            values=dict(pingReceived=pingReceived,pingLoss=pingLoss,minRtt=minRtt,avgRtt=avgRtt,maxRtt=maxRtt,mdevRtt=mdevRtt)
            for dp in cmd.points:
                result.values.append( (dp, values.get(dp.dpname) ))
        else:
            msg = output.strip() or '命令: %s - 编号: %s - 消息: %s' % (
            cmd.command, exitCode, getExitMessage(exitCode))
            if exitCode == 2:
                severity = min(severity + 1, 5)
            component=cmd.componentId
            if component:moUid=cmd.componentId
            else:moUid=cmd.manageObjConfig.objId
            result.events.append({"moUid":moUid,
                          "title":cmd.title,
                          "componentType":cmd.componentType,
                          "message":"%s" % msg,
                          "severity":severity,
                          "collector":cmd.manageObjConfig.cuid,
                          "agent":"netcommand"
            })
        return result

