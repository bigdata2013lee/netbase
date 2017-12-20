#coding=utf-8
import re
from products.netUtils.Utils import getExitMessage
from products.netCommand.commandParser import CommandParser
NagParser = re.compile(r"""([^ =']+|'(.*)'+)=([-0-9.eE]+)([^;]*;?){0,5}""")
CacParser = re.compile(r"""([^ :']+|'(.*)'+):([-0-9.]+)""")
class middlewareDefaultParser(CommandParser):
  
    def processResults(self, cmd, result):

        output = cmd.result.output
        output = output.split('\n')[0].strip()
        exitCode = cmd.result.exitCode
        severity = cmd.severity
        component=cmd.componentId
        if component:moUid=cmd.componentId
        else:moUid=cmd.manageObjConfig.objId
        if output.find('|') >= 0:
            msg, values = output.split('|', 1)
            for value in values.split(' '):
                label=value.split("=")[0]
                val=value.split("=")[1]
                for dp in cmd.points:
                    if dp.dpname == label:
                        result.values.append( (dp, val) )
                        break
        else:
            msg, values = output, ''
        msg = msg.strip() or '命令: %s - 编号: %s - 消息: %s' % (
            cmd.command, exitCode, getExitMessage(exitCode))
        
        if exitCode != 0 or not values:
            if not msg.find("STATUS OK")>=0:
                severity=5
                msg="中间件%s连接失败!"%cmd.manageObjConfig.manageId
            else:
                severity = min(severity + 1, 5)
        else:
            severity=0
        result.events.append({"moUid":moUid,
                  "title":cmd.title,
                  "componentType":cmd.componentType,
                  "message":"%s" % msg,
                  "severity":severity,
                  "eventClass":"/status",
                  "collector":cmd.manageObjConfig.cuid,
                  "agent":"netcommand"})
        return result

