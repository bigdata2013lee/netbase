#coding=utf-8
    
class BaseTask(object):
    
    def __init__(self,taskResult,taskConfig,addressIp):
        """
                初始化任务类
        """
        self._taskResult=taskResult
        self._taskConfig=taskConfig
        self._addressIp=addressIp
    
    def executeTask(self,resultCached):
        """
                执行任务
        """
        pass
                   
    def processResults(self,rs):
        """
                处理获取的结果
        """
        pass
        
    

class SimpleTaskFactory(object):
    """
        简单任务工厂
    """
    def build(self,results,_taskClass,addressIp):
        return _taskClass(results,self.config,addressIp)

    def reset(self):
        self.config = None