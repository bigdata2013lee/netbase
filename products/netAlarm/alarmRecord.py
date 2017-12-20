#encoding:utf-8
import time
import logging
from products.netModel.baseModel import DocModel
from products.netModel import medata
from products.netModel.user.user import User
from products.netUtils import xutils

log = logging.getLogger("netalarm")


def getCurrentDate():
    """
    获取当前时间
    """
    data=time.time()
    st=time.localtime(data)
    return time.strftime("%Y-%m-%d %H:%M:%S",st)


class AlarmRecord(DocModel):
    dbCollection = 'AlarmRecord'
    def __init__(self):
        DocModel.__init__(self)
        self._medata.update(dict(
            alarmTime=getCurrentDate()           
        ))
        
    alarmContent = medata.plain("alarmContent", "")
    alarmEventId = medata.plain("alarmEventId", "")
    alarmUser = medata.plain("alarmUser", "")
    
    @classmethod
    def getAlarmRecord(cls):
        """ 
        获取告警记录
        """
        _records=AlarmRecord._findObjects({})                        
        return _records
    
    def getAlarmRecordsNumByEventIdAndUser(self,eventId,alarmUser):
        """
        根据事件ID获取告警记录数
        """
        condition={}
        condition["alarmEventId"] = eventId
        condition['alarmUser'] = alarmUser
        records=AlarmRecord._findObjects(conditions=condition)
        return len(records)  
      
    def delAlarmRecord(self):
        """
        删除当前记录
        """
        self.remove()
    
    def getUserByUseId(self):
        """
        根据用户ID获取用户对象
        """
        userObj = User._findObjects({'_id':self.alarmUser})
        if len(userObj) > 0:
            return userObj[0]
        else:
            alarmUser=xutils.fixObjectId(self.alarmUser)
            if alarmUser != self.alarmUser:
                userObj = User._findObjects({'_id':alarmUser})
                if len(userObj) > 0:
                    return userObj[0]
            raise  Exception("数据不同步，由于找不到通知地址，本事件不能通知用户")
            return False
       
    def addRecord(self,alarmContent,alarmEventId,alarmUser):
        """
        新增告警记录
        """
        self._saveObj()
        self.alarmContent=alarmContent
        self.alarmEventId=alarmEventId
        self.alarmUser=alarmUser
        