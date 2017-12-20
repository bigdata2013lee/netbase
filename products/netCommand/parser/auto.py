#coding=utf-8
###########################################################################
#
#
#此软件版权为深圳商之杰科技有限公司所有,更多信息请访问www.netbase.asia
#
#
###########################################################################

import re
NagParser = re.compile(r"""([^ =']+|'(.*)'+)=([-0-9.eE]+)([^;]*;?){0,5}""")
CacParser = re.compile(r"""([^ :']+|'(.*)'+):([-0-9.]+)""")

from products.netUtils.Utils import getExitMessage
from products.netCommand.commandParser import CommandParser

class auto(CommandParser):
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
        elif CacParser.search(output):
            msg, values = '', output
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
            for dp in cmd.points:       # FIXME: linear search
                if dp.dpname == label:
                    result.values.append( (dp, value) )
                    break
        return result

