#coding=utf-8
import threading
import time

class RecordLastOriginalCache(object):
    """
    建立最后的原始记录缓存机制
    @note: 
        原始数据记录可以类似设计及实现
        1.与记录表的结构一致的缓存
        2.缓存初始加载表中的所有数据
        3.只能从缓存中，获取数据记录
        4.id = moType-uid:tpl|ds|dp
    """
    
    __worked = False
    __cache = {}
    __preRecordCache = {}
    __datapointcache={}
    _timeout = 15 #分钟
    
    @classmethod
    def startWork(cls):
        if cls.__worked:
            return
        cls.__worked = True
        cls.__autoClear()
    
    
    @classmethod
    def get(cls, recordId):
        """
            返回最后一次插入数据的记录
            @param recordId: 记录ID
        """
        record =  cls.__cache.get(recordId, None)
        return record
    
    @classmethod
    def dget(cls, recordId, timeout=10):
        """
        返回数据点的上一次记录
        @param recordId: 记录ID
        """
        record =  cls.__datapointcache.get(recordId, None)
        if not record: return None
        if time.time() - record["timeId"] > timeout * 60:
            return None
        return record
    
    @classmethod
    def dset(cls, recordId, record):
        """
        缓存数据点这一次的记录
        @param record: 记录
        """
        if not (recordId or record): return
        cls.__datapointcache[recordId] = record
        
    @classmethod
    def getPre(cls, recordId):
        """
        获取上次原记录
        @param recordId: 记录编号
        @param timeOut: 过时时间(分钟)，意味着在timeout分钟前的记录是无效的,将返回None
        """
        record =  cls.__preRecordCache.get(recordId, None)
        if not record: return None
        if time.time() - record["timeId"] > cls._timeout * 60:
            return None
        return record
    
    @classmethod
    def set(cls, recordId, record):
        """
            设置记录（缓存最后操作的记录队列）
            @param recordId: 记录的ID
            @param record: 记录
        """
        if not (recordId or record): return
        
        record.update({"_id": recordId})
        if cls.__cache.has_key(recordId): #转移到上次记录缓存中
            cls.__preRecordCache[recordId] = cls.__cache.get(recordId)

        cls.__cache[recordId] = record
        

    @classmethod
    def __autoClear(cls):
        "定时维护清理"
        def __clearCacheMap(mapDict):
            for key, record in mapDict.items():
                    if time.time() - record.get("timeId",0) > 3600:  #忽略1小时前的记录
                        del mapDict[key]
                        
        def clear():
            while True:
                time.sleep(60 * 10)
                __clearCacheMap(cls.__cache)
                __clearCacheMap(cls.__preRecordCache)
                __clearCacheMap(cls.__datapointcache)
            
        th = threading.Thread(target = clear)
        th.setDaemon(True)
        th.start()
        
RecordLastOriginalCache.startWork()


