#coding:utf-8
import ssl
import pickle
import socket
import time
from products.netUtils.xutils import nbPath as _p

class ColloectorCallClient(object):
    
    def __init__(self, host, port=12368, timeout=60):
        self._host = host
        self._port = port
        self._timeout=timeout
    
    def __getSocket(self):
        """
                得到SSL套接字
        """
        ADDR = (self._host, self._port)
        TCPClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TCPClient.settimeout(self._timeout)
        sslSock = ssl.wrap_socket(TCPClient,
                           ca_certs=_p("/bin/cacert.pem"),
                           cert_reqs=ssl.CERT_REQUIRED)
        sslSock.connect(ADDR)
        return sslSock
    
    
    def call(self, callType, vars={}):
        """
        调用/发送数据到收集器
        @param callType: <string>调用类型\标识
        @param vars: <dict>附加参数
        @return: {"data":obj, "message":"str"}
        """
        s=None
        try:  
            s = self.__getSocket()
        except socket.gaierror, e:  
            message='连接服务器地址错误:%s'%e
        except socket.error, e:  
            message='连接出错:%s' % e

        if s is None:return {"data":[], "message":message}

        _vars = {}
        _vars.update(vars)
        _vars.update({"clsName": callType})
        
        pickleVars = pickle.dumps(_vars)
        s.send(pickleVars)
        revData=""
        try:
            while True:
                data=s.recv(1024)
                if data.strip():
                    revData+=data
                else:
                    break
        except:
            return {"data":[], "message":"warn:获取配置超时,请检查SNMP/SSH配置是否正确!"}
        finally:s.close()
        if not revData:return {"data":[], "message":"warn:未返回任何结果,请检查SNMP/SSH配置是否正确!"}
        return {"data":pickle.loads(revData)}
    
    def verifyDevice(self,vars):
        """
                验证设备联通性和SNMP配置是否正确
        """
        s=None
        try:  
            s = self.__getSocket()
        except socket.gaierror, e:  
            message='warn:连接服务器地址错误:%s'%e
        except socket.error, e:  
            message='warn:连接出错:%s' % e

        if s is None:return {"data":{}, "message":message}

        _vars = {}
        _vars.update(vars)
        _vars.update({"clsName": "discoverDevice"})
        pickleVars = pickle.dumps(_vars)
        s.send(pickleVars)
        revData=""
        try:
            while True:
                data=s.recv(1024)
                if data.strip():
                    revData+=data
                else:
                    break
        except:
            return {"data":{}, "message":"warn:验证设备信息超时!!"}
        finally:s.close()
        if not revData:return {"data":{}}
        return pickle.loads(revData)
    
    
    
if __name__ == "__main__":
    t1 = time.time()
    cCall = ColloectorCallClient("192.168.1.89")
    data={"uid":"5212e6799c59154eb308b56c","componentType":"Device"}
    #rs1 = cCall.call("HRSWRunMap", vars=data)
    #rs2 = cCall.call("InterfaceMap", vars=data)
    rs3 = cCall.call("HRFileSystemMap", vars=data)
    t2 = time.time()
                
                