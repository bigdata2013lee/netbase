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
class multiCpu(CommandParser):
    """
    功能:多核cpu命令行输出结果的解析器
    作者:wl
    时间:2013-12-13
    """
    def processResults(self, cmd, result):
        """
                功能:处理命令行输出的结果
                参数:命令行对象,结果对象
                返回:结果对象
                作者:wl
                时间:2013-12-13
        """
        output = cmd.result.output
        cpuRates=[cpu.rsplit(":",1)[1].strip() for cpu in output.splitlines()]
        exitCode = cmd.result.exitCode
        severity = cmd.severity
        msg ='命令: %s - 编号: %s - 消息: %s' % (
            cmd.command, exitCode, getExitMessage(exitCode))
        if exitCode != 0:
            msg="%s获取CPU信息失败!"%cmd.manageObjConfig.manageId
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
        value=""
        for i in xrange(len(cpuRates)):
            value+="CPU%s=%s "%(i,cpuRates[i])
        if value:
            for dp in cmd.points:
                if dp.dpname == "multiCPU":
                    result.values.append( (dp, value) )
                    break
        return result

