#coding=utf-8
import time
import datetime
class TimeIntervalUtil(object):
    """
    时间分割处理类
    """
    def timeTransform(self,lastTime,timeRange):
        """
        将长整形时间转化成月,周,日,小时,得到按Range分割的开始时间和结束时间
        """
        year=int(time.strftime("%Y",time.localtime(lastTime)))
        if timeRange==2592000:
            month=int(time.strftime("%m",time.localtime(lastTime)))
            firstTime=time.mktime(datetime.date(year,month,1).timetuple())
            strTime="%s月"%(month)
        elif timeRange==604800:
            week=datetime.date(*time.localtime(lastTime)[:3])
            firstTime=time.mktime((week-datetime.timedelta(days=week.weekday())).timetuple())
            strTime="%s周"%(week.isocalendar()[1])
        elif timeRange==86400:
            day=time.strftime("%d",time.localtime(lastTime))
            firstTime=time.mktime(datetime.date(*time.localtime(lastTime)[:3]).timetuple())
            strTime="%s日"%(day)
        else:
            hour=time.strftime("%H时",time.localtime(lastTime))
            firstTime=time.mktime(list(time.localtime(lastTime))[:4]+[0,0, 0, 0, 0])
            strTime="%s"%(hour)
        return firstTime,strTime
    
    def getIntervalTime(self,timeRange=3600,intervalNum=10):
        """
        得到按照时间间隔分割的时间段
        """
        lastTime=time.time()
        IntervalTimes=[]
        for i in xrange(intervalNum):
            startTime,strTime=self.timeTransform(lastTime-1,timeRange)
            oneRangeTime={"lastTime":lastTime,"firstTime":startTime,"date":strTime}
            lastTime=startTime
            IntervalTimes.append(oneRangeTime)
        IntervalTimes.reverse()
        return IntervalTimes
    
if __name__=="__main__":
        tu=TimeIntervalUtil()