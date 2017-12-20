#coding=utf-8
###########################################################################
#
#
#此软件版权为深圳商之杰科技有限公司所有,更多信息请访问www.netbase.asia
#
#
###########################################################################

__doc__ = """python性能数据收集客户端
"""
from products.dataCollector.baseClient import BaseClient
from twisted.internet.defer import Deferred, DeferredList
from twisted.python.failure import Failure
import logging
log = logging.getLogger("PythonClient")

class PythonClient(BaseClient):
    """
    实现python的客户端
    """
    def __init__(self, device=None, datacollector=None, plugins=[]):
        """
        初始化
        @param device:设备
        @param datacollector: 收集器
        @param plugins: 数据收集插件
        """
        BaseClient.__init__(self, device, datacollector)
        self.hostname = device.id
        self.plugins = plugins
        self.results = []


    def run(self):
        """
        Start Python collection.
        """
        deferreds = []
        for plugin in self.plugins:
            log.debug("运行收集插件%s", plugin.name())
            r = plugin.collect(self.device, log)
            if isinstance(r, Deferred):
                deferreds.append(r)
                r.addBoth(self.collectComplete, plugin)
            else:
                log.debug("运行%s的结果是: %s", plugin.name(), str(r))
                self.results.append((plugin, r))
        
        dl = DeferredList(deferreds)
        dl.addCallback(self.collectComplete, None)


    def collectComplete(self, r, plugin):
        """
        Twisted deferred error callback used to store the
        results of the collection run

        @param r: result from the collection run
        @type r: result or Exception
        @param plugin: Python-based performance data collector plugin
        @type plugin: plugin object
        """
        if plugin is None:
            self.clientFinished()
            return

        if isinstance(r, Failure):
            log.warn("运行%s时出错: %s", plugin.name(), r.getErrorMessage())
        else:
            log.debug("运行%s的结果是: %s", plugin.name(), str(r))
            self.results.append((plugin, r))


    def clientFinished(self):
        """
        Stop the collection of performance data
        """
        log.info("Python客户端完成设备%s的收集工作" % self.device.id)
        if self.datacollector:
            self.datacollector.clientFinished(self)


    def getResults(self):
        """
        Return the results of the data collection.
        To be implemented by child classes

        @return: list of results
        @rtype: list of results
        """
        return self.results
