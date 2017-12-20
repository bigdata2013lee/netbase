#coding=utf-8
'''
Created on 2012-12-7

@author: Administrator
'''
from pymongo import MongoClient
import threading
from products.netUtils.settings import DbSettings

settings = DbSettings.getSettings()

def getMongoConf(name="mongodbManager"):
    username,password = settings.get(name,'username'),settings.get(name,'password')
    host,port = settings.get(name, 'host'),settings.getAsInt(name,'port')   
    max_pool_size=settings.getAsInt(name,'maxPoolSize')
    
    database = "admin"#管理员用户认证
    HOST_URL = "mongodb://%s:%s@%s/%s" %(username,password,host,database)
    
    return dict(    
                host=HOST_URL,  port=port,
                max_pool_size=max_pool_size,
                connectTimeoutMs=60 * 1000
    )                           
             
    
lock0 = threading.Lock()
lock1 = threading.Lock()
lock2 = threading.Lock()
lock3 = threading.Lock()
lock4 = threading.Lock()

   
def getNetCenterDB():
    "getNetCenterDB"
    client = None
    dbName = "netcenter"
    lock0.acquire()
    m = getNetCenterDB
    if not getattr(m, '_client', None):
        try:
            print ">>> new netcenter db client instance..."
            client = MongoClient(**getMongoConf("userCenterMongodb"))
        except Exception, e:
            lock0.release()
            raise e
        m._client = client
    else: client = m._client
    
    db = getattr(client, dbName)
    lock0.release()
    return db

def getSwglDB():
    "getSwglDB"
    client = None
    dbName = "swgl"
    lock4.acquire()
    m = getNetCenterDB
    if not getattr(m, '_client', None):
        try:
            print ">>> new swgl db client instance..."
            client = MongoClient(**getMongoConf("userCenterMongodb"))
        except Exception, e:
            lock4.release()
            raise e
        m._client = client
    else: client = m._client
    
    db = getattr(client, dbName)
    lock4.release()
    return db
   
   
def getNetbaseDB():
    "getNetbaseDB"
    client = None
    dbName = "netbase"
    lock1.acquire()
    m = getNetbaseDB
    if not getattr(m, '_client', None):
        try:
            print ">>> new netbase db client instance..."
            client = MongoClient(**getMongoConf(name="confDataMongodb"))
        except Exception, e:
            lock1.release()
            raise e
        m._client = client
    else: client = m._client
    
    db = getattr(client, dbName)
    lock1.release()
    return db
    
    
def getNetEventDB():
    "getNetEventDB"
    client = None
    dbName = 'netevent'
    lock2.acquire()
    m = getNetEventDB
    if not getattr(m, '_client', None):
        try:
            print ">>> new netevent db client instance..."
            client = MongoClient(**getMongoConf(name="confDataMongodb"))
        except Exception, e:
            lock2.release()
            raise e
        m._client = client
    else: client = m._client
    
    db = getattr(client, dbName)
    lock2.release()
    return db




def getNetPerfDB(dbName):
    "getNetPerfDB"
    client = None
    lock3.acquire()
    m = getNetPerfDB
    if not getattr(m, '_client', None):
        try:
            print ">>> new getNetPerfDB db client instance..."
            client = MongoClient(**getMongoConf(name="perfDataMongodb"))
        except Exception, e:
            lock3.release()
            raise e
        m._client = client
    else: client = m._client
    
    db = getattr(client, dbName)
    lock3.release()
    return db



def getPerfDataBaseNames():
    "得到性能数据库的所有库名"
    try:
        client = MongoClient(**getMongoConf(name="perfDataMongodb"))
        dbNames=client.database_names()
        return dbNames
    except Exception, e:
        raise e
    return None    
    