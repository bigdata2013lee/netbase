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

class adpAllInfo(CommandParser):
    """
    功能raid输出结果的默认解析器
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
            valueLines= output.splitlines()
            raidNames=["productName","serialNo","memorySize","vdsOnLineDisk","vdsRebuildDisk","vdsCriticalDisks","pdsDisks","pdsCriticalDisks","pdsFailedDisks"]
            raidValues=[i.split(":")[-1].strip() for i in valueLines]
            values=dict(zip(raidNames,raidValues))
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
