#-*- coding:utf-8 -*-

from products.netRealTimeDB.redisClient import Client

class RedisManager(object):
    """
    功能:事件管理类,提供对事件的集中管理
    作者:lb
    时间:2013-3-8
    """
    redisClient = Client()
    
    def __init__(self):pass
        
    def saveEvent(self,evtDict):
        """
        功能:发送事件到redis,data便于结构调整
        作者:lb
        时间:2013-3-8
        """
        moUid=evtDict.get("moUid")
        componentType=evtDict.get("componentType")
        severity=evtDict.get("severity")
        collector=evtDict.get("collector")
        agent=evtDict.get("agent")
        clearKey="%s|%s|%s|%s"%(moUid,componentType,collector,agent)
        evtKey="%s|%s|%s|%s|%s"%(moUid,componentType,collector,agent,severity)
        data = {
                "moUid":moUid,
                "title":evtDict.get("title"),
                "componentType":componentType,
                "message":evtDict.get("message"),
                "evtKey":evtKey,
                "clearKey":clearKey,
                "severity":severity,
                "collector":collector,
                "agent":agent
            }
        if  evtDict.has_key("eventClass"):
            data.update(dict(eventClass=evtDict.get("eventClass")))
        if evtDict.has_key("collectPointUid"):
            collectPointUid=evtDict.get("collectPointUid")
            clearKey="%s|%s|%s|%s|%s"%(moUid,componentType,collector,agent,collectPointUid)
            evtKey="%s|%s|%s|%s|%s|%s"%(moUid,componentType,collector,agent,collectPointUid,severity)
            message="收集点%s:%s"%(evtDict.get("collectPointTitle"),evtDict.get("message"))
            data.update(dict(collectPointUid=collectPointUid,clearKey=clearKey,evtKey=evtKey,message=message))
        self.redisClient.insert(data,"events")
        
    def saveResult(self,resDict):
        """
        功能:发送结果到redis,data便于结构调整
        作者:lb
        时间:2013-3-8
        """
        data = {
          "moUid":resDict.get("moUid"),
          "title":resDict.get("title"),
          "componentType":resDict.get("componentType"),
          "templateUid":resDict.get("templateUid"),
          "dataSource":resDict.get("dataSource"),
          "dataPoint":resDict.get("dataPoint"),
          "agent":resDict.get("agent"),
          "value":resDict.get("value")
        }
        if resDict.has_key("collectPointUid"):
            data.update(dict(collectPointTitle=resDict.get("collectPointTitle")))
            data.update(dict(collectPointUid=resDict.get("collectPointUid")))
        self.redisClient.insert(data,resDict.get("componentType",None))