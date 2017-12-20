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

class pwd(CommandParser):
    """
    功能:命令行输出结果的默认解析器
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
        output = output.split('\n')[0].strip()
        exitCode = cmd.result.exitCode
        severity = cmd.severity
        if output.find('|') >= 0:
            msg, values = output.split('|', 1)
        else:
            msg, values = output, ''
        msg = msg.strip() or '命令: %s - 编号: %s - 消息: %s' % (
            cmd.command, exitCode, getExitMessage(exitCode))
        if exitCode != 0:
            if exitCode == 2:
                severity = min(severity + 1, 5)
            result.events.append(dict(device=cmd.manageObjConfig.manageId,
                                      summary=msg,
                                      severity=severity,
                                      message=msg,
                                      performanceData=values,
                                      eventKey=None,
                                      eventClass=None,
                                      componentId=cmd.componentId,
                                      componentType=cmd.componentType))

        for dp in cmd.points:
            result.values.append( (dp, output) )
        return result

