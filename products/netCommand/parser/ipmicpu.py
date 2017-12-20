#coding=utf-8
###########################################################################
#
#
#此软件版权为深圳商之杰科技有限公司所有,更多信息请访问www.netbase.asia
#
#
###########################################################################

from products.netUtils.Utils import getExitMessage
from products.netCommand.commandParser import CommandParser
class ipmicpu(CommandParser):
    """
    功能:ipmi温度命令行输出结果的解析器
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
            output = output.split('\n')[0].strip()
            tempValues= output.split(":")
            status=tempValues[3].strip()[1:-1]
            if status=="OK":
                severity=0
                msg = '%s状态正常!'%cmd.title
            else:
                severity=5
                msg = '%s状态异常!'%cmd.title
            temperature=tempValues[2].strip().split(" ",1)[0]
            rs=dict(status=status,temperature=temperature)
            for dp in cmd.points:
                result.values.append( (dp,rs.get(dp.dpname)))
        else:
            severity=5
            msg = output.strip() or 'ipmi执行命令出错!'
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
        return result

