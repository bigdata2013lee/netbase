#coding=utf-8
import time
import Queue
import socket
import pickle
import threading
from products.netCollectPoint.task.BaseTask import SimpleTaskFactory


def importClass(modulePath, classname=""):
    """
    Import a class from the module given.

    @param modulePath: path to module in sys.modules
    @type modulePath: string
    @param classname: name of a class
    @type classname: string
    @return: the class in the module
    @rtype: class
    """
    try:
        if not classname: 
            classname = modulePath.split(".")[-1]
            modulePath = ".".join(modulePath.split(".")[0:-1])
        try:
            __import__(modulePath, globals(), locals(), classname)
            mod = sys.modules[modulePath]
        except (ValueError, ImportError, KeyError), ex:
            raise ex

        return getattr(mod, classname)
    except AttributeError:
        raise ImportError("Failed while importing class %s from module %s" % (classname, modulePath))


cmdResult={}
class ThreadTask(threading.Thread):
    """
        多线程任务
    """
    def __init__(self,taskQueue):
        threading.Thread.__init__(self)
        self.taskQueue=taskQueue
        self.start()
   
    def run(self):
        while True:
            try:
                task= self.taskQueue.get(block= True)
                rs=task.executeTask(cmdResult)
                task.processResults(rs)
            except Exception,e:
                print e
                time.sleep(10) #出现异常就睡眠10秒
            time.sleep(0.1)

class TaskPool(object):
    """
        任务池
    """
    def __init__(self,threadNum):
        """
                初始化
        """
        self.taskQueue = Queue.Queue()
        self.threads=[]
        self.__initTaskPool(threadNum)
        
    def __initTaskPool( self,threadNum):
        """
                初始化任务池
        """
        for i in xrange(threadNum):
            self.threads.append(ThreadTask(self.taskQueue))
            
    def addTask(self,task):
        """
                添加任务
        """
        #任务入队，Queue内部实现了同步机制
        self.taskQueue.put(task)

class netcollectserver(object):
    """
        收集点守护进程
    """
    threadNum=10 #线程数
    allConfigs={}
    results={}
    def __init__(self,taskFactory,port):
        """
                初始化任务池
        """
        self.tp=TaskPool(self.threadNum)
        self._taskFactory = taskFactory
        self.port=port
    
    def _updateConfig(self):
        """
                更新配置
        """
        while True:
            self._splitConfiguration()
            time.sleep(300)
    
    def _newTask(self,taskClass,config,results,addressIp):
        self._taskFactory.reset()
        self._taskFactory.config = config
        return self._taskFactory.build(results,taskClass,addressIp)

    def _splitConfiguration(self):
        """
                分割配置,生成任务
        """
        for addressIp,configs in self.allConfigs.iteritems():
            for config in configs:
                taskName=config.get("taskName")
                taskObj = importClass("products.netCollectPoint.task.%s"%taskName,taskName)
                self.tp.addTask(self._newTask(taskObj,config,self.results,addressIp))

    def _tcpListen(self):
        """
        TCP监听程序
        """
        serSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        serSocket.bind(("0.0.0.0",self.port))
        serSocket.listen(10)
        while True:
            __configData=""
            clientSock,addr = serSocket.accept()
            print "%s连接来自%s"%(time.strftime("%Y-%m-%d %H:%M:%S"),addr)
            while True:
                try:
                    __tmpData=clientSock.recv(1024)
                    if not __tmpData:
                        break
                    __configData+=__tmpData
                    if __configData.startswith("<<config:") and __configData.endswith(">>"):
                        self.allConfigs[addr[0]]=pickle.loads(__configData[9:-2])
                        print "%s:更新配置共计%s条"%(time.strftime("%Y-%m-%d %H:%M:%S"),len(pickle.loads(__configData[9:-2])))
                        if not self.results.has_key(addr[0]):self.results[addr[0]]={}
                        clientSock.send("<<result:%s>>"%pickle.dumps(self.results[addr[0]].values()))
                except:
                    print "%s接收%s配置数据失败!"%(time.strftime("%Y-%m-%d %H:%M:%S"),addr)
            clientSock.close()
        serSocket.close()
        
    def runTask(self):
        """
                执行任务
        """
        tuc=threading.Thread(target=self._updateConfig)
        tuc.start()
        ttl=threading.Thread(target=self._tcpListen)
        ttl.setDaemon(True)
        ttl.start()
        

if __name__=="__main__" :
    import sys
    port=8888
    if len(sys.argv) >= 1:  int(sys.argv[0])
    stf=SimpleTaskFactory()
    ncs=netcollectserver(stf,port)
    ncs.runTask()
