# -*- coding: utf-8 -*-
import pickle
import redis
import time

class TransRDobject(object):
    """
    序列化与反序列化实时数据工具
    """
    @classmethod
    def dumps(cls, rd):
        return pickle.dumps(rd)
    
    @classmethod
    def loads(cls, transRd):
        return pickle.loads(transRd)
    
class RealtimeData(object):
    def __init__(self, timeId, value):
        self.value = value
        self.timeId = timeId

class Client(object):
    """
    访问实时数据库的客户端
    """
    componentTypes = ['Network', 'Device', "Website", "IpInterface", "Process", "FileSystem", "IpService"]
    componentTypes += ['MwApache','MwTomcat','MwNginx','MwIis']
    acceptedDataAreas = ['ping', 'syslog', 'events'] + componentTypes
    
    def __init__(self, host="localhost", port=6379):
        self.host = host
        self.port = port
        self.cnn = self.__connect()
   
    def clear(self, dataArea):
        """
        清除某个数据区
        @param dataArea: type->string 数据区
        """
        self.cnn.delete(dataArea) 
        
            
    def got(self, dataArea):
        """
        取走数据区的“最早”一条数据
        @param dataArea: type->string 数据区
        @return: type->RealtimeData
        """
        pdata = self.cnn.lpop(dataArea)
        if not pdata: return None
        rd = TransRDobject.loads(pdata)
        return rd
    
    def insert(self, value, dataArea):
        """
        向数据区插入值
        @param value: 值、数据
        @param dataArea: type->string 数据区
        """
        if dataArea not in Client.acceptedDataAreas:
            raise Exception('Data Area [%s] is not accepted.' % dataArea)
        tId = int(time.time())
        tId = tId - tId%60 #取值到分钟的时间点
        rdData = RealtimeData(tId, value)
        pdata = TransRDobject.dumps(rdData)
        self.cnn.rpush(dataArea, pdata)
        return True
    
    def set(self, key, val, expire=0):
        self.cnn.set(key, pickle.dumps(val))
        if expire:
            self.cnn.expire(key, expire)
        
        
    def get(self, key):
        val = self.cnn.get(key)
        if val is None: return None
        return pickle.loads(val)
        
    
    def __connect(self):
        pool = redis.ConnectionPool(host=self.host, port=self.port, db=0)
        cnn = redis.Redis(connection_pool=pool, socket_timeout=10)
        return  cnn
    



        
        
        
        

class Person(object):
    def __init__(self, name):
        self.name = name
                
if __name__ == "__main__":
    c = Client("192.168.2.101")
    
    key = "myname"
    c.set(key,Person("yezi"), 0)
    
    
    for x in range(100):
    
        try:
            time.sleep(4)
            val = c.get(key)
            
            print x, " ", val.name
            
        except:
            pass
            
    
    
        
        
        
