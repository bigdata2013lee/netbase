#coding=utf-8
import time
import Queue
from threading import Thread


sleepTime = 20 #秒

class RpnException(Exception):
    def __init__(self, e):
        Exception.__init__(self, e)
    

class RpnObject(object):
    __doc__ = """
    
    """
    def __init__(self, mo, tpl, value):
        """
        @param mo: 监控对象 
        @param tpl: 模板对象 
        """
        self.__mo= mo
        self.__tpl = tpl
        self.value = value
        
    def pv(self, dsName, dpName, defaultVal = None):
        """
        获取监控对象“性能”或 “状态”值的访求
        """
        if not (self.__mo or self.__tpl) : return defaultVal
        val = self.__mo.getPerfValue(self.__tpl.uname, dsName, dpName)
        if val is None: return defaultVal
        return val

    def pvs(self, v):
        return v
    
    def mattr(self,name,defaultVal = None):
        """
        获取监控对象属性
        """
        if hasattr(self.__mo, name):
            return getattr(self.__mo, name)
        return defaultVal
        

#-----------------------------------------------------------------------------#


class RpnThread(Thread):
    
    def run(self):
        while True:
            if RpnTools._datas.empty():
                time.sleep(1)
                continue
            
            data = RpnTools._datas.get(block=True)
            now = time.time()
            timeId = int(time.time())
            sleep = sleepTime
            if now - timeId >= sleepTime: sleep = 0
            
            time.sleep(sleep)
            RpnTools.dealRpn(data)
        
        


#-----------------------------------------------------------------------------#
            
class RpnTools(object):
    _poolSize = 20
    _datas = Queue.Queue() #
    _theadPool = []
    
    @classmethod
    def _initTheadPool(cls):
        for i in xrange(cls._poolSize):
            rth = RpnThread()
            cls._theadPool.append(rth)
            rth.setDaemon(True)
            rth.start()
            

    @staticmethod
    def receive(timeId, mo, rdata, rpnCode, callback):
        """
        接收实时数据，及相关参数，并保存到数据队列中
        """
        
        data = dict(timeId=timeId, mo = mo, rdata=rdata, rpnCode=rpnCode, callback=callback)
        RpnTools._datas.put(data)
    
    @staticmethod
    def execRpn(rpn, rpnCode=""):
        """
        执行RPN公式代码
        @param rpn: <RpnObject>
        @param rpnCode: python code
        """
        try:
            o = {"r": rpn, "value": None}
            exec(rpnCode,o)
            return o.get("value")
        except Exception, e :
            raise RpnException(e)
    
    @staticmethod    
    def dealRpn(data):
        """
        RPN处理分析
        """
        from products.netAnalysis.utils import RpycUtil
        
        mo = data.get("mo")
        rdata = data.get("rdata")
        rpnCode = data["rpnCode"]
        callback = data['callback']
        tpl = RpycUtil.getMonitorOjbTpl(mo, rdata["templateUid"])
        _value = rdata["value"]
        rpnObj = RpnObject(mo, tpl, _value)
        value = RpnTools.execRpn(rpnObj, rpnCode)
        
        callback(value)
        
        
    
if __name__ == "__main__":
    
    mycode = """
cpu = 90
if cpu >= 100:
    value = "%s /100" %cpu
    print value
    exit()  

value =  (r.pvs(103) + r.pvs(3)) / 1
    """
    
    rpn = RpnObject(0,0)
    rs = RpnTools.execRpn(rpn, mycode)
    
    
    
    
    
    
    
    
    
    
