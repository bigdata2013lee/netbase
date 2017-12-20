#coding=utf-8
from products.netModel import medata
from products.netswgl.model.swglDocModel import SwglDocModel

class SEngineerFeedback(SwglDocModel):
    "用户对服务商工程师的评价"
    
    dbCollection = 'SEngineerFeedback'
    
    def __init__(self, uid=None):
        SwglDocModel.__init__(self)
        self._medata.update(dict(
            _id=uid, 
        ))

    sEngineer= medata.doc("sEngineer")
    fbType = medata.plain("fbType", 0) #评论类型
    fbTime = medata.plain("fbTime", 0) #评论时间
    summary = medata.plain("summary", "") #评论内容
 
    userID = medata.plain("userID", "") #用户编号
    userLabelName = medata.plain("userLabelName", "") #用户名
    
 
            
            

class SEngineerReport(SwglDocModel):
    "用户对服务商工程师的举报"
    
    dbCollection = 'SEngineerReport'
    def __init__(self, uid=None):
        SwglDocModel.__init__(self)
        self._medata.update(dict(
            _id=uid, 
        ))        
        
        
    sEngineer= medata.doc("sEngineer")
    fbTime = medata.plain("fbTime", 0) #举报时间
    fbType = medata.plain("fbType", 0) #举报类型
    summary = medata.plain("summary", "") #评论内容

    userID = medata.plain("userID", "") #用户编号
    userLabelName = medata.plain("userLabelName", "") #用户名
        
        
    
