#coding=utf-8

import re
import types
import difflib

from products.netAnalysis.rloc import RecordLastOriginalCache
from products.netAnalysis.rpn.rpn import RpnTools
from products.netAnalysis.rpycUtil import RpycUtil
from products.netUtils import xutils





def _sendEvent(eventInfo):
    "发送事件"
    _eventInfo = {}
    _eventInfo.update(eventInfo)
    RpycUtil.sendEvent(_eventInfo)


class StatusUtil(object):
    "状态工具类，状态指监控对象的up|down状态"
    
    pass
        
        
class CommonUtil(object):
    @classmethod
    def transVal(cls, val, default=None):
        """
            转换数值类型，如果转换不成功返回默认值
            @param val: 需要转换的值
            @param default:默认值
        """
        if type(val) in types.StringTypes:
            val = val.strip()
            if not val: return default
            if(re.match(r"\d+\.\d+",val)): return float(val)
            if re.match(r"\d+", val): return int(val)
        if type(val) in (types.IntType, types.FloatType, types.LongType): return val        
        return  default


            
class StrStatusUtil(object):
    
    @classmethod
    def keyword(cls, text, word):
        if not (text or word): return "unknow"
        if text.find(word) >= 0: return True
        
        return False
    
    @classmethod
    def compare(cls, newText, standText):
        if not (newText or standText): return "unknow"
        newText = str(newText)
        standText = str(standText)
        
        newTextLines = newText.splitlines(1)
        standTextLines = standText.splitlines(1)
        diffInstance = difflib.Differ()
        diffList = list(diffInstance.compare(newTextLines, standTextLines))
        rs = ""
        for line in diffList:
            rs += line + "\n"
        
        return rs
      
    @classmethod
    def guage(cls, text):
        return text

class PerfUtil(object):
    
    @classmethod
    def derive(cls, mo, curTimeId, rdata):
        """
            求差值
            找到“前一个原始记录”， 如果“前一个原始记录”，不存在，返回None,
            如果“前一个原始记录”的时间点，早于timeout（过期时间，默认300秒），返回None
            @param mo:监控对象
            @param curTimeId:当前数据的时间戳
            @param rdata:   实时数据
        """
        
        record = cls.findPreRecord(rdata)
        if not record: return None
        
        timeout = 1800 #秒
        curTimeId = CommonUtil.transVal(curTimeId, default=0) #当前分析的数据时间点
        preTimeId = CommonUtil.transVal(record["timeId"]) #最后记录的数据时间点
        if curTimeId - preTimeId > timeout: return None
        preVal = CommonUtil.transVal(record["value"], default=0)
        value = CommonUtil.transVal(rdata["value"], default=0)
        #print preVal,value,rdata["value"]
        
        v =  value - preVal
        if v < 0 : return 0
        return v
    
    @classmethod
    def absolute(cls, mo, rdata):
        """
            求绝对值
            @param mo:监控对象
            @param rdata:  实时数据
        """
        value = CommonUtil.transVal(rdata["value"], default=0)
        return abs(value)
               
    @classmethod      
    def findPreRecord(cls, rdata):
        """
            求前一次的原始记录
            @param rdata:实时数据
        """
        recordId =TaskProcessUtil.getRlodRecordId(rdata)
        record = RecordLastOriginalCache.getPre(recordId)
        return record
    
       
    
        
class TaskProcessUtil(object):
    """
        处理过程的工具
    """
    
    @classmethod
    def getDbName(cls, rdata):
        uid = rdata["moUid"]
        componentType = rdata.get('componentType',"")
        return xutils.fixPerfDbName(uid, componentType)
    
    @classmethod
    def getTableName(cls, rdata):
        """
        构建性能数据表名
        @param rdata:实时数据
        """
        uid = rdata["moUid"]
        tableName = "|".join([rdata.get("templateUid"), rdata.get("dataSource"), rdata.get("dataPoint")])
        
        #如果有收集点，把收集点作为表名一部分
        if rdata.get("collectPointUid",""): tableName += "|cpt_%s" %rdata.get("collectPointUid","")
        return "%s:%s" %(uid, tableName)
    
    @classmethod
    def getStringStatusDatasTableName(cls, rdata):
        uid = rdata["moUid"]
        return "%s:string_status_datas" %uid
    
    @classmethod
    def getStringStatusDatasRecordId(cls, rdata):
        """
        生成字符状态数据记录编号(_id)
        """
        recordId = "|".join([rdata.get("templateUid"), rdata.get("dataSource"), rdata.get("dataPoint")])
        
        #如果有收集点，把收集点作为表名一部分
        if rdata.get("collectPointUid",""): recordId += "|cpt_%s" %rdata.get("collectPointUid","")
        return recordId
    
    @classmethod
    def getStatusTableName(cls, rdata):
        uid = rdata["moUid"]
        #如果有收集点，把收集点作为表名一部分
        tableName = "%s:status" %uid
        if rdata.get("collectPointUid",""): tableName += "|cpt_%s" %rdata.get("collectPointUid","")
        return tableName
    
    @classmethod
    def getRlodRecordId(cls, rdata):
        """
        生成原始数据记录编号(_id)
        """
        uid = rdata["moUid"]
        componentType = rdata.get('componentType',"")
        
        recordId = "|".join([rdata.get("templateUid"), rdata.get("dataSource"), rdata.get("dataPoint")])
        #如果有收集点，把收集点作为表名一部分
        if rdata.get("collectPointUid",""): recordId += "|cpt_%s" %rdata.get("collectPointUid","")
        _recordId = "%s-%s:%s" %(componentType, uid, recordId)
        
        return _recordId
   
   
    @classmethod
    def getThredsholds(cls, tpl, dsName, dpName):
        """
        获取数据点的所有阀值
        @param obj: 设备|组件 
        @param tplName: 模板名称
        @param dsName: 数据源名称
        @param dpName: 数据点名称
        """
        dp = None; thresholds = {};
        
        if not tpl: return thresholds
        
        ds = tpl.getDataSource(dsName)
        if ds: dp = ds.dataPoints.get(dpName, None)
        if dp: thresholds = dp.thresholds
        
        return thresholds
    
    
    @classmethod
    def getDataPoint(cls, tpl, rdata):
        """
        @param tpl: 
        @param rdata: 实时数据
        """
        dsName = rdata["dataSource"]; dpName = rdata["dataPoint"]
        if not tpl: return None
        ds = tpl.getDataSource(dsName)
        if ds: dp = ds.dataPoints.get(dpName, None)
        dp.dsname = dsName
        dp.tplname = tpl._medata["_id"]
        return dp
 

    @classmethod
    def dealStringDataPoint(cls, timeId, mo, dataPoint, rdata):
        from products.netAnalysis.thredsholdUtil import DataPointThredsholdUtil
        _dataPointType = dataPoint.get("type")
        value = rdata["value"]
        dbName = cls.getDbName(rdata)
        stringStatusDatasTableName = cls.getStringStatusDatasTableName(rdata)
        if _dataPointType == "Keyword": #关键字查找
            word =  dataPoint.get("word", None)
            rs = StrStatusUtil.keyword(value, word)
            
        elif _dataPointType == "Compare": #比较
            standText =  dataPoint.get("standText", "")
            rs = StrStatusUtil.compare(value, standText)
            
        else: #原始文本
            rs = StrStatusUtil.guage(value)
            
        recordId = TaskProcessUtil.getStringStatusDatasRecordId(rdata)
        RpycUtil.insertStrStatusData(dbName, stringStatusDatasTableName, recordId, timeId, rs)
        DataPointThredsholdUtil.dealDataPointThresholdEvent(value, mo, dataPoint, rdata)
        
    @classmethod
    def dealNunDataPoint(cls, timeId, mo, tpl, dataPoint, rdata):
        from products.netAnalysis.thredsholdUtil import DataPointThredsholdUtil
        
        value = CommonUtil.transVal(rdata["value"])
        if value is None: return
        dbName = cls.getDbName(rdata)
        tableName = cls.getTableName(rdata)
        
        def callback(value):
            RpycUtil.insertPerfData(timeId, value, dbName, tableName)
            DataPointThredsholdUtil.dealDataPointThresholdEvent(value, mo, dataPoint, rdata)
            
        _dataPointType = dataPoint.get("type")
        if _dataPointType == "DERIVE": #差值
            value = PerfUtil.derive(mo, timeId, rdata)
            if value is None: return None
        
        elif _dataPointType == "GUAGE": #原始值
            pass
            #print "deal GUAGE"
        
        elif _dataPointType == "ABSOLUTE": #绝对值
            value = PerfUtil.absolute(mo, rdata)
            
        elif _dataPointType == "RPN": #RPN公式
            rpnCode = dataPoint.get("rpn", "")
            RpnTools.receive(timeId, mo, rdata, rpnCode, callback)
            return
        
        else: return
        
        callback(value)






