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
NagParser = re.compile(r"""([^ =']+|'(.*)'+)=([-0-9.eE]+)([^;]*;?){0,5}""")
CacParser = re.compile(r"""([^ :']+|'(.*)'+):([-0-9.]+)""")
class http(CommandParser):
    """
    功能:Http命令行输出结果的解析器
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
                if not msg.find("HTTP OK")>=0:
                    severity=5
                    msg="站点%s连接失败!"%cmd.manageObjConfig.manageId
            else:
                severity = min(severity + 1, 5)
        else:severity=0
        component=cmd.componentId
        if component:moUid=cmd.componentId
        else:moUid=cmd.manageObjConfig.objId
        result.events.append({"moUid":moUid,
                      "title":cmd.title,
                      "componentType":cmd.componentType,
                      "message":"%s" % msg,
                      "severity":severity,
                      "eventClass":"/status",
                      "collector":cmd.manageObjConfig.cuid,
                      "agent":"netcommand"
        })
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
            for dp in cmd.points:
                if dp.dpname == label:
                    result.values.append( (dp, value) )
                    break
        return result

