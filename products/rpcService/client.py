#coding=utf-8

import rpyc

class Client(object):
    """
    连接Netbase Rpc Service客户端。
    Client无需手动关闭， 在系统回收client对象时，连接会自动关闭；
    请勿在短时间内频繁创建client, 
    如果你的确需要频繁访问Rpc Service，共享连接client是最合适的办法。
    """
    def __init__(self, hostName="localhost", port=12233):
        self.hostName = hostName
        self.port = port
        self.__conn = self.__getConnect()
    
    def __getConnect(self):
        conn = rpyc.connect(self.hostName, self.port, config={"allow_public_attrs":True})
        return conn
    
        
    def access(self, accessFun, *agvs, **kws):
        if self.__conn  and  self.__conn.closed:
            self.__conn = self.__getConnect()
        
        kws['serviceObj'] = self.__conn.root
        rs = None
        try: rs = accessFun(*agvs, **kws)
        except Exception, e:
            raise e
        finally: pass
        return rs

    def getServiceObj(self):
        if self.__conn  and  self.__conn.closed:
            self.__conn = self.__getConnect()
            
        serviceObj = self.__conn.root
        return serviceObj
    
    
if __name__ == '__main__':
    c = Client()
    sobj = c.getServiceObj()
    
    
    
    
    
    
    
    
    
    
    
