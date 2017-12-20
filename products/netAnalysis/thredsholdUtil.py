#coding=utf-8
import re
from products.netUtils import xutils
from products.netAnalysis.utils import TaskProcessUtil, CommonUtil
import md5
from products.netAnalysis.rpycUtil import RpycUtil
from products.netModel.templates.threshold import Threshold
        
class DataPointThredsholdUtil(object):

    @classmethod
    def dealDataPointThresholdEvent(cls, value, mo, dataPoint, rdata):
        """
        处理阀值, 生成事件
        处理数值型的数据点的Threshold事件
        @note: 
        evtKey是由componentType+moUid+tpl+ds+dp+th+阀值类型+agent+级别，构成的
        evtKeyId,是evtKey的MD5码
        clearId,是evtKey的级别为0的MD5码
        无论何种级别的事件，都会产生相同的clearId,以便在clear事件过来时，清除相关的事件
        如何区分clear事件与普通的事件？？根据它们的级别不同作出判断clear事件severity=0
        """
        if value is None: return
        title = rdata.get("title","")
        componentType=rdata["componentType"]
        moUid = rdata["moUid"]
        agent = rdata["agent"]
        collector = rdata.get('collector', None)
        objThresholds = mo.objThresholds
        eventInfo = {
            "moUid":moUid, "title":title,
            "componentType":componentType, "agent":agent,'collector':collector
        }
        #增加收集点的相关属性
        if rdata.get("collectPointUid",""):
            eventInfo["collectPointUid"] = rdata.get("collectPointUid","") #uid
            eventInfo["collectPointTitle"] = rdata.get("collectPointTitle","")
      
 
        for threshold in dataPoint.thresholds.values():
            thname = threshold.uname
            thdKey = "%s|%s|%s|%s" %(dataPoint.tplname,dataPoint.dsname,dataPoint.uname,thname)
            if objThresholds.get(thdKey,None):
                medata = objThresholds[thdKey]
                threshold = Threshold.createInst(medata)
            monitored = threshold.get("monitored")
            if monitored==False:continue 
            severity = threshold.get("severity", xutils.severitys['warning'])
            rpnvalue=None
            if threshold.get("rpn",""):
                exec(threshold.get("rpn"))
            if rpnvalue is not None:
                threshold.rpnvalue = rpnvalue #后期绑定rpn阀值
            threshold.dataPoint = dataPoint #后期绑定数据点
            thresholdType = threshold.get("type")
            recordId = TaskProcessUtil.getRlodRecordId(rdata)
            preEvtKey="%s|%s<%s>.agent=%s" %(recordId, threshold.uname, thresholdType, agent)
            evtKey = "%s.severity:%s" %(preEvtKey, severity)
            _clearEvtKey = "%s.severity:%s" %(preEvtKey, 0)
            evtKeyId = md5.new(evtKey).hexdigest()
            clearId = md5.new(_clearEvtKey).hexdigest()
            
            eventInfo.update(dict(
                severity=severity,evtKey=evtKey,evtKeyId=evtKeyId,clearId=clearId
            ))
            
            
                
            if thresholdType == "MinThreshold":
                cls._dealMinThreshold(title, value, threshold, eventInfo)
                
            if thresholdType == "MaxThreshold":
                cls._dealMaxThreshold(title, value, threshold, eventInfo)
                
            if thresholdType == "RangeThreshold":
                cls._dealRangeThreshold(title, value, threshold, eventInfo)
                
            if thresholdType == "StatusThreshold":
                cls._dealStatusThreshold(title, value, threshold, eventInfo)
            
            if thresholdType == "KeyThreshold":
                cls._dealKeyThreshold(title, value, threshold, eventInfo)
            
            if thresholdType == "CompareThreshold":
                drecordId="%s|%s" %(recordId, threshold.uname)
                cls._dealCompareThreshold(title, value, threshold, eventInfo,drecordId)
            

    @classmethod
    def _dealMinThreshold(cls, title, value, thredshold, eventInfo):
        """
        根据当前Threshold处理逻辑，调整修改eventInfo内容，并发送事件
        """
        
        if value is None: return
        min = CommonUtil.transVal(thredshold.get("min"))
        unit = thredshold.dataPoint.get("unit", None)
        if hasattr(thredshold,"rpnvalue"):min=thredshold.rpnvalue*min
        if min != None and value < min:
            message = thredshold.formatEvtMessage(title, value, unit=unit, eventInfo=eventInfo)
            eventInfo.update( {'message': message})
            RpycUtil.sendEvent(eventInfo)
            return 
       
            
        #发送clear事件
        eventInfo.update( {'message': "clear event", 'severity':xutils.severitys["clear"]})
        RpycUtil.sendEvent(eventInfo)

    @classmethod
    def _dealMaxThreshold(cls, title, value, thredshold, eventInfo):
        """
        根据当前Threshold处理逻辑，调整修改eventInfo内容，并发送事件
        """
        if value is None: return
        max = CommonUtil.transVal(thredshold.get("max"))
        if hasattr(thredshold,"rpnvalue"):max=thredshold.rpnvalue*max
        unit = thredshold.dataPoint.get("unit", None)
        if max != None and value > max:
            message = thredshold.formatEvtMessage(title, value, unit=unit, eventInfo=eventInfo)
            eventInfo.update( {'message': message})
            RpycUtil.sendEvent(eventInfo)
            return 
       
            
        #发送clear事件
        eventInfo.update( {'message': "clear event", 'severity':xutils.severitys["clear"]})
        RpycUtil.sendEvent(eventInfo)
        
    @classmethod
    def _dealRangeThreshold(cls, title, value, thredshold, eventInfo):
        """
        根据当前Threshold处理逻辑，调整修改eventInfo内容，并发送事件
        """
        if value is None: return
        min = CommonUtil.transVal(thredshold.get("min"))
        max = CommonUtil.transVal(thredshold.get("max"))
        if min == None or max == None: return
        if hasattr(thredshold,"rpnvalue"):
            max=thredshold.rpnvalue*max
            min=thredshold.rpnvalue*min
        unit = thredshold.dataPoint.get("unit", None)    
        if min <= value <= max:
            message = thredshold.formatEvtMessage(title, value, unit=unit, eventInfo=eventInfo)
            eventInfo.update( {'message': message})
            RpycUtil.sendEvent(eventInfo)
            return 
       
            
        #发送clear事件
        eventInfo.update( {'message': "clear event", 'severity':xutils.severitys["clear"]})
        RpycUtil.sendEvent(eventInfo)


    @classmethod
    def _dealStatusThreshold(cls, title, value, threshold, eventInfo):
        """
        处理StatusThreshold
        """
        if value is None: return
        status = str(threshold.get("status")) #标准的状态值
        if value is None:return
        if str(value) != status:
            message = threshold.formatEvtMessage(title, value, eventInfo=eventInfo)
            eventInfo.update( {'message': message})
            RpycUtil.sendEvent(eventInfo)
            return 
        
        #发送clear事件
        eventInfo.update( {'message': "clear event", 'severity':xutils.severitys["clear"]})
        RpycUtil.sendEvent(eventInfo)
        
    @classmethod
    def _dealKeyThreshold(cls, title, value, threshold, eventInfo):
        """
        处理KeyThreshold
        """
        if value is None: return
        key = str(threshold.get("key")) #标准的状态值
        if key is None:return
        rc=re.compile(key)
        rs=rc.search(str(value))
        if rs:
            message = threshold.formatEvtMessage(title, value, eventInfo=eventInfo)
            eventInfo.update( {'message': message})
            RpycUtil.sendEvent(eventInfo)
            return 
        
        #发送clear事件
        eventInfo.update( {'message': "clear event", 'severity':xutils.severitys["clear"]})
        RpycUtil.sendEvent(eventInfo)
        
        
    @classmethod
    def _dealCompareThreshold(cls, title, value, threshold, eventInfo,drecordId):
        """
        处理比对阀值
        """
        import time
        from products.netAnalysis.rloc import RecordLastOriginalCache
        value=str(value)
        dRecord=RecordLastOriginalCache.dget(drecordId, 5)
        record={"value":value,"timeId":time.time()}
        RecordLastOriginalCache.dset(drecordId, record)
        if dRecord is None: return
        dValue=dRecord.get("value")
        if not dValue==value:
            message = threshold.formatEvtMessage(title, value, eventInfo=eventInfo)
            eventInfo.update( {'message': message})
            RpycUtil.sendEvent(eventInfo)
            return 
        
        #发送clear事件
        eventInfo.update( {'message': "clear event", 'severity':xutils.severitys["clear"]})
        RpycUtil.sendEvent(eventInfo)