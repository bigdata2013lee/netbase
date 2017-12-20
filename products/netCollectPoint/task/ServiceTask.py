#coding=utf-8
###########################################################################
#
#
#此软件版权为深圳商之杰科技有限公司所有,更多信息请访问www.netbase.asia
#
#
###########################################################################

import re
import socket
from products.netCollectPoint.task.BaseTask import BaseTask
NagParser = re.compile(r"""([^ =']+|'(.*)'+)=([-0-9.eE]+)([^;]*;?){0,5}""")
CacParser = re.compile(r"""([^ :']+|'(.*)'+):([-0-9.]+)""")
class ServiceTask(BaseTask):
    """
        服务端口执行任务
    """
    
    def executeTask(self,resultCached):
        """
                执行任务
        """
        ipaddress=self._taskConfig.get("manageId")
        port=self._taskConfig.get("port")
        s=socket.socket()
        s.settimeout(5)
        try:
            s.connect((ipaddress,int(port)))
            return True
        except Exception,e:
            print e
        finally:
            s.close()
        return False

    def processResults(self,rs):
        """
                功能:处理命令行输出的结果
                参数:命令行对象,结果对象
                返回:结果对象
                作者:wl
                时间:2013-1-7
        """
        title=self._taskConfig.get("title")
        cptUid=self._taskConfig.get("cptUid")
        collector=self._taskConfig.get("cuid")
        severity=self._taskConfig.get("severity")
        moUid=self._taskConfig.get("componentId")
        collectorIp=self._taskConfig.get("collectorIp")
        componentType=self._taskConfig.get("componentType")
        msg=u"IP Service%s已停止!"%title
        if rs:
            severity=0
            msg=u"IP Service%s已启动!"%title
        eventKey="%s|%s|%s"%(moUid,severity,collector)
        self._taskResult[collectorIp][eventKey]={"moUid":moUid,
                      "title":title,
                      "componentType":componentType,
                      "message":msg,
                      "severity":severity,
                      "eventClass":"/status",
                      "collector":collector,
                      "agent":"netcollect",
                      "collectPoint":cptUid,
                      "insertType":"event"
        }
        

