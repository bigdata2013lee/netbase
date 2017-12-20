#coding=utf-8
import time
import datetime
class TimeUtil(object):
    """
        报表时间处理类
    """
    dateMap=[(0.5,3600),(1,7200),(5,3600*12),(15,86400),(31,172800),(90,604800),(365,2592000),(365*5,31536000)]
    def getDataRange(self,startTime,endTime):
        """
                得到显示时间跨度(本报表只可计算1年内的数据)
        """
        dataRange=86400
        totalTime=endTime-startTime
        days = totalTime/float(dataRange)
        for key,value in self.dateMap:
            if days<=key:return value
        else:
            return self.dateMap[0.5]
    
    def calculateSplitDate(self,startTime,endTime):
        """
                计算分割时间日期
        """
        splitDate=[]
        endTime=self.timeToInt(endTime, 3600)
        startTime=self.timeToInt(startTime, 3600)
        timeRange=self.getDataRange(startTime, endTime)
        for i in xrange(18):
            endTime=self.timeToInt(endTime,3600)
            firstTime,lastTime,strTime=self.timeTransform(endTime,timeRange)
            endTime=firstTime
            if firstTime>startTime:pass
            elif lastTime>startTime:
                firstTime=startTime
            else:break
            oneRangeTime={"lastTime":lastTime,"firstTime":firstTime,"date":strTime}
            splitDate.append(oneRangeTime)
        return splitDate
    
    def timeTransform(self,lastTime,dataRange):
        """
                将长整形时间转化成年,月,周,日,小时,得到按Range分割的开始时间和结束时间
        """
        if dataRange>=31536000:
            lastTime=lastTime-1
            year=int(time.strftime("%Y",time.localtime(lastTime)))
            firstTime=time.mktime(datetime.date(year,1,1).timetuple())
            strTime="%s年"%(year)
            lastTime=lastTime+1
        elif dataRange==2592000:
            lastTime=lastTime-1
            year=int(time.strftime("%Y",time.localtime(lastTime)))
            month=int(time.strftime("%m",time.localtime(lastTime)))
            firstTime=time.mktime(datetime.date(year,month,1).timetuple())
            strTime="%s月"%(month)
            lastTime=lastTime+1
        elif dataRange==604800:
            lastTime=lastTime-1
            year=int(time.strftime("%Y",time.localtime(lastTime)))
            week=datetime.date(*time.localtime(lastTime)[:3])
            firstTime=time.mktime((week-datetime.timedelta(days=week.weekday())).timetuple())
            strTime="%s周"%(week.isocalendar()[1])
            lastTime=lastTime+1
        elif 43200<dataRange<=172800:
            day=time.strftime("%d",time.localtime(lastTime))
            firstTime=time.mktime(datetime.date(*time.localtime(lastTime-dataRange)[:3]).timetuple())
            strTime="%s日"%(day)
        else:
            hour=time.strftime("%d日%H时",time.localtime(lastTime))
            firstTime=time.mktime(list(time.localtime(lastTime-dataRange))[:4]+[0,0, 0, 0, 0])
            strTime="%s"%(hour)
        return firstTime,lastTime,strTime
    
    def timeToInt(self,stampTime,dataRange):
        """
                时间取整
        """
        stampTime=(int(stampTime)/dataRange)*dataRange
        return stampTime

    def stampToTime(self,stampValue):
        """
                将stamp类型的时间转化为秒数
        """
        timeTuple = time.strptime(stampValue, '%Y-%m-%d %H:%M:%S')
        stampTime = time.mktime(timeTuple)
        return stampTime

if __name__=="__main__":
    tu=TimeUtil()
    tu.calculateSplitDate(time.time()-365*24*3600,time.time())
    
    