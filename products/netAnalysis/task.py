#coding=utf-8
import time
import Queue
from threading import Thread

from products.netAnalysis.utils import TaskProcessUtil as TPU, StatusUtil
from products.netAnalysis.utils import RpycUtil
from products.netAnalysis.rloc import RecordLastOriginalCache
import logging
import sys

    
def _getComponent(dev, componentCollectionsName, rdata):
    """
        得到设备对象的组件
        @param dev:设备对象
        @param rdata: 实时数据
        @param componentCollectionsName: 取得组件列表的方法名
    """
    component = None
    components = getattr(dev,componentCollectionsName)
    for com in components:
        if com.getUid() == rdata.get('component', ''):
            component = com
            break
    return component


def _dealFun(mo, timeId, rdata):

        tpl = RpycUtil.getMonitorOjbTpl(mo, rdata["templateUid"])
        dataPoint = TPU.getDataPoint(tpl, rdata)
        if not dataPoint: return None
 
        if dataPoint.get("valueType") == "String": #文本状态
            TPU.dealStringDataPoint(timeId, mo, dataPoint, rdata)

        if dataPoint.get("valueType") == "Num": #数值性能
            TPU.dealNunDataPoint(timeId, mo, tpl, dataPoint, rdata)
            

class TaskThread(Thread):
    
    def __init__(self, taskCls):
        Thread.__init__(self)
        self._taskCls = taskCls
    
    def run(self):
        taskCls = self._taskCls
        #t1 = time.time()
        while True:
            if taskCls._q.qsize() > 0:
                item = taskCls._q.get()
                try:
                    taskCls.deal(item[0], item[1])
                except:
                    logging.warn("数据分析处理过程出现异常")
                    logging.exception(sys.exc_info())
                    
            else:

                time.sleep(2)

                
        
    
      
    
class TaskChain(object):
    
    def __init__(self):
        self._tasks = []
        
    def append(self, task):
        if not task or not isinstance(task, Task): return
        self._tasks.append(task)
        return self
    
    def dealData(self, timeId, rdata):
        for task in self._tasks:
            task.__class__._q.put((timeId, rdata))
        
class Task(object):
        
    def initTaskThreads(self, num):
        for n in xrange(num):
            th = TaskThread(self.__class__)
            self.__class__._taskThreads.append(th)
            th.setDaemon(True)
            th.start()
            
    def __init__(self, qNum=5000, taskThreadsNum=10):
        if not hasattr(self.__class__, '_inited'):
            self.__class__._inited = False
            
        if self.__class__._inited: return
        self.__class__._q = Queue.Queue(qNum)
        self.__class__._taskThreads = []
        self.initTaskThreads(taskThreadsNum)
        self.__class__._inited = True
        
##----------------------------------------原始数据记录任务---------------------------------------------------##
class RecordLastOriginalData(Task):
    """
    记录最后一次入性能数据库的原始数据
    """
    @staticmethod
    def deal(timeId, rdata):
        if not rdata: return
        recordId = TPU.getRlodRecordId(rdata)
        record = {'timeId': timeId, 'value': rdata['value']}
        RecordLastOriginalCache.set(recordId, record)
        
            
##----------------------------------------设备分析---------------------------------------------------##
class DevicePerfmsTask(Task):
    """
        性能\状态 数据分析
        通过 模板->数据源->数据点, 得到数据点类型
        分析差值|绝对值|原始值，保存性能数据
    """
    @staticmethod
    def deal(timeId, rdata):
        moUid = rdata["moUid"]
        mo = RpycUtil.findDeviceByUid(moUid)
        if not mo:
            logging.warn("Warning: Can't find Device mo:%s" %moUid)
            return 
        
        _dealFun(mo, timeId, rdata)

        
##-----------------------------------站点分析-------------------------------------------------------##
class WebsitePerfmsTask(Task):
    """
        性能\状态 数据分析
        通过 模板->数据源->数据点, 得到数据点类型
        分析差值|绝对值|原始值，保存性能数据
    """
    @staticmethod
    def deal(timeId, rdata):
        moUid = rdata["moUid"]
        mo = RpycUtil.findWebsiteByUid(moUid)
        if not mo:
            logging.warn("Warning: Can't find Website mo:%s" %moUid)
            return 
        
        _dealFun(mo, timeId, rdata)
        
##----------------------------------------网络设备分析---------------------------------------------------##
class NetworkPerfmsTask(Task):
    """
        性能\状态 数据分析
        通过 模板->数据源->数据点, 得到数据点类型
        分析差值|绝对值|原始值，保存性能数据
    """
    @staticmethod
    def deal(timeId, rdata):
        moUid = rdata["moUid"]
        mo = RpycUtil.findNetworkByUid(moUid)
        if not mo:
            print "Warning: Can't find Network mo:%s" %moUid
            return 
        
        _dealFun(mo, timeId, rdata)


##----------------------------------------中间件分析---------------------------------------------------##
class ApachePerfmsTask(Task):
    """
        性能\状态 数据分析
        通过 模板->数据源->数据点, 得到数据点类型
        分析差值|绝对值|原始值，保存性能数据
    """
    @staticmethod
    def deal(timeId, rdata):
        moUid = rdata["moUid"]
        mo = RpycUtil.findApacheByUid(moUid)
        if not mo:
            print "Warning: Can't find Apache mo:%s" %moUid
            return 
        
        _dealFun(mo, timeId, rdata)

class TomcatPerfmsTask(Task):
    """
        性能\状态 数据分析
        通过 模板->数据源->数据点, 得到数据点类型
        分析差值|绝对值|原始值，保存性能数据
    """
    @staticmethod
    def deal(timeId, rdata):
        moUid = rdata["moUid"]
        mo = RpycUtil.findTomcatByUid(moUid)
        if not mo:
            print "Warning: Can't find Tomcat mo:%s" %moUid
            return 
        
        _dealFun(mo, timeId, rdata)
        
class NginxPerfmsTask(Task):
    """
        性能\状态 数据分析
        通过 模板->数据源->数据点, 得到数据点类型
        分析差值|绝对值|原始值，保存性能数据
    """
    @staticmethod
    def deal(timeId, rdata):
        moUid = rdata["moUid"]
        mo = RpycUtil.findNginxByUid(moUid)
        if not mo:
            print "Warning: Can't find Nginx mo:%s" %moUid
            return 
        
        _dealFun(mo, timeId, rdata)
        
class IisPerfmsTask(Task):
    """
        性能\状态 数据分析
        通过 模板->数据源->数据点, 得到数据点类型
        分析差值|绝对值|原始值，保存性能数据
    """
    
    @staticmethod
    def deal(timeId, rdata):
        moUid = rdata["moUid"]
        mo = RpycUtil.findIisByUid(moUid)
        if not mo:
            print "Warning: Can't find Iis mo:%s" %moUid
            return 
        
        _dealFun(mo, timeId, rdata)


##------------------------------------接口分析-------------------------------------------##
class InterfacePerfmsTask(Task):
    """
        性能\状态 数据分析
        通过 模板->数据源->数据点, 得到数据点类型
        分析差值|绝对值|原始值，保存性能数据
    """
    @staticmethod
    def deal(timeId, rdata):
        moUid = rdata["moUid"]
        mo = RpycUtil.findDeviceComponent("IpInterface", moUid)
        if not mo:
            logging.warn("Warning: Can't find IpInterface mo:%s" %moUid)
            return 
        
        _dealFun(mo, timeId, rdata)
            
##------------------------------------进程分析-------------------------------------------##
class ProcessPerfmsTask(Task):
    """
        性能\状态 数据分析
        通过 模板->数据源->数据点, 得到数据点类型
        分析差值|绝对值|原始值，保存性能数据
    """
    @staticmethod
    def deal(timeId, rdata):
        moUid = rdata["moUid"]
        mo = RpycUtil.findDeviceComponent("Process", moUid)
        if not mo:
            logging.warn("Warning: Can't find Process mo:%s" %moUid)
            return 
        
        _dealFun(mo, timeId, rdata)


##------------------------------------文件系统分析-------------------------------------------##
class FileSystemPerfmsTask(Task):
    """
        性能\状态 数据分析
        通过 模板->数据源->数据点, 得到数据点类型
        分析差值|绝对值|原始值，保存性能数据
    """
    @staticmethod
    def deal(timeId, rdata):
        moUid = rdata["moUid"]
        mo = RpycUtil.findDeviceComponent("FileSystem", moUid)
        if not mo:
            logging.warn("Warning: Can't find FileSystem mo:%s" %moUid)
            return 
        
        _dealFun(mo, timeId, rdata)

        
##-----------------------------------事件分析-------------------------------------------------------##

class EventTask(Task):
    @staticmethod
    def deal(timeId, rdata):
        eventInfo = {
                     "moUid":rdata.get("moUid"),
                     "title":rdata.get("title"),
                     'componentType': rdata.get("componentType"),
                     'evtKey':rdata.get("evtKey"),
                     'clearKey':rdata.get("clearKey"),
                     'message':rdata.get("message"),
                     'severity':rdata.get("severity"),
                     'agent':rdata.get("agent",""),
                     'eventClass':rdata.get("eventClass",""),
                     'collectPointUid':rdata.get("collectPointUid",""),
                     'collector':rdata.get("collector","")
         }
        
        statusTableName = TPU.getStatusTableName(rdata)
        if eventInfo.get("eventClass","") == "/status": #处理状态事件，插入状态值至status表中
            dbName = TPU.getDbName(rdata)
            statusValue = 1 if 0 == eventInfo.get("severity", 0) else 0
            RpycUtil.insertStatusData(statusValue, dbName, statusTableName)
                
            
        RpycUtil.sendEvent(eventInfo)
    
    

#-----------------------------------------------------------------------------------

if __name__ == '__main__':
    pass




