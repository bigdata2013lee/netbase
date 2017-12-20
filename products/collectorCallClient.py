#coding:utf-8
import ssl
import pickle
import socket
import time


indexMap = dict(ckIndex=0)

def getCmdIndex():
    indexMap["ckIndex"] +=1
    return indexMap["ckIndex"]

class CmdObj(object):
    
    def __init__(self, cId, cmdName, vars):
        self.cId = cId
        self.cmdName = cmdName
        self.vars = vars
        
class cmdRs():
    def __init__(self, cId, rs):
        self.cId = cId
        self.rs = rs
        
class ColloectorCallClient(object):
    
    def __init__(self, host, port=13522, timeout=60):
        self._host = host
        self._port = port
        self._timeout=timeout
    
    def __getSocket(self):
        """
                得到SSL套接字
        """
        address = (self._host, self._port)
        TCPClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TCPClient.settimeout(self._timeout)
        TCPClient.connect(address)
        return TCPClient
    
    
    def checkCmdRs(self, cmdId):
        mc = {}
        sTime = time.time()
        while True:
            rs = mc.get(cmdId)
            if not rs:
                if time.time() - sTime > self._timeout:
                    return None
                
                time.sleep(1)
                continue
            
            return pickle.loads(rs)
        
    
    def call(self, collId, callType, vars=None):
        """
        调用/发送数据到收集器
        @param callType: <string>调用类型\标识
        @param vars: <dict>附加参数
        @return: {"data":obj, "message":"str"}
        """
        message=""
        s=None
        try:  
            s = self.__getSocket()
        except socket.gaierror, e:  
            message='连接服务器地址错误:%s'%e
        except socket.error, e:  
            message='连接出错:%s' % e
            
        print message
        
        if s is None:return {"data":[], "message":message}

        #构建cmdobj
        cmdId = "%s:%d%d" %(collId, time.time()*1000, getCmdIndex())
        cmdObj = CmdObj(cmdId, callType, vars)
        #发送
        pickleCmdObj = pickle.dumps(cmdObj)
        s.send(pickleCmdObj)
        
        #检测结果
        cmdRs = self.checkCmdRs(cmdId)
        s.close()
        #返回
        if not cmdRs:
            return {"data":[], "message":"warn:未返回任何结果,可能在执行过程中超时!"}
        if cmdRs:
            return {"data":cmdRs.rs}
        
        return None

    

    
    
    
if __name__ == "__main__":
    ColloectorCallClient("192.168.2.104").call("coll001", "sum", [4, 9])
    print "over!"
                
                