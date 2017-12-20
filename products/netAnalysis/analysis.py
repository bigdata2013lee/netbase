#coding=utf-8

import time
import types
from threading import Thread
import task
import logging
import sys



def _taskChainDealData(analysis, chain, dataArea):
    """
    任务链处理数据
    @param analysis: 分析器
    @param chain: 任务链
    @param dataArea: 数据区  
    """
    while True:
        rdata = None
        try:
            
            rdata = analysis.client.got(dataArea) #去远程redis实时数据库取数据
            
            if False and dataArea in []:
                print "%s rdata:" %dataArea
                if rdata is None: print "No data"
                else: print rdata.value
        except:
            logging.exception(sys.exc_info())
            
        if rdata is not None:
            timeId = rdata.timeId
            rdata  = rdata.value
            chain.dealData(timeId, rdata) #往队列Queue中放数据
        else:
            time.sleep(5)
            
class Analysis(object):
    """
        分析器主程序，开启多个分析任务，每个任务分析不同的数据，
        同一份数据根据业务的不同，可能会有多次分析
        （例如收集器收集的cpu数据，根据该数据，可能需要产生事件，同时需要根据用户设置的不同，计算并保存性能数据），
        所以任务以任务链的方式执行，为了提高处理速度，任务链中每一个节点以多线程方式运行。
    """
    def setDBClient(self, client):
        self.client = client
    
    def work(self):
        attributes = dir(self)
        workMethodNames = [attr for attr in attributes if attr.find('workFor') == 0 
                     and type(getattr(self, attr)) == types.MethodType]
        for name in workMethodNames:
            method = getattr(self, name)
            t = Thread(target=method)
            t.setDaemon(True)
            t.start()
            time.sleep(1)

    def workForDeviceData(self):
        "workForDevicePerf"
        chain = task.TaskChain()
        #开启工作线程去队列Queue中取数据
        chain.append(task.RecordLastOriginalData())
        chain.append(task.DevicePerfmsTask())
        _taskChainDealData(self, chain, 'Device')
        
  
    def workForNetworkData(self):
        print "workForNetworkPerf"
        chain = task.TaskChain()
        #开启工作线程去队列Queue中取数据
        chain.append(task.RecordLastOriginalData())
        chain.append(task.NetworkPerfmsTask())
        _taskChainDealData(self, chain, 'Network')
        
#-------------------------------------------------------------------------------#        
    def workForApacheData(self):
        print "workForApachePerf"
        chain = task.TaskChain()
        #开启工作线程去队列Queue中取数据
        chain.append(task.RecordLastOriginalData())
        chain.append(task.ApachePerfmsTask())
        _taskChainDealData(self, chain, 'MwApache')
    
    def workForTomcatData(self):
        print "workForTomcatPerf"
        chain = task.TaskChain()
        #开启工作线程去队列Queue中取数据
        chain.append(task.RecordLastOriginalData())
        chain.append(task.TomcatPerfmsTask())
        _taskChainDealData(self, chain, 'MwTomcat')
    
    def workForNginxData(self):
        print "workForNginxPerf"
        chain = task.TaskChain()
        #开启工作线程去队列Queue中取数据
        chain.append(task.RecordLastOriginalData())
        chain.append(task.NginxPerfmsTask())
        _taskChainDealData(self, chain, 'MwNginx')
        
    def _workForIisData(self):
        print "workForIisPerf"
        chain = task.TaskChain()
        #开启工作线程去队列Queue中取数据
        chain.append(task.RecordLastOriginalData())
        chain.append(task.IisPerfmsTask())
        _taskChainDealData(self, chain, 'MwIis')
#-------------------------------------------------------------------------------# 
    def workForWebsiteData(self):
        "workForWebsiteData"
        chain = task.TaskChain()
        #开启工作线程去队列Queue中取数据
        chain.append(task.RecordLastOriginalData())
        chain.append(task.WebsitePerfmsTask())
        _taskChainDealData(self, chain, 'Website')
        
        
    def workForInterfaceData(self):
        "workForInterfaceData"
        chain = task.TaskChain()
        #开启工作线程去队列Queue中取数据
        chain.append(task.RecordLastOriginalData())
        chain.append(task.InterfacePerfmsTask())
        _taskChainDealData(self, chain, 'IpInterface')
        
    def workForProcessData(self):
        "workForProcessData"
        chain = task.TaskChain()
        #开启工作线程去队列Queue中取数据
        chain.append(task.RecordLastOriginalData())
        chain.append(task.ProcessPerfmsTask())
        _taskChainDealData(self, chain, 'Process')
        
    def workForFileSystemData(self):
        "workForFileSystemData"
        chain = task.TaskChain()
        #开启工作线程去队列Queue中取数据
        chain.append(task.RecordLastOriginalData())
        chain.append(task.FileSystemPerfmsTask())
        _taskChainDealData(self, chain, 'FileSystem')
        
    
    def workForEventsData(self):
        "workForEventsData"
        chain = task.TaskChain()
        chain.append(task.EventTask())
        _taskChainDealData(self, chain, 'events')
        




