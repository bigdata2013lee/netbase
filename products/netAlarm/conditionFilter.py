#coding=utf-8
import re
from products.netPublicModel.modelManager import ModelManager
from products.netUtils.xutils import getEventManager
negativeMode=["!~","$ne"]
class ConditionFilter(object):
    """
    告警条件匹配
    """
    def fromFormVariables(self,forms):
        """
        格式转换
        """
        conditions=[]
        for form in forms:
            result=[]
            typeObj=eval(form.get("obj"))
            name=form.get("name")
            values=form.get("values")
            mode=form.get("mode")
            for value in values: 
                result.append(typeObj.buildClause(name,value,mode))                                           
                if mode in negativeMode:
                    conditions.append({"$and":result})
                else:
                    conditions.append({"$or":result})
        return {"$and":conditions}
    
class Select(object):
    """
    选择类型
    """
    modeType = 'select'
    def buildClause(self, name, v, mode):
        if mode=="":
            return {"%s"%name:"%s"%v}
        else:
            return {"%s"%name:{"%s"%mode:v}}
    
class Text(object):
    """
    文本类型
    """
    modeType = 'text'
    def buildClause(self, name, v, mode):
        if mode == '':
            return {"%s"%name:"%s"%v}%(name,v)
        elif mode == '~':
            return {"%s"%name:re.compile("%s"%v)}
        elif mode == '!~':
            return {"%s"%name:{"$not":re.compile("%s"%v)}}
        elif mode == '^':
            return {"%s"%name:re.compile('^%s'%v)}
        elif mode == '$':
            return {"%s"%name:re.compile("%s$"%v)}
        elif mode == '$ne':
            return {"%s"%name:{"%s"%mode:"%s"%v}}

Modes = """
 var modes = {
   text:[{text:"包含",value:"~"},
         {text:"不包含",value:"!~"},
         {text:"开始于",value:"^"},
         {text:"结束于",value:"$"},
         {text:"是",value:""},
         {text:"非",value:"$ne"}],
            
   select:[{text:"小于",value:"$lt"},
            {text:"小于或等于",value:"$lte"},
            {text:"等于",value:""},
            {text:"不等于",value:"$ne"},
            {text:"大于",value:"$gt"},
            {text:"大于或等于",value:"$gte"}]};
"""

if __name__=="__main__":
    from products.netPublicModel.startNetbaseApp import startApp
    startApp()
    af=ConditionFilter()
    forms=[{"obj":"Select()","mode":"$ne","values":[0,1,2,4],"name":"servrity"},{"obj":"Text()","mode":"!~","values":[360,"CPU","Mem"],"name":"message"}]
    ffv=af.fromFormVariables(forms)
    mgr=getEventManager()
    resultList=mgr.findHistoryEvents(ffv)
    
#    eventManager = ModelManager.getMod("eventManager")
#    rs=eventManager.findEvents(ffv)
#    for i in resultList:
    