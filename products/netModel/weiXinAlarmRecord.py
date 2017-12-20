#coding=utf-8
from products.netModel.baseModel import DocModel
from products.netModel import medata
import re
import time

        
def _parseTime(timeStr):
    """
        解析时间
    """

    rep = re.compile(r'(\d{4})-(\d{2})-(\d{2})\s(\d{2}):(\d{2}):(\d{2})')
    m = rep.match(timeStr)
    dt = time.mktime((int(m.group(1)),
                      int(m.group(2)),
                      int(m.group(3)),
                      int(m.group(4)),
                      int(m.group(5)),
                      int(m.group(6)),0,0,0))
    return dt


class WeiXinAlarmRecord(DocModel):
    dbCollection = 'WeiXinAlarmRecord'
    def __init__(self):
        DocModel.__init__(self)
        
    alarmContent = medata.plain("alarmContent", "")
    alarmEventId = medata.plain("alarmEventId", "")
    alarmUser = medata.plain("alarmUser", "")
    alarmTime = medata.plain("alarmTime", "")
    
    @classmethod
    def getNewestAlarmRecord(cls, username):
        """
        @return: object
        """
        rs = WeiXinAlarmRecord._findObjects(conditions={"alarmUser": username}, sortInfo={"alarmTime":-1}, limit=1)[0]
        return rs
        
